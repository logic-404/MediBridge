"""Shared profile read/write — used by CLI onboarding and the HTTP API."""
from __future__ import annotations

import json

from medibridge.config import USER_PROFILE_JSON
from medibridge.data import db as dbmod

COVER_TYPES = ("single", "couple", "family", "sole_parent")


def has_profile() -> bool:
    try:
        with dbmod.get_conn() as conn:
            row = conn.execute("SELECT 1 FROM user_profile WHERE id = 1").fetchone()
        return row is not None
    except Exception:
        return False


def load_profile() -> dict | None:
    """Return profile rehydrated with insurer + tier records, or None."""
    with dbmod.get_conn() as conn:
        row = conn.execute(
            """SELECT
                    p.cover_type, p.policy_start_date,
                    t.tier_id, t.tier_name,
                    t.gp_benefit_pct, t.specialist_benefit_pct, t.in_hospital_benefit_pct,
                    i.insurer_id, i.insurer_name
               FROM user_profile p
               JOIN insurer_tiers t ON p.tier_id = t.tier_id
               JOIN insurers i ON t.insurer_id = i.insurer_id
               WHERE p.id = 1"""
        ).fetchone()
    if not row:
        return None
    return {
        "insurer": {"id": row["insurer_id"], "name": row["insurer_name"]},
        "tier": {
            "id": row["tier_id"],
            "name": row["tier_name"],
            "gp": row["gp_benefit_pct"],
            "spec": row["specialist_benefit_pct"],
            "in_hospital": row["in_hospital_benefit_pct"],
        },
        "cover": row["cover_type"],
        "date": row["policy_start_date"],
    }


def save_profile(tier_id: str, cover_type: str, policy_start_date: str) -> dict:
    """Upsert profile (id=1) in SQLite + JSON. Returns rehydrated profile."""
    if cover_type not in COVER_TYPES:
        raise ValueError(f"cover_type must be one of {COVER_TYPES}")
    with dbmod.get_conn() as conn:
        exists = conn.execute(
            "SELECT 1 FROM insurer_tiers WHERE tier_id = ?", (tier_id,)
        ).fetchone()
        if not exists:
            raise ValueError(f"Unknown tier_id: {tier_id}")
        conn.execute("DELETE FROM user_profile")
        conn.execute(
            "INSERT INTO user_profile (id, tier_id, cover_type, policy_start_date) VALUES (1, ?, ?, ?)",
            (tier_id, cover_type, policy_start_date),
        )
    USER_PROFILE_JSON.parent.mkdir(parents=True, exist_ok=True)
    USER_PROFILE_JSON.write_text(
        json.dumps(
            {
                "tier_id": tier_id,
                "cover_type": cover_type,
                "policy_start_date": policy_start_date,
            }
        ),
        encoding="utf-8",
    )
    profile = load_profile()
    if profile is None:
        raise RuntimeError("Profile write succeeded but reload failed")
    return profile


def clear_profile() -> None:
    with dbmod.get_conn() as conn:
        conn.execute("DELETE FROM user_profile")
    if USER_PROFILE_JSON.exists():
        USER_PROFILE_JSON.unlink()


def list_insurers() -> list[dict]:
    """Return [{id, name, tiers:[{id,name,gp,spec,in_hospital}]}] for onboarding UI."""
    with dbmod.get_conn() as conn:
        ins_rows = conn.execute(
            "SELECT insurer_id, insurer_name FROM insurers ORDER BY insurer_name"
        ).fetchall()
        tier_rows = conn.execute(
            """SELECT tier_id, insurer_id, tier_name,
                      gp_benefit_pct, specialist_benefit_pct, in_hospital_benefit_pct
               FROM insurer_tiers ORDER BY tier_name"""
        ).fetchall()
    by_insurer: dict[str, list[dict]] = {}
    for t in tier_rows:
        by_insurer.setdefault(t["insurer_id"], []).append(
            {
                "id": t["tier_id"],
                "name": t["tier_name"],
                "gp": t["gp_benefit_pct"],
                "spec": t["specialist_benefit_pct"],
                "in_hospital": t["in_hospital_benefit_pct"],
            }
        )
    return [
        {
            "id": ins["insurer_id"],
            "name": ins["insurer_name"],
            "tiers": by_insurer.get(ins["insurer_id"], []),
        }
        for ins in ins_rows
    ]
