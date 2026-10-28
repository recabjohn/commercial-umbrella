# Findings 06 - full FRC sheet review (Page / Page Fields / Domain) and other ERC sheets

Source: `FRC-CU-{AK,CW}-12012020-V01.xlsx` read straight from the workbook (`scripts/xlsx_raw.py`, `scripts/frc_sheets_full.py`), all columns exported to `frc-data-full/`. Earlier CSVs (`frc-data/`) came from the XML and dropped columns.

## 1. What the three sheets contain (AK; CW has same structure)
| Sheet | Rows x cols | Notes |
|---|---|---|
| Page | 377 x 53 | Type: Form 254, Detail 62, Summary 61. Min/Max Occurs, Sequence, Condition, Hide Premium, Variable, Scheduled. Btn* columns (button labels) are all empty |
| Page Fields | 937 x 54 | Select 51, Text 750, Textarea 74, Checkbox 35, Button 24, Hidden 2, Radio 1 |
| Domain Tables / Keys / Entries | 49 / 7 / 259 | Entries sheet only carries 12 tables (the rest inherit platform values). Display value = data value for every entry. Keys (County, CityTown, ConstructionCode, FireClassificationCode, UMBILimit) are not used by any CU page field |

AK vs CW: identical on Policy Detail and the 9 risk groups (167 fields). They differ only in form pages ("Alaska ..." variants) and domain-entry Status (Inherited vs Added).

## 2. Columns missed in the first pass (now used)
- **Comment = "Header"** -> row is a section heading, not a value (Premium 1st-5th Million, GL Premises/Products). Now Subheading.
- **Help Text** (TerrorismCoverageSpecificLimitations) -> tooltip.
- **Min / Max** on numeric text fields -> input min/max.
- **Required Condition** (10 fields) -> required only when that condition holds.
- **Display Controller** (7 Policy fields) and **Trigger Automatic Rating** (PolicyCoverageForm, TerrorismCoverage) -> recorded in `Custom3` / `Custom4`; rating itself is not simulated.
- **Page sequence + Max Occurs** -> risk groups now in FRC order (Aircraft, BOP, Commercial Auto, Auto Dealers, General Liability, Employers Liability, Liquor, Watercraft, Other Liability); **Auto Dealers allows 1 row only**.
- Not UI: Display Columns (print layout), Amendable/Auditable flags, Print Required, Policy-side flags (screen uses the Quote-side flags).

## 3. Other sheets / files
| File | Usable in UI? | What was done |
|---|---|---|
| **DS** (data structure) Column Details | **Yes** - data type, size, scale per column | Decimal(10,2) -> number step 0.01; Integer; Date; Text size -> maxlength. `NameID` is a Unique Identifier (confirms carrier is a lookup) |
| **ALG_HR** `Err-*` / `ErrorMessages` | **Yes** - validation rules + exact messages | 14 group rules + 1 policy rule turned into `cu_validation_rules.json` (e.g. "At Least One Underlying Liability Premium Must Be Greater Than 0", GL hired/non-owned limit vs premium). Form-level rules (only one of CU 22 20 / CU 22 63 etc., 56 in all) belong to forms, not built |
| ALG rating sheets (Policy, 39_CU 1st Million Cov ... 41, Table Objects, 14k Column Nodes) | No (premium calculation) | Not read in detail; only the sheet list |
| **TC** test case (Input / Calculations) | Reference only | Sample values consistent with FRC defaults (e.g. Umbrella limit 1,000,000, SIR 10,000, Excess manual premium). Can seed demo data |
| **DOC** | Guidance | "Refer to Company" = 7 form rules rated manually (manual premium field); "Not Supported" empty |
| RC (delta report) | No | Duplicates FRC pages added/changed for AK |
| AMF xml, RCRN docx, Readme | Not read (feed file / release notes) | |
| DS sheets "Ratebook*", "Tables" | No (rating tables) | |

## 4. Still open
- Garage / UnderlyingLiability / Payments / ESignature have DS tables but no FRC pages.
- GL rule mentions `Underlying Employee Benefits Premium`, a DB column with no field on the GL Detail page (treated as 0).
- 2023/2026 CU batches not compared.
