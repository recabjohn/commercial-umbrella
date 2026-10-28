# 07 - CU screens: versions, design, TC samples, premium, tests, deploy

Status: 2026-10-27. Covers everything built after the FRC review (docs 01-06). Tags: **[SOURCE]** = read from a file/page, **[PROPOSAL]** = my design choice, not in the FRC, **[ASSUMPTION]** = guessed because the files do not say, **[NOT FOUND]** = looked, not in the files.

## 1. The four live sites (all Vercel, project name = folder name)

| Site | Folder (build -> deploy) | What it is |
|---|---|---|
| https://commercialumbrella.vercel.app | `build\` -> `deploy\commercialumbrella` | Single state. Policy `+` opens the one policy. Opens pre-filled with the AK TC. Has the Carrier / Underlying Policy Number dropdown lookup (main only). |
| https://commercialumbrella2.vercel.app | `CUmultistate\build` -> `CUmultistate\deploy\commercialumbrella2` | One policy (one form, limits, SIR). `+` on the POLICY header adds a state row (State only). Each underlying row has a State dropdown (policy states, or "All States"). |
| https://commercialumbrella3.vercel.app | `CUmultistate3\build` -> `CUmultistate3\deploy\commercialumbrella3` | `+` on POLICY adds a full policy block for the new state (copy of primary, editable). Rating runs per state block. |
| https://commercialumbrella4.vercel.app | `CUmultistate4\build` -> `CUmultistate4\deploy\commercialumbrella4` | Policy container (no `+`, no State field) then a **STATES** section (`+` here). Each state holds its own Underlying Insurance Information. |

Multistate sites open pre-filled with AK + KY + AR; the single-state site with AK. A "Sample data (Test Case workbooks)" dropdown on the Risk page switches samples. All four need the flow to be started on the Line Of Business page (Risk/Program pages redirect to `./` when opened directly).

Vercel CLI login: `recabjohn-2794`, team `recabs-projects-bf6ae966`. Deploy = `vercel deploy --prod --yes` inside the deploy folder. Project names must be lowercase.

## 2. Pages and flow

1. **Line Of Business** (`index.html`) - checkbox list (heading "Program Information / Select Program"). Next unlocks when a box is ticked.
2. **Risk/Coverage** (`risk.html`) - Policy, Additional Coverages (stub), Underlying Insurance Information (9 groups); states section in the multistate versions.
3. **Program Selection** (`program.html`, new) - modelled on the default Solartis page (user screenshots). Rate Indication (Subline CU, State, dates 10/23/2026 to 10/23/2027 read-only, Billing Type, Quote Type read-only), Risk Schedule (one row per state: Subline, State, Policy Coverage Form, Umbrella/Excess Limit, SIR, Underlying count), Save (spinner 1 s) -> "Get Available Carriers" -> loading bar (1.2 s) -> two carrier cards (Prime Insurance, Solartis Insurance - names from the pasted default-page response). Cards: Total Premium, Subjectivities, Forms, Preview Rating Worksheet (opens the TC-style worksheet), Preview Quote, Create Quote (last two are "Prototype: not wired").
4. Previous on Program Selection returns to Risk and **replays** the saved state through the same UI.

`sessionStorage` keys: `cuFlow` (one-shot gate), `cuRestore` (replay requested), `cuRiskState` (policy, states, rows, forms), `cuRisk` (rows for the Program schedule), `cuRate` (rating worksheet), `cuSample` (selected sample). Details panel values are the Line Of Business values (TestAgency9590, testagent1003 testagent1003, SN196153, In Progress, flow test) on all pages.

## 3. Risk page details common to all versions

- Fields come from the FRC metadata JSON (policy 26 fields, 9 underlying groups with Summary + Detail pages). **[SOURCE]**
- Policy Save collapses the policy to one line, e.g. `AK - COMMERCIAL UMBRELLA COVERAGE FORM AND COMMERCIAL EXCESS LIABILITY COVERAGE FORM (PRIMARY STATE)`; click to edit again.
- Underlying rows: chevron (expand/edit, size bug fixed), Save collapses the row, Action `⋮` opens a "Delete" menu.
- Rules from the FRC/ALG (e.g. at least one underlying liability premium > 0) still run on Save.
- `cond()` fix: the FRC condition text contains values like `'... Form and Commercial Excess ...'`; the old code replaced the word "and" inside the quotes, hiding Umbrella Limit/SIR/premium fields for the combined form. Fixed by only replacing `and`/`or` outside quotes (all four sites).
- Toasts are muted while a sample is replayed (`window.QUIET`).

## 4. How the versions differ (the question for Teena)

| | v1 main | v2 | v3 | v4 |
|---|---|---|---|---|
| Policy terms (form, limits, SIR, terrorism) | once | once (primary) | once per state (own block, prefilled copy) | once |
| Adding a state | n/a | `+` on POLICY; row has State only | `+` on POLICY; full policy block | `+` on STATES; State dropdown + Add |
| Underlying rows | one global list | one global list, State dropdown per row (policy states or All States) | same as v2 | inside each state |
| Premium rated | policy | policy | per state block; All-States rows rated on the primary **[ASSUMPTION]** | per state (rows under it); policy terms/excess once |
| Program schedule | 1 row | 1 row per state | 1 row per state (each own limit) | 1 row per state |

All multistate structure is **[PROPOSAL]**. **[NOT FOUND]** in any file: how the Solartis CU ERC models several states on one policy (own limit/SIR per state or one for all), how an All-States underlying row is split. Evidence for "one limit/SIR per policy": ISO CU DS 01 declarations (see doc 08). Evidence for "one policy record per state": the pasted GL runtime metadata (policy record carries State and SolartisIsPrimaryState) and the FRC (State is the first Policy field).

Removed on request: the Multi-State Summary table and its checks; a sample policy number (POL-nnnnnnn) was added and reverted.

## 5. Premium (reproduces the TC "Calculations" sheet)

Formula: for each underlying row, every premium field (Underlying Liability Premium, vehicle-class premiums, GL Table 1-3 / A-C premiums, Hired & Non-Owned premium) x **Policy Type Factor** = premium; sum by group = **1st Million Premium**; + **Excess Liability Manual Premium**; + premiums of the policy-level forms; = **Policy Term Premium**. **[SOURCE]** TC Calculations sheets (AK, KY, AR).

- Policy Type Factor is 1 in every TC; the real factors come from rate tables not in the TC. **[NOT FOUND]** -> screens use 1.
- 2nd-5th Million premium is $0.00 in the TC (limit 1,000,000); the rule for higher limits is **[NOT FOUND]** -> $0.00.
- The Risk page policy section shows 1st-5th Million and Excess premium; Program Selection shows Total Premium; Preview Rating Worksheet shows the per-group lines (per state in v3/v4).

| TC | 1st Million | Excess manual | Forms | Policy Term Premium |
|---|---|---|---|---|
| AK (TC-CU-AK-12012020-V01) | 856,000 | 100,000 | BOP changes 10,000 + TRIA 10,000 | **976,000** |
| KY (TC-CU-KY-12012023-V03) | 871,000 | 10,000 | Auto Dealers 250,000 + BOP changes 250,000 | **1,381,000** |
| AR (TC-CU-AR-01012026-V01) | 10,000 | 10,000 | 11 forms 35,100 + Terrorism 6,612 | **61,712** |

AR terrorism premium (6,612 = Terrorism Factor .12 x 55,100) is carried over as a form line because "Terrorism Factor" is not a screen field.

Multistate totals with AK+KY+AR: v2 and v4 **2,398,712** (excess counted once: AK's 100,000); v3 **2,418,712** (excess per state: 100,000 + 10,000 + 10,000). Differences are the excess-premium counting only.

## 6. Sample data from the TC workbooks (`samples\`)

- `make_samples.py` holds AK, KY, AR values (copied from each `Input` sheet) and writes `seed_<kind>.html` (head script that loads the chosen sample into sessionStorage before the Risk page runs) and `bar_<kind>.html` (selector). Kinds: `single`, `v2`, `v3`, `v4`.
- Filled: TC fields that exist on the screens. **Skipped** TC-only fields: KY "Policy Issued To Operators Of Aerial Recreational Devices Or Facilities", AR "Terrorism Factor", all individual form input blocks except their premium.
- **Assumed:** AR Aircraft row Carrier = "Test" (the TC summary line is blank, the detail block says Test). The AR TC has only an Aircraft Liability row; the other eight groups are not invented.
- Policy values: all three TCs use the combined form (Umbrella + Excess), Corporation, 1,000,000 / 10,000. AK and AR Accept Certified Acts = Yes; KY = No (with Specific Limitations = No).
- Dates are ISO in the inputs (`2013-10-01`, `2020-12-01`, `2026-01-01`...). KY GL Hired and Non-Owned limit 1,500,000 and Watercraft limit 4,500,000 are valid options in the FRC domains.
- Source paths: `CUP Batch 1 ERC Files\ERC-CU-AK-12012020-V01\...\TC-CU-AK-12012020-V01.xlsx`, `Documents\Commercial Umbrella\2023\ERC-CU-KY-12012023-V03\...\TC-CU-KY-12012023-V03.xlsx`, `Documents\Commercial Umbrella\2026\ERC-CU-AR-01012026-V01\...\TC-CU-AR-01012026-V01.xlsx`.

## 7. Underlying policy lookup (main site only)

Carrier and Underlying Policy Number on every underlying row are dropdowns (State-select look, chevron) that also accept typing. **[PROPOSAL]** - the FRC defines both as plain text. Data = `samples\lookup.json` from `make_lookup.py`: header values of the AK/KY/AR TC rows per LOB plus 10 made-up samples per LOB (fictional carriers: Prime Insurance, Solartis Insurance, Northwind Mutual, Summit Insurance Co, Harbor Specialty; numbers like GL-100231; two periods 2026-01-01/2027-01-01 and 2026-08-01/2027-08-01). Behaviour: click/focus opens the list; typing filters; "No matches" keeps the typed value; choosing a carrier narrows the policy-number list; choosing a number fills carrier and (empty) effective/expiration dates. Tab is handled in code because the browser default dropped focus after the input was wrapped. Not connected to a real policy lookup. Multistate sites do not have it.

## 8. Bugs found and fixed during the build

1. `cond()` replaced "and" inside quoted values (section 3).
2. Row chevron had zero size (CSS) - same bug as Crime.
3. First `.card .btn` was used as the Previous button; once the policy form renders at load it became the Save button -> use `.lobnav .btn`.
4. LOB Next also set `cuRestore` (copy of the Previous handler) and blocked sample seeding - removed.
5. Restore filled the State field before the rest of the form existed - fill State first, then the rest.
6. Tab from the Carrier dropdown lost focus (section 7).

## 9. Tests (all headless Playwright, run from the repo; rebuild with `py -I` first)

Build order per site: `build_risk_screen.py` (metadata dir, expand-panel json, logo, out) -> `build_program_page.py` -> `deploy\make_site.py`. Logo path used: `Documents\findinsured\site\logo.png`; Details data `build\lob-page\cu_expand_panel_metadata.json`.

| Test | Checks |
|---|---|
| `samples\test_samples.py` | All four sites open pre-filled; rows (9 / 19) and Total Premium (976,000 / 2,398,712 / 2,418,712 / 2,398,712); Previous restores. |
| `samples\test_ky_ar.py` | Main site with KY (1,381,000) and AR (61,712). |
| `samples\test_lookup.py` | Dropdown lookup on GL, Aircraft, Auto Dealers, Liquor; pick, filter, type, autofill. |
| `build\program-page\test_program_page.py`, `test_flow.py` | Program Selection page and main flow. |
| `build\tc-ak\test_tc_preview.py` | AK TC fill and $976,000 (preview folder). |
| `CUmultistate\build\program-page\test_flow.py`, `CUmultistate3\...\test_v3.py`, `CUmultistate4\...\test_v4.py` | Each multistate model end to end incl. Previous restore. |

Old card-based multistate files are kept as `*_v1_state_cards.py`. Patch scripts (`patch_*.py`, `samples\wire_*.py`) record exactly what changed from one version to the next.

## 10. Known limits / not done

- No real rating: factors, 2nd-5th million, forms premium rules, terrorism factor are TC constants.
- Lookup dropdown only on the single-state site.
- Additional Coverages and Underlying "forms" are stubs; the TC form list is not on a screen (only form premiums feed the worksheet).
- Premium split for an All-States row (v3) is an assumption.
- Program Selection Quote/Create Quote buttons are not wired.
- Details panel and carriers/subline values on Program Selection come from pasted default-page data, not a service.
