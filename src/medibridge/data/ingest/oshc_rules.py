"""Hardcoded deed-rule seed for oshc_coverage_rules table."""
from __future__ import annotations

import sqlite3

DEED_RULES = [
    ("benefit_rate", "out_of_hospital", None, 85.0, None, None, None,
     "Out-of-hospital medical: 85% of MBS schedule fee", "Schedule 1c"),
    ("benefit_rate", "in_hospital", None, 100.0, None, None, None,
     "In-hospital medical: 100% of MBS schedule fee", "Schedule 1d"),
    ("benefit_rate", "public_hospital", None, 100.0, None, None, None,
     "Public hospital: 100% of charges", "Schedule 1f"),
    ("benefit_rate", "ambulance", None, 100.0, None, None, None,
     "Ambulance: 100% of charge when medically necessary", "Schedule 1a"),
    ("waiting_period", None, None, None, None, None, 0,
     "Nil waiting: out-of-hospital MBS groups A1, A2, A7(2,10), A22, A23, A40(1,2), A46", "Schedule 4"),
    ("waiting_period", None, None, None, None, None, 0,
     "Nil waiting: emergency treatment", "Schedule 4"),
    ("waiting_period", None, "psychiatric", None, None, None, 2,
     "2 months: psychiatric hospital treatment (non-emergency)", "Schedule 4"),
    ("waiting_period", None, "pre_existing", None, None, None, 12,
     "12 months: pre-existing condition hospital treatment", "Schedule 4"),
    ("waiting_period", None, "pregnancy", None, None, None, 12,
     "12 months: pregnancy (OSHC < 2 years)", "Schedule 4"),
    ("waiting_period", None, "general", None, None, None, 2,
     "2 months: all other Schedule 1 services", "Schedule 4"),
    ("exclusion", None, None, None, None, None, None,
     "Treatment outside Australia (unless medical repatriation)", "Schedule 3"),
    ("exclusion", None, None, None, None, None, None,
     "Compensable injury/illness (workers comp, motor vehicle)", "Schedule 3"),
    ("exclusion", None, None, None, None, None, None,
     "Treatment that is not medically necessary", "Schedule 3"),
    ("limit", None, "pharmaceutical", None, None, None, None,
     "Pharmaceutical: PBS co-payment excess, up to $50/item, min $500/yr single $1000/yr family", "Schedule 1b"),
]


def insert_deed_rules(conn: sqlite3.Connection) -> int:
    cur = conn.executemany(
        """INSERT INTO oshc_coverage_rules
        (rule_type, setting, provider_type, benefit_pct, category_code, btos_code,
         waiting_months, description, deed_reference)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        DEED_RULES,
    )
    return cur.rowcount
