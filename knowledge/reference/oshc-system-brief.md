# OSHC System Brief — How Overseas Student Health Cover Works

> Source: OSHC Deed for the Provision of Overseas Student Health Cover (1 July 2025), Medicare Benefits Schedule (MBS) XML March 2026, MBS IMAP Mapping File March 2026.

---

## 1. What is OSHC?

Overseas Student Health Cover (OSHC) is a mandatory private health insurance product for international students studying in Australia on a Student Visa (subclass 500). It is regulated by the Australian Government Department of Health and Aged Care.

OSHC provides cover for:
- Out-of-hospital medical treatment (GP visits, specialist consultations, pathology, radiology)
- In-hospital medical treatment (surgeon fees, anaesthetist fees, hospital accommodation)
- Prescription medicines listed on the Pharmaceutical Benefits Scheme (PBS)
- Surgically implanted prostheses and medical devices
- Emergency ambulance transport

OSHC does NOT replace Medicare. Most international students are not eligible for Medicare (Australia's public health insurance for citizens and permanent residents). OSHC fills this gap.

### Legal Requirement

Under Student Visa condition 8501, all holders of a Student Visa must maintain adequate health insurance (OSHC) for the entire duration of their visa. Failure to maintain OSHC may result in visa cancellation. OSHC providers may notify the Department of Home Affairs if a student cancels or lapses their policy.

### Who Can Be Covered

| Cover Type | Who Is Covered |
|------------|---------------|
| Single | Primary Student Visa holder only |
| Couple (Dual Family) | Student + partner listed on student visa |
| Family (Multi Family) | Student + partner + dependant children under 18, listed on student visa |
| Sole Parent | Student + dependant children under 18, listed on student visa |

Extended family members (parents, siblings, aunts, uncles) cannot be covered under OSHC.

Dependants receive the same level of cover as the primary student (Deed Clause 3.6c).

---

## 2. The OSHC Deed

The OSHC Deed is a legally binding agreement between the Australian Government (Department of Health and Aged Care) and each approved OSHC insurer. It sets the **minimum** standards that all OSHC products must meet.

**Current Deed Term**: 1 July 2025 to 30 June 2028 (extendable to 30 June 2029)

There are six approved OSHC providers, all bound by the same deed:
1. Allianz Care Australia (underwritten by Peoplecare Health Limited)
2. Bupa Australia (Bupa HI Pty Ltd)
3. CBHS International Health (CBHS Corporate Health Pty Ltd)
4. Medibank Private (Medibank Private Limited)
5. ahm OSHC (a business of Medibank Private Limited)
6. nib OSHC (nib Health Funds Limited)

### Key Deed Provisions

- **No excess** allowed on any OSHC product (Clause 8.3) — unlike regular Australian private health insurance, OSHC cannot charge an excess/co-payment for hospital admissions
- **Maximum 12% discount** on first purchase only (Clause 8.2)
- **National coverage** across all States and Territories (Clause 3.6a)
- **Benefits cannot exceed actual costs** incurred (Clause 3.6d) — insurer never pays more than the student actually spent
- **Continuous cover** required for Student Visa validity — any gap must be paid back before claims can be made for new periods

### Deed Schedules

The deed contains five schedules that define the coverage framework:

| Schedule | Content |
|----------|---------|
| Schedule 1 | Base coverage rates (mandatory minimum benefits) |
| Schedule 2 | Additional coverage (optional, insurer may offer above minimum) |
| Schedule 3 | Exclusions (only 3 exclusions in the deed) |
| Schedule 4 | Waiting periods |
| Schedule 5 | Premium refund scenarios |

---

## 3. The Medicare Benefits Schedule (MBS)

The MBS is the Australian Government's list of medical services and their associated fees. It is the foundation for all OSHC benefit calculations.

### What the MBS Contains

- **~6,000+ active medical service items**, each with a unique item number (e.g., Item 23 = GP Level B consultation)
- **Schedule Fee**: the government-determined "standard fee" for each service (e.g., $43.90 for Item 23)
- **Benefit amounts**: pre-calculated benefit amounts at 100%, 85%, and 75% of the schedule fee
- **Benefit Type** (A through E): determines which benefit rate applies
- **Category, Group, Sub-group codes**: hierarchical classification of services

### MBS Benefit Types

| Type | Meaning | Benefit Rates Available |
|------|---------|----------------------|
| A | Anaesthesia items (basic units) | Calculated from basic units |
| B | 85% benefit only (some telehealth, allied health) | 85% only |
| C | Standard specialist items | 75% (in-hospital) + 85% (out-of-hospital) |
| D | Derived fee items (fee calculated from formula) | Varies |
| E | GP/bulk-billed items | 100% only |

### MBS Categories

| Code | Category |
|------|----------|
| 01 | Professional Attendances (GP visits, specialist consultations) |
| 02 | Diagnostic Procedures |
| 03 | Therapeutic Procedures (surgery, operations) |
| 04 | Oral and Maxillofacial Services |
| 05 | Diagnostic Imaging Services (X-ray, MRI, CT, ultrasound) |
| 06 | Pathology Services (blood tests, biopsies) |
| 07 | Cleft Lip and Cleft Palate Services |
| 08 | Miscellaneous Services |

### MBS Groups (Selected Key Groups)

| Group | Description | Relevance to OSHC |
|-------|-------------|-------------------|
| A1 | General Practitioner Attendances | Nil waiting period (Deed Schedule 4) |
| A2 | Other Non-Referred Attendances | Nil waiting period |
| A7 (sub 2, 10) | Selected attendance sub-groups | Nil waiting period |
| A22 | GP After-Hours Attendances | Nil waiting period |
| A23 | GP Telehealth Attendances | Nil waiting period |
| A40 (sub 1, 2) | Selected allied health sub-groups | Nil waiting period |
| A46 | Practice Nurse items | Nil waiting period |

### BTOS (Broad Type of Service)

The IMAP mapping file classifies all MBS items into 17 Broad Types of Service:

- Non-referred attendances (GP/VR GP, Other, Enhanced Primary Care, Practice Nurse)
- Specialist attendances
- Obstetrics
- Anaesthetics
- Assistance at Operations
- Operations
- Diagnostic Imaging
- Pathology (Collection + Tests)
- Radiotherapy
- Optometry
- Other Allied Health
- Other MBS services

---

## 4. Coverage Rates — How OSHC Pays

### Base Coverage (Deed Schedule 1 — Mandatory Minimum)

Every OSHC product must provide at least these benefits:

#### Out-of-Hospital Medical Services

**Deed minimum: 85% of the MBS Schedule Fee for ALL out-of-hospital services.**

The deed itself makes NO distinction between GP and specialist services — 85% applies uniformly to all out-of-hospital medical services.

However, in practice, **most insurers voluntarily exceed this minimum for GP visits**, paying 100% of the MBS fee for GP consultations. This is an insurer-specific enhancement, not a deed requirement. The one exception is CBHS Essentials, which pays only the deed minimum of 85% for all services including GP.

#### In-Hospital Medical Services

**100% of the MBS Schedule Fee** for all medical services provided during a hospital admission (surgeon fees, anaesthetist fees, in-hospital consultations, etc.). This is universal across all insurers and tiers.

#### Public Hospital

**100% of charges** as determined by State and Territory health authorities for:
- Shared ward accommodation (overnight and same-day)
- Hospital same-day services
- Operating theatre, intensive care, labour ward fees
- Accident and emergency department services
- Outpatient medical services
- Post-operative services

#### Private Hospital (Agreement/Contracted)

**100% of contracted charges** at hospitals where the insurer has an agreement. This covers:
- Shared ward accommodation (minimum)
- Operating theatre fees
- Intensive care and labour ward fees
- Supplied pharmaceuticals (PBS-listed, for the condition being treated)
- Allied health services provided as part of inpatient treatment
- Private room where available (varies by insurer)

#### Private Hospital (Non-Agreement/Non-Contracted)

**Minimum benefit** as set out in the Private Health Insurance (Benefit Requirements) Rules 2011. This typically results in **significant out-of-pocket expenses** for the student.

#### Ambulance

**100% of the ambulance charge** when transport is:
- Medically necessary for admission to hospital, OR
- Required for emergency treatment

Only covers ambulance provided by or under arrangement with an approved State/Territory ambulance service. Does NOT cover non-emergency transfers between hospitals.

#### Prostheses and Medical Devices

**100% of the benefit** as listed in the Australian Government's Prescribed List of Medical Devices and Human Tissue Products (no gap for "no gap" items, gap permitted for "gap permitted" items).

#### Prescription Medicines (Pharmaceuticals)

The deed sets minimum pharmaceutical benefits:

| Parameter | Deed Minimum |
|-----------|-------------|
| Co-payment | Student pays the PBS patient contribution for general beneficiaries first |
| Maximum benefit per item | Up to $50 above the PBS co-payment |
| Annual limit (Single) | Minimum $500 per calendar year |
| Annual limit (Family/Couple) | Minimum $1,000 per calendar year |

Only PBS-listed prescription medicines are covered. Non-PBS medications, over-the-counter medicines, vitamins, and herbal medicines are NOT covered.

**Important**: Students requiring high-cost pharmaceuticals (e.g., oncology/cancer treatment drugs) may face significant out-of-pocket expenses even with OSHC cover, as the per-item and annual limits may be insufficient.

---

## 5. How Out-of-Pocket / Gap Costs Are Calculated

A student's out-of-pocket cost depends on three factors:
1. **What the doctor actually charges** (may be above MBS fee)
2. **What the MBS schedule fee is** for that service
3. **What percentage the OSHC insurer pays** of the MBS fee

### Formula

```
Out-of-Pocket = Doctor's Actual Charge - OSHC Benefit Paid

Where:
  OSHC Benefit Paid = MBS Schedule Fee x Benefit Percentage (from insurer tier)
  
  But: OSHC Benefit Paid can NEVER exceed Doctor's Actual Charge (Deed Clause 3.6d)
```

### Scenario 1: GP Visit (Out-of-Hospital) — Doctor Charges at MBS Fee

```
MBS Item 23 (Level B GP consultation):
  Schedule Fee = $43.90
  Doctor charges = $43.90 (bulk-bill equivalent)
  
  Most insurers (100% GP rate):
    OSHC pays = $43.90 x 100% = $43.90
    Out-of-pocket = $43.90 - $43.90 = $0.00
    
  CBHS Essentials (85% rate):
    OSHC pays = $43.90 x 85% = $37.32
    Out-of-pocket = $43.90 - $37.32 = $6.59
```

### Scenario 2: GP Visit — Doctor Charges ABOVE MBS Fee

```
MBS Item 23:
  Schedule Fee = $43.90
  Doctor charges = $85.00 (private billing)
  
  Most insurers (100% GP rate):
    OSHC pays = $43.90 x 100% = $43.90
    Out-of-pocket = $85.00 - $43.90 = $41.10
```

### Scenario 3: Specialist Visit (Out-of-Hospital)

```
MBS Item 104 (Specialist consultation):
  Schedule Fee = $101.35
  Doctor charges = $250.00
  
  Most insurers (85% specialist rate):
    OSHC pays = $101.35 x 85% = $86.15
    Out-of-pocket = $250.00 - $86.15 = $163.85
    
  CBHS Standard (100% specialist rate — unique):
    OSHC pays = $101.35 x 100% = $101.35
    Out-of-pocket = $250.00 - $101.35 = $148.65
```

### Scenario 4: In-Hospital Surgery

```
MBS Item 30001 (some surgical procedure):
  Schedule Fee = $500.00
  Surgeon charges = $1,200.00
  
  All insurers (100% in-hospital rate):
    OSHC pays = $500.00 x 100% = $500.00
    Out-of-pocket on surgeon fees = $1,200.00 - $500.00 = $700.00
    
  PLUS: Hospital accommodation, theatre fees, anaesthetist, etc.
  (covered separately if agreement hospital; may have gaps at non-agreement)
```

### Key Points About Gap Costs

1. **OSHC only covers up to the MBS fee** (at the applicable percentage). Any amount the doctor charges above the MBS fee is the student's gap.
2. **Public hospital**: Generally no gap if treated as a public patient in shared ward. Doctors are hospital-nominated.
3. **Agreement private hospital**: Hospital charges covered. Doctor may still charge above MBS fee (gap).
4. **Non-agreement private hospital**: Student may face large gaps on both hospital charges AND doctor fees.
5. **Bulk-billing doctors** charge exactly the MBS fee — no gap for students whose insurer pays 100% for that service type.
6. **Some insurers offer gap schemes** (e.g., Bupa Medical Gap Scheme) where participating doctors agree to limit their charges.

---

## 6. Waiting Periods (Deed Schedule 4)

Waiting periods are times when the student cannot claim benefits for certain services. They start from the later of:
- The date the student arrives in Australia on a Student Visa, OR
- The date the OSHC policy commenced

### Deed-Mandated Waiting Periods

| Service Type | Waiting Period | How Determined |
|-------------|---------------|----------------|
| Out-of-hospital services in MBS Groups A1, A2, A7 (sub 2, 10), A22, A23, A40 (sub 1, 2), A46 | **Nil** | By MBS group_code of the item |
| Emergency treatment | **Nil** | By clinical assessment (8 qualifying conditions) |
| Pre-existing psychiatric conditions (hospital treatment) | **2 months** | Medical practitioner assessment |
| Pre-existing conditions (all other hospital treatment) | **12 months** | Medical practitioner assessment |
| Pregnancy and birth (OSHC policy < 2 years, after premium change post 1 Jul 2025) | **12 months** | Policy duration check |
| Pregnancy and birth (OSHC policy >= 2 years, after premium change post 1 Jul 2025) | **Nil** | Policy duration check |
| All other Schedule 1 services not listed above | **2 months** | Default |
| Waiting period from previous OSHC provider | **Credited** | If continuous cover maintained |

### Pre-Existing Condition Definition

A person has a pre-existing condition if:
1. They have an ailment, illness, or condition; AND
2. In the opinion of a medical practitioner appointed by the insurer, the signs or symptoms of that condition existed at any time in the **6-month period** ending on the day the person became insured

### Emergency Treatment Definition

Emergency treatment applies to any of these 8 conditions (no waiting period):
1. Risk of serious morbidity or mortality requiring urgent assessment and resuscitation
2. Suspected acute organ or system failure
3. Illness/injury where viability or function of a body part/organ is acutely threatened
4. Drug overdose, toxic substance or toxin effect
5. Psychiatric disturbance where patient or others are at immediate risk
6. Severe pain where viability/function of a body part/organ is suspected to be acutely threatened
7. Acute haemorrhaging requiring urgent assessment and treatment
8. Condition requiring immediate admission to avoid imminent morbidity/mortality where transfer to another facility is impractical

### Insurer-Specific Overrides

Insurers may waive or reduce waiting periods beyond the deed minimum:
- **Bupa**: Has waived the 2-month psychiatric pre-existing condition waiting period "until further notice"
- **Medibank (both tiers)**: Nil waiting for hospital psychiatric services (including pre-existing)
- **Most insurers**: Nil waiting for prescription medicines (deed allows up to 2 months)

---

## 7. Exclusions

### Deed Exclusions (Schedule 3 — Only 3)

The deed itself only mandates three exclusions:

1. **Treatment outside Australia** — except medical repatriation where offered under Schedule 2
2. **Compensable injury/illness** — where medical expenses are for an injury/illness covered by workers compensation, motor vehicle accident insurance, or any other compensation scheme
3. **Treatment that is not medically necessary** — includes elective cosmetic surgery

### Common Insurer-Specific Exclusions (Beyond Deed)

Most insurers add these exclusions:
- Assisted reproductive services (IVF, etc.)
- Treatment arranged before the student arrived in Australia
- Transportation of student/dependants into or out of Australia (except medical repatriation where offered)
- Dental, optical, physiotherapy, chiropractic, and other extras/ancillary services (unless the service has an MBS item number or is provided as part of a hospital admission)
- Non-PBS medications, experimental drugs, over-the-counter medicines
- Cosmetic surgery (explicitly listed beyond the deed's "not medically necessary" exclusion)
- Laser eye surgery
- Services not recognised by Medicare / not attracting MBS item numbers
- Cost of medical examinations required for visa applications

---

## 8. Additional Coverage (Deed Schedule 2)

Schedule 2 allows insurers to **optionally** offer coverage above the base minimum. These are not required but some insurers provide them as competitive differentiators:

| Additional Service | Deed Provision | Which Insurers Offer It |
|-------------------|----------------|------------------------|
| General treatment (dental, optical, physio, etc.) | Rate set by insurer | Bupa (separate Extras add-on purchase) |
| Assisted reproductive services | At Schedule 1 rates if offered | None currently include |
| Pre-arranged services (before OSHC start) | At Schedule 1 rates if offered | None currently include |
| Medical repatriation to home country | Rate set by insurer | Allianz (both tiers, $100k), Medibank Comprehensive ($100k) |

---

## 9. Premium Refunds (Deed Schedule 5)

Students can receive pro-rata premium refunds (less reasonable processing fee) in these 9 scenarios:

| # | Scenario | Refund Type |
|---|----------|-------------|
| 1 | Failed to arrive in Australia at all | Full refund |
| 2 | Delayed arrival | Pro-rata for delay period |
| 3 | Visa refused by Home Affairs | Full refund |
| 4 | Visa extension refused | Full refund of extension premium |
| 5 | Required to cease studies and leave early (beyond student's control) | Pro-rata for remaining period |
| 6 | Granted permanent residency or non-student visa | Pro-rata for remaining period |
| 7 | Not residing in Australia for 3+ continuous months while holding valid student visa | Pro-rata for absence period |
| 8 | Overlapping OSHC with another insurer | Pro-rata for overlap period |
| 9 | Administrative changes adjusting OSHC period beyond visa dates | Excess premium refunded |

Refunds are calculated on a monthly pro-rata basis. Most insurers will not pay a refund if the unexpired portion is less than 30 days.

---

## 10. How Claims Work

### Out-of-Hospital Claims

1. Student visits doctor/specialist/pathology/radiology
2. If doctor direct-bills the insurer: student shows membership card, insurer-covered portion is billed directly, student pays any gap
3. If doctor does NOT direct-bill: student pays full amount, submits claim to insurer (via app, online portal, or email), receives reimbursement of the covered portion to their Australian bank account

### In-Hospital Claims

1. Student should contact insurer BEFORE planned hospital admission to confirm coverage and any potential out-of-pocket costs
2. For agreement/contracted hospitals: insurer pays hospital directly for covered charges
3. For non-agreement hospitals: student may need to pay and claim, with significantly lower benefits
4. For public hospitals: insurer pays the gazetted rate directly

### Pharmaceutical Claims

1. Student takes prescription to pharmacy
2. Student pays full cost of the medicine
3. Student claims the amount exceeding the PBS co-payment from the insurer (up to per-item and annual limits)

---

## 11. Transferring Between OSHC Providers

Students can transfer between OSHC providers without losing waiting period credit, provided:
- There is **no gap** between the end date of the previous policy and the start date of the new policy (continuous cover)
- The student obtains a clearance certificate from the previous provider
- Any waiting periods already served with the previous provider are credited toward the new policy

If upgrading to a higher tier, waiting periods may apply to services not previously included in the old cover.

---

## 12. Key Cost Calculation Rules for MediBridge System

### Determining GP vs Specialist

The system must determine whether an MBS item is a "GP item" or a "specialist item" to apply the correct insurer-specific benefit rate:

1. **BenefitType = E**: Item only has 100% benefit → GP/bulk-billed item
2. **MBS Group A1**: General Practitioner Attendances → GP item
3. **BenefitType = C**: Item has both 75% and 85% benefits → specialist item
4. **All other items**: Treated as specialist/other (85% rate applies for most insurers)

### Applying Insurer-Tier-Specific Rates

```
IF setting = "in_hospital":
    benefit = schedule_fee × 100%  (all insurers, all tiers)
    
ELIF setting = "out_of_hospital":
    IF is_gp_item:
        benefit = schedule_fee × tier.gp_benefit_pct  
        (100% for most, 85% for CBHS Essentials)
    ELSE:
        benefit = schedule_fee × tier.specialist_benefit_pct  
        (85% for most, 100% for CBHS Standard)
        
ELIF setting = "public_hospital":
    benefit = actual_charges × 100%  (gazetted rate)
    
ELIF setting = "ambulance":
    IF medically_necessary:
        benefit = ambulance_charge × 100%
```

### Pharmaceutical Calculation

```
IF medicine is PBS-listed:
    student_pays_first = current_PBS_copayment_for_general_beneficiaries
    
    remaining = medicine_cost - student_pays_first
    
    IF remaining > 0:
        IF tier.pharma_copayment_type == "flat":
            student_contribution = tier.pharma_copayment_amount  (e.g., $30 for Medibank)
            reimbursable = remaining - student_contribution
        ELSE:  # PBS co-pay type
            reimbursable = remaining
            
        benefit = MIN(reimbursable, tier.pharma_max_per_item)
        
        # Check annual limit
        IF benefits_paid_this_year + benefit > tier.pharma_annual_limit:
            benefit = MAX(0, tier.pharma_annual_limit - benefits_paid_this_year)
```

### Waiting Period Check

```
months_since_policy_start = (today - policy_start_date).months

lookup item.group_code in MBS database

IF group_code IN [A1, A2, A7_sub2, A7_sub10, A22, A23, A40_sub1, A40_sub2, A46]:
    waiting = 0  # Nil
ELIF is_emergency_treatment:
    waiting = 0  # Nil
ELIF is_pre_existing AND is_psychiatric:
    IF tier.waived_psychiatric_waiting:
        waiting = 0  # Bupa waiver
    ELSE:
        waiting = 2  # months
ELIF is_pre_existing:
    waiting = 12  # months
ELIF is_pregnancy:
    IF policy_duration >= 24 months AND post_premium_change:
        waiting = 0  # Nil
    ELSE:
        waiting = 12  # months
ELSE:
    waiting = tier_specific_general_waiting  # 2 months default, some insurers 0

IF months_since_policy_start >= waiting:
    status = "Waiting period served"
ELSE:
    remaining = waiting - months_since_policy_start
    status = f"{remaining} months remaining"
```
