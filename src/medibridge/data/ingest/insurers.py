"""Hardcoded insurer/tier/exclusion/waiting data."""
from __future__ import annotations

import sqlite3

INSURERS = [
    ("allianz", "Allianz Care Australia", "1800 651 060", "https://www.allianzcare.com.au"),
    ("bupa", "Bupa Australia", "134 135", "https://www.bupa.com.au"),
    ("cbhs", "CBHS International Health", "1300 174 226", "https://www.cbhsinternationalhealth.com.au"),
    ("medibank", "Medibank Private", "134 148", "https://www.medibank.com.au"),
    ("ahm", "ahm OSHC", "134 148", "https://ahm.com.au"),
    ("nib", "nib OSHC", "1800 783 685", "https://www.nib.com.au"),
]

# (tier_id, insurer_id, tier_name, gp%, spec%, in_hosp%, priv_uncon%,
#  pharma_max, pharma_single, pharma_family, copay_type, copay_amt,
#  has_repat, repat_lim, has_mh, mh_annual, has_boarder, boarder_lim,
#  has_extras, has_online_doc, ed_fee, waived_psych)
TIERS = [
    ("allianz_essentials", "allianz", "Essentials", 100, 85, 100, None,
     50, 500, 1000, "pbs_copay", None, 0, None, 0, None, 0, None, 0, 0, None, 0),
    ("allianz_standard", "allianz", "Standard", 100, 85, 100, None,
     50, 500, 1000, "pbs_copay", None, 1, 100000, 0, None, 0, None, 0, 0, None, 0),
    ("bupa_oshc", "bupa", "OSHC", 100, 100, 100, None,
     50, 500, 1000, "pbs_copay", None, 0, None, 0, None, 0, None, 1, 0, None, 1),
    ("cbhs_standard", "cbhs", "Standard", 100, 100, 100, None,
     50, 300, 600, "pbs_copay", None, 0, None, 0, None, 0, None, 0, 1, 160, 0),
    ("cbhs_essentials", "cbhs", "Essentials", 85, 85, 100, None,
     50, 500, 1000, "pbs_copay", None, 0, None, 0, None, 0, None, 0, 0, None, 0),
    ("medibank_essentials", "medibank", "Essentials", 100, 85, 100, None,
     70, 500, 1000, "flat_30", 30, 0, None, 0, None, 0, None, 0, 0, None, 0),
    ("medibank_comprehensive", "medibank", "Comprehensive", 100, 85, 100, None,
     None, 1000, 2000, "flat_30", 30, 1, 100000, 1, 200, 1, 150, 0, 0, None, 0),
    ("ahm_oshc", "ahm", "OSHC", 100, 85, 100, None,
     50, 500, 1000, "pbs_copay", None, 0, None, 0, None, 0, None, 0, 0, None, 0),
    ("nib_oshc_core", "nib", "OSHC Core", 100, 85, 100, None,
     50, 500, 1000, "pbs_copay", None, 0, None, 0, None, 0, None, 0, 0, None, 0),
]

DEED_EXCLUSIONS = [
    "Treatment outside Australia (unless medical repatriation)",
    "Compensable injury/illness (workers comp, motor vehicle)",
    "Treatment that is not medically necessary",
]

INSURER_EXCLUSIONS = [
    # These are the service-level exclusions checked by the coverage calculator.
    # "Dental/optical/physio unless MBS-listed" is intentionally absent:
    # non-MBS services are not in our DB; MBS-listed ones are covered per deed.
    "Cosmetic surgery / elective cosmetic",
    "Assisted reproductive services / IVF",
    "Pre-arranged treatment before arrival in Australia",
    "Non-PBS medications and over-the-counter drugs",
    "Transportation into or out of Australia (except medical repatriation where applicable)",
]

# (condition_type, waiting_months, notes)
DEFAULT_WAITING = [
    ("pre_existing_non_psych", 12, None),
    ("pre_existing_psychiatric", 2, None),
    ("pregnancy", 12, "OSHC policy < 2 years"),
    ("psychiatric_hospital", 2, None),
    ("general_hospital", 2, None),
    ("gp_outpatient", 0, "MBS Groups A1, A2, A7(2,10), A22, A23, A40(1,2), A46"),
    ("ambulance", 0, "Emergency"),
    ("pharmaceutical", 0, "Most insurers waive deed's 2-month default"),
]

BUPA_WAITING_OVERRIDES = [
    ("pre_existing_psychiatric", 0, "Waived until further notice"),
    ("general_hospital", 0, "Non pre-existing"),
]


def seed_all(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT OR REPLACE INTO insurers VALUES (?,?,?,?)",
        INSURERS,
    )
    conn.executemany(
        """INSERT OR REPLACE INTO insurer_tiers VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )""",
        TIERS,
    )
    # exclusions: deed (3) + insurer-specific (6) for every tier
    conn.execute("DELETE FROM insurer_exclusions")
    for tier in TIERS:
        tier_id = tier[0]
        for desc in DEED_EXCLUSIONS:
            conn.execute(
                "INSERT INTO insurer_exclusions (tier_id, exclusion_desc, is_deed_exclusion) VALUES (?,?,1)",
                (tier_id, desc),
            )
        for desc in INSURER_EXCLUSIONS:
            conn.execute(
                "INSERT INTO insurer_exclusions (tier_id, exclusion_desc, is_deed_exclusion) VALUES (?,?,0)",
                (tier_id, desc),
            )
    # waiting periods
    conn.execute("DELETE FROM insurer_waiting_periods")
    for tier in TIERS:
        tier_id = tier[0]
        for cond, months, notes in DEFAULT_WAITING:
            conn.execute(
                "INSERT INTO insurer_waiting_periods (tier_id, condition_type, waiting_months, notes) VALUES (?,?,?,?)",
                (tier_id, cond, months, notes),
            )
    # Bupa overrides
    for cond, months, notes in BUPA_WAITING_OVERRIDES:
        conn.execute(
            """UPDATE insurer_waiting_periods
            SET waiting_months = ?, notes = ?
            WHERE tier_id = 'bupa_oshc' AND condition_type = ?""",
            (months, notes, cond),
        )
