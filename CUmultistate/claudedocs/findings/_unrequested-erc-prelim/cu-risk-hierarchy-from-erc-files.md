# Findings 02 — Commercial Umbrella (CU) risk hierarchy

**Sources read:**
- Guide: `ISO ERC Suite Product Guide` pp.5, 20-22, 44-49, 72-83 (diagrams viewed as images, not text).
- Data: `CUP Batch 1 ERC Files` — CW and AK packages (12/01/2020 V01):
  - `DS-CU-{CW,AK}-...xml` (table tree)
  - `RC-CU-{CW,AK}-...xml` (`Forms` element = pages tree)
- Extraction scripts: `claudedocs/scripts/cu_pages.py`, `cu_form_occ.py`.

**Not read yet:** ALG (form logic, coverage-on-policy indicator), page fields, TC file, DOC file, RCRN. The coverage-to-risk relationship below is therefore from DS only.

## 1. Answer: CU hierarchy is FLAT (2 levels), unlike GL

| LOB | Hierarchy [guide diagram] | Depth |
|---|---|---|
| GL (p.82) | Policy → **Location** → **Classification** (each with Forms/Coverages; forms have Schedules/Coverages) | 3 |
| BOP (p.73) | Policy → Location → Building → Classification | 4 |
| **CU (p.79 + DS + RC)** | **Policy → {risk groups} — no nesting** | **2** |

No risk sits inside another risk in CU. Verified in DS: all 14 risk tables are direct children of `CommercialUmbrella`, and their only children are `system` tables (Note, Company, Address, Human). No risk has a coverage, form, or schedule child.

## 2. CU tree (DS, identical in CW and AK)

```
CommercialUmbrella  [policy]  134 columns
├─ Coverages (8, policy-level only)
│    1stMillionCoverage, 2ndMillionCoverage, 3rdMillionCoverage, 4thMillionCoverage,
│    5thMillionCoverage, ExcessLiabilityCoverage, CommissionAdjustmentCoverage,
│    PolicyMinimumPremiumCoverage
├─ Forms (453 DS form tables; 255 form pages in CW RC)
│    └─ 64 forms have a 1:1 "...Detail" schedule child (the 64 schedule tables)
│    └─ 6 forms have a system child (not analysed)
├─ Risk groups (11 underwriting-type, direct children)
│    AircraftLiability(46 cols)  AutoDealers(49)  BOP(59)  CommercialAuto(70)
│    EmployersLiability(49)  Garage(49)  GeneralLiability(65)  Liquor(47)
│    OtherLiability(50)  UnderlyingLiability(40)  Watercraft(46)
├─ System risks (3, not ISO content)
│    ElectronicSignature(46)  Payments(98; Address, Company x2, Human, Note)  QuoteLetter(51)
└─ Note [system]
```
11 + 3 = 14 risk tables, matching the DS count.

## 3. Page tree (RC `Forms`, CW) — what the screen actually shows

```
Policy Detail  (CommercialUmbrella, occ 0/1)
├─ [Summary → Detail] per risk group  (list page → entry page)
│    Aircraft Liability   0/999      Auto Dealers      0/1
│    BOP                  0/999      Commercial Auto   0/999
│    Employers Liability  0/999      General Liability 0/999
│    Liquor               0/999      Other Liability   0/999
│    Watercraft           0/999
└─ Form pages (255): each Form → Summary → Detail (schedule) where a schedule exists
```
- Risk entry = **Summary** page (repeating list, `0/999`) + **Detail** page (`0/1`, one occurrence).
- Counts in CW: Detail 64, Summary 63, Form 255.
- AK RC is exceptions only: **one** page, form "Alaska Changes - Attorney's Fees" (flag A). Alaska adds no risk pages.

## 4. Occurrence/attachment pattern on CW pages
| Count | Page type | Min/Max | Condition | AttachmentCondition | Reading |
|---|---|---|---|---|---|
| 25 | Form | 0/0 | no | **yes** | Conditional forms (attached by logic, matches guide p.47) |
| 226 | Form | 0/1 | **yes** | no | Optional forms with an eligibility Condition |
| 4 | Form | 0/1 | no | no | Optional, unconditional |
| 64 | Detail | 0/1 | no | no | One detail per summary |
| 40 | Summary | 1/99 | no | no | Form schedule lists |
| 15 | Summary | 0/1 | no | no | Single-occurrence summary |
| 8 | Summary | 0/999 | no | no | Repeating risk lists |

No Mandatory forms (1/1) in CW CU. Not checked for state packages beyond AK.

## 5. Discrepancies to resolve (guide vs data)
1. **Garage:** guide p.79 lists Garage; DS has `CommercialUmbrellaGarage`; but the CW RC page tree has **no Garage page** (searched page names/tables for "Garage": not found in the CW `Forms` tree).
2. **Auto Dealers, Other Liability:** present in DS and CW RC pages; **not** in the guide's p.79 diagram. Guide edition is Oct 2019, content is 12/2020 — **[INFERENCE]** the guide diagram is out of date.
3. **UnderlyingLiability:** in DS but no page found in CW RC pages. **[INFERENCE]** likely a data-only table; verify in ALG / page fields.
4. **Optional form occurrence:** guide p.47 says Optional = Min 0 / Max >99; CU CW data shows optional forms at **0/1**. Treat the data as authoritative for CU.
5. **Guide says Summary pages "can be ignored" (p.45):** true for form summaries, but for CU risk groups the Summary page is the repeating list (0/999), so it is not ignorable in a screen build.
6. Guide p.79 diagram shows 8 risk groups; data shows 11 groups (9 with pages).

## 6. Screen implications (CU)
- Screen structure: Policy Detail page, then one list+detail pair per underlying-insurance type (9 with pages), plus form/schedule pages.
- No Location/Building/Classification screens exist for CU. Do not copy a GL layout.
- Coverages are all policy-level: the layered million coverages (1st–5th million), excess liability, commission adjustment, policy minimum premium. **[INFERENCE]** these drive an "Limits / Premium" area on Policy Detail, not on the risk screens.
- Risk groups look like **scheduled underlying insurance** by type (aircraft, auto, GL, EL, liquor, watercraft…). **[INFERENCE]** — confirm from page fields (columns like carrier / limit / policy number).

## 7. Next to confirm
- Page Fields (labels, types, required/conditions) for Policy Detail and each risk Detail.
- ALG Coverage-on-Policy indicator and Flowchart for CU, to see what the coverages depend on.
- Why Garage/UnderlyingLiability lack pages.
- Whether other states (not in this batch) add risk pages.
