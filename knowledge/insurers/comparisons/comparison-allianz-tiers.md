# Allianz Care Australia — Tier Comparison: Essentials vs Standard

> This document compares the two OSHC tiers offered by Allianz Care Australia.

---

## Overview

Allianz offers two OSHC tiers that are **functionally identical** in all measurable benefits. The distinction is primarily in product naming and market positioning. There is no material difference in coverage, limits, waiting periods, or exclusions.

---

## Side-by-Side Comparison

### Medical Benefits

| Feature | Essentials | Standard | Difference |
|---------|-----------|----------|------------|
| GP benefit (out-of-hospital) | 100% MBS | 100% MBS | None |
| Specialist benefit (out-of-hospital) | 85% MBS | 85% MBS | None |
| Pathology (out-of-hospital) | 85% MBS | 85% MBS | None |
| Radiology (out-of-hospital) | 85% MBS | 85% MBS | None |
| In-hospital medical | 100% MBS | 100% MBS | None |
| Public hospital | 100% charges | 100% charges | None |

### Pharmaceutical Benefits

| Feature | Essentials | Standard | Difference |
|---------|-----------|----------|------------|
| Co-payment | PBS co-pay | PBS co-pay | None |
| Max per item | $50 | $50 | None |
| Annual limit (Single) | $500 | $500 | None |
| Annual limit (Family) | $1,000 | $1,000 | None |

### Additional Features

| Feature | Essentials | Standard | Difference |
|---------|-----------|----------|------------|
| Medical repatriation | $100,000 | $100,000 | None |
| 24/7 helpline | Yes | Yes | None |
| Allianz MyHealth app | Yes | Yes | None |
| Direct billing | Yes | Yes | None |
| No excess | Yes | Yes | None |

### Waiting Periods

| Condition | Essentials | Standard | Difference |
|-----------|-----------|----------|------------|
| GP services | Nil | Nil | None |
| Emergency | Nil | Nil | None |
| Psychiatric | Nil | Nil | None |
| Pre-existing | 12 months | 12 months | None |
| Other | — | — | None |

### Exclusions

Identical exclusion lists.

---

## Summary

**Both Allianz OSHC tiers provide identical coverage.** There is no cost calculation difference between Essentials and Standard. For system implementation purposes, they can share the same benefit rate configuration with only the tier name differing.

The only potential difference may be in premium pricing — students should compare current premiums for both tiers on the Allianz website as pricing may vary by tier even though benefits are identical.

---

## System Implementation Note

Since both tiers are functionally identical:
- Same `gp_benefit_pct` (100), `specialist_benefit_pct` (85), `in_hospital_benefit_pct` (100)
- Same pharma limits ($50/item, $500/$1,000 annual)
- Same repatriation limit ($100,000)
- Same waiting periods
- Same exclusions
- Two separate `tier_id` entries ("allianz_essentials", "allianz_standard") mapping to identical benefit parameters
