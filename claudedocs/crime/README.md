# Crime LOB - first analysis (FRC-CR-AL / FRC-CR-CW, 06/01/2022 V01)

Source: `Crime/ERC-CR-{AL,CW}-06012022-V01.zip` (extracted to `Crime/_extracted/`, nested `RC-CR-*.zip` holds FRC and DS). FRC sheets exported with `scripts/frc_sheets_full.py` to `frc-data-full/` (AL = Alabama, CW = countrywide).
Reading tools: raw xlsx reader (`scripts/xlsx_raw.py`) for FRC/DS (markitdown returned empty output on the FRC: openpyxl style bug); markitdown works on small files (DOC).

## Structure (Page sheet, AL)
- 583 pages: Form 260, Detail 162, Summary 161. Root = `Policy` (Detail, table Crime, 22 fields).
- 7 groups, direct children of Policy, each Summary (0..1 row) -> Detail (0..1):
  | Order (Sequence) | Group | Summary fields | Detail fields |
  |---|---|---|---|
  | 10000 | Commercial Fidelity | 3 | 94 |
  | 20000 | Commercial Crime | 1 | 88 |
  | 40000 | Commercial Fidelity And Forgery | 3 | 53 |
  | 50000 | Government Fidelity | 3 | 77 |
  | 60000 | Government Crime | 1 | 81 |
  | 70000 | Government Fidelity And Forgery | 1 | 51 |
  | 80000 | Kidnap Ransom And Extortion | 3 | 56 |
- Matches the Crime Hierarchy picture (7 groups, each with Coverages + Forms). Names differ: picture "Employee Theft & Forgery" = FRC "Commercial Fidelity And Forgery"; picture "Government Employee Theft and Forgery" = FRC "Government Fidelity And Forgery".
- Group Detail fields = insuring agreements: Included (radio), Premium, Limit, Deductible (select), varying-deductible flag.
- Policy fields include entity type, policy type, ratable employees, premises count, classification chain (Major Industry Group, Predominant Activity, Class Description, Class Code), terrorism (package only), SIC code. Several depend on `PackagePolicy` (hidden field on this page).

## Differences from CU
- No many-row schedule: every group is 0..1, so the "table with +" pattern becomes one row per group (or a plain form).
- Detail forms are large (51-94 fields).
- AL vs CW page counts differ by 1 (583 vs 582); fields equal (2069) - difference to check.

## Not yet done
Forms (260) ignored as with CU; DS types, ALG messages, DOC/TC not read; domain lists (133 tables) not yet mapped; no screen built.
