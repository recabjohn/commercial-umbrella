# Findings 01 — ISO ERC Suite Product Guide (Oct 2019, Parser 4.0.8)

**Source:** `ISO ERC Suite Product Guide - October 2019 version for Parser 4.0.8 2.pdf` (83 pages)
**Converted copy:** `claudedocs/source-md/iso-erc-suite-product-guide.md` (markitdown). Page 79 rendered to `source-md/pages/p79.png` because the hierarchy diagrams do not survive text conversion.
**Scope of this analysis:** whole guide read. Not yet read: the 3 sibling ISO guides it references (Maintenance, RC XML, On-line Help), the ERC files in `CUP Batch 1 ERC Files`, the assumption hierarchy.
**Convention:** `[G p.N]` = stated in the guide, page N. `[INFERENCE]` = mine, unverified.

---

## 1. What ERC is
- Excel + XML representation of the ISO Commercial Lines Manual (CLM): rules, state exceptions, loss costs, form attachment logic, per LOB and state. [G p.5]
- Meant to be uploaded into any rating / policy admin system. [G p.5]
- Umbrella is a supported LOB ("Commercial Umbrella"). [G p.5]

## 2. File naming `TTTT-LL-XX-MMDDYYYY-VVV` [G p.7]
| Part | Meaning |
|---|---|
| TTTT | File type: ALG, AMF, DOC, RC, RCRN, TC (also DS, FRC seen in our folder) |
| LL | 2-char LOB code (guide example: CF = Commercial Property) |
| XX | 2-char state, or `CW` countrywide |
| MMDDYYYY | Effective date (driven by circular effective date) |
| VVV | Re-release version for the same effective date |

- **[INFERENCE]** `CU` in our folder = Commercial Umbrella. The guide text I read only gives `CF` as an example code; it does not list `CU`. Confirm against `Readme.txt` / RC Ratebook Properties.
- State packages and countrywide packages are separate since June 2014. [G p.11]

## 3. Package components
| File | Format | Purpose | Screen relevance |
|---|---|---|---|
| **RC** (Rating Content) | xlsx + xml | Rating data, domain tables, rate tables, **pages, page fields** | **PRIMARY** — defines screens |
| **DS** (Data Structure) | xlsx + xml | Table/column inventory + parent/child; state packages only | Field types/sizes, hierarchy |
| **ALG** | xlsx + xml (HR/MR) | Rating algorithms, form attachment, stat, error messages | Validations, conditional logic, premium flow |
| **DOC** | xlsx | Refer to Company, Not Supported, stat assignment, special considerations | **Read first** — what is NOT supported |
| **RCRN** | docx | Release notes: circulars, enhancements, corrections, known issues | Change tracking |
| **AMF** | xml | Delta feed (rate/domain values, PCH, workflow) since Feb 2016 | Maintenance, not initial build |
| **TC** | xlsx | Sample test case: Input + Calculations tabs | **Test oracle** for premium |
| **Readme.txt** | txt | File list for audit | Completeness check |

- HR = human readable, MR = machine readable. XML is for programmatic consumption; Excel for analysis. [G p.19, p.17]
- Commercial Auto and GL have two countrywide files (CW1, CW2). Not stated for Umbrella. [G p.19]

## 4. Content layering (inheritance) [G p.25-26]
`non-LOB base` → `countrywide (CW)` → `state`. State content is **exceptions only** (Report Type: "Exceptions (Additions And Deletions)") since Aug 2011.
Colour code in Excel: black = inherited, **blue = added/modified**, **red = deleted**. [G p.49]
`Status` column on entries: Added / Changed / Deleted; stays until deleted or re-inherited. [G p.31]
**Build implication:** a state screen definition = CW pages/fields overlaid with state exceptions. Reading the state file alone gives an incomplete picture.

## 5. Table types and hierarchy (DS) [G p.20-22]
Five relevant types: **Policy** (exactly one, root) → **Risk** (0..n, can nest) → **Form** → **Coverage** → **Schedule**.
- Policy links: ≥1 risk, 0+ forms, 0+ coverages.
- Risk links: child risks, forms, coverages, schedules.
- Form links: coverages, schedules.
- Ignore Human / Company / Payment / Note / User / Address (ERC+software only).

**Commercial Umbrella hierarchy** (image, p.79): Policy has children `Forms`, `Coverages`, and risk groups **Aircraft Liability, BOP, Commercial Auto, Employers Liability, General Liability, Garage, Liquor, Water Craft** (10 children total under the quote/policy node).
**[INFERENCE]** Those 8 groups likely represent underlying/scheduled-insurance sections on the umbrella screen. Not stated by the guide. Verify in the CU `DS` Tables tab.

> **Recheck (PDF only):** diagrams viewed as images. CU p.79 = Policy with 10 direct children (Forms, Coverages + 8 risk groups), no nesting, no Schedules shown. GL p.82 = Policy→Location→Classification (matches your example). BOP p.73 = Policy→Location→Building→Classification. So per the guide alone, CU is flat (depth 2) unlike GL (depth 3). Whether the ERC files agree is NOT checked here.

## 6. Pages → screens (the core of the screen task) [G p.44-55]
### 6.1 Page tab
- One page = one table. Policy page is the first Detail page, one per LOB.
- Page `Type`: **Detail** (policy / risk / form-schedule), **Form** (an ISO form), **Summary** (ignore).
- Page tree for a wireframe: start at Policy Detail, filter `Type=Summary` + `Parent=...` to list child risk pages; repeat per level. Ignore the "Payment" page. Filter `Type=Form` + `Parent` for forms. [G p.49]
- Form pages: **Mandatory** (min/max 1/1), **Conditional** (0/0, attached by ALG Form Logic), **Optional** (0 / >99; Condition column = eligibility, not attachment). [G p.46-47]
- Guide p.45 says Summary pages "can be ignored" but p.44 also uses Summary pages to find child risks; the guide does not say whether a Summary carries repeat occurrences. Unverified against data.
- `Number` = form number + edition ("CP 00 90 07 88"); blank number = data-collection page only.
- `Hide Premium`: Yes = NOT premium bearing.
- Columns to ignore: Sequence, Sub Sequence, Before/After Script, Template File, Btn*, etc. (ERC+software, removed Oct 2018). [G p.47]

### 6.2 Page Fields tab
| Attribute | Meaning / rule |
|---|---|
| Field | Same name as DS column. Always tied to a column |
| Sequence | Display order |
| Type | Select, Radio, Radio-Vertical, Checkbox, Text, Text Area (real inputs). Anchor, Hidden, Button, Dialog = ignore for UI [G p.50-51] |
| Label | UI label text |
| Quote/Policy Required, Display, Read Only | Separate flags per context; premium/rate/factor outputs are read-only |
| Default / Min / Max | Default value, numeric bounds |
| Domain Table | Allowed for radio, radio-vertical, select, text. Select/Radio **require** one |
| **Condition** | When the field is displayed (expression) |
| **Required Condition** | When the field is required for rating |
| Print Required | Variable data needed on the printed form |
| Help, Help Text, Display Controller | Internal, ignore |

- Data-collect fields = filter `Quote Required` or `Policy Required` = Yes, drop read-only. [G p.54]
- Some fields are Policy-required but not Quote-required (stat/data capture, e.g. name, address, occupancy description). [G p.52]
- **Coverage identification:** page fields formatted `Table.Column` (e.g. `...PrsnlPropCoverage.PolicyTermPremium`) mark a coverage. [G p.54]
- Text Area needs Text column type; Text field input is constrained by the column type (integer column cannot take a string). [G p.51]

### 6.3 Page Related Fields tab
Declares which field **controls** a domain table's values (cascading dropdowns). Columns: Page, Field, Domain Table, Related Field, Related XPath. **Related Field and Related XPath are mutually exclusive.** [G p.55]

## 7. Domain tables → dropdown/option content [G p.28-36]
- Types: **Picklist** (exact match, `DataValue`) and **Range** (`MinimumValue`/`MaximumValue`, used to restrict Integer/Decimal input).
- Data types: Date, Decimal, Integer, Text. Size only for Decimal/Text; Scale only for Decimal.
- **Keys** create cascading lists: without keys all values show; with keys only rows matching the key values show. Example: `ZipCodeTN` keyed on CityTown + County. Keys appear left-to-right by Sequence. [G p.30]
- `ConstructionCode` keyed by `ConstructionTypeToUse` is the guide's worked cascading example. [G p.35]
- `DisplayValue` is "internal, disregard"; **`DataValue` is the stored value**. [G p.32]
- Generic reusable domains exist, e.g. `YesNo` (No seq 1, Yes seq 2). [G p.33]
- Each page field links to exactly one domain table; one domain table can serve many fields. [G p.34]
- Domain value `Other` = user types it in; ERC+software only, **ignore for ERC**. [G p.31]
- Masked domain tables are obsolete, being removed. [G p.29]

## 8. Rate tables (rating, not display) [G p.37-43]
- ≥1 key column + value column(s). Keys usually match domain table `DataValue`s; key name = domain table name when a domain is used.
- Key/value types: Date, Decimal, Integer, Long, Text. A key backed by a **Range domain must be Text** regardless of the domain's type. [G p.38]
- Lookup types: Exact Match (fails if absent), Less Than, Less Than or Equal, Greater Than, Greater Than or Equal, Interpolate (linear).
- Standard column sizes: **Rates/Factors decimal 8,4; Premium decimal 10,2**. [G p.23]
- ⚠ **Guide defect:** the Less Than / Greater Than strategy descriptions and the worked examples on p.42-43 contradict the one-line definitions on p.42 (e.g. key 3 vs rows 0,1,4,9: "Less Than" example returns the row for 4, whereas the definition says highest value below 3, i.e. row 1). Do not implement lookup direction from this guide alone; confirm from ALG XML / ISO Maintenance Guide / a TC case.
- Interpolation example: 3 between (1→5.51) and (4→11.40) = 9.44. [G p.43]

## 9. Algorithm (ALG) structure [G p.56-71]
Tab order: Table of Contents, Application Version, Error Messages, Stat Assignment Info, Form Logic, Common Rating / Risk Common Rating, Total Policy/Risk Premium, Coverage on Policy Indicator, per-table premium tabs, Table Objects, Column Nodes, **Flowchart** (exact execution order).
- `PCH` = Premium Calculation Header; `CCH` class calc header; `Column Nodes` usage: BOTH (rating + premium), OTHERS (rating only), UNUSED.
- Element types: Common Rating, **Error Messages** (validation text → screen validations), Execution Flow, **Form Logic** (conditional attachment), Coverage on Policy Indicator, Premium Calculation, Stat Reporting, Table Objects, Opt Out (GL only).
- Variable types in column F: `UI` = user input field, `RT` = rate table, `COLUMN_*`, `XPATH_*`, `CONSTANT`, `LV_*` local vars.
- `inherited` / `Overridden` attributes show whether state logic deviates from CW.
- ALG links to RC XML through `AssemblyId` (GUID). `asText`, `excelRow`, `excelSheet` are documentation only.
- Only function in ALG is `count` (tally). Operators incl. `&&`, `||`, `!=`, `%`, `Ceiling`, `Round Up Dollar`, `AddYears`, `PadLeft`, `.Date/.Month/.Year/.Days/.Months/.Years`.
- Premium navigation example: premium = Final Basic Group Rate × Limit/1000 × IRPM Factors × Multi-Premium & Dispersion Credit × Package Mod Factor. [G p.71] (Commercial Property example, not Umbrella.)

## 10. Policy administration elements (not in RC, referenced by ALG) [G p.72]
`EffDate`, `ExpDate`, `Renewal` (renewal vs first issuance), `RenewalIteration`, `Transaction/Effective` (create/issue/endorse date), `State/Name`, `State/ID`, `StateId`, `AnnDate` (WC only). These are **system-supplied inputs the screen/BFF must provide**, not user-entered fields.

## 11. Screen-building implications
1. **Screen set = RC Pages + Page Fields**, ordered by Sequence, filtered to Type ≠ Summary and Field Type not in {Anchor, Hidden, Button, Dialog}.
2. **Visibility** = page-field `Condition`; **required** = `Required Condition` and Quote/Policy Required flags. These map to renderConditions/XPath-style metadata in Builder. **[INFERENCE]** the exact Builder mapping needs `areas/frontend-ui/BUILDER_GUIDE.md`.
3. **Dropdowns** = domain tables; cascading via keys / Page Related Fields.
4. **Numeric limits** = Min/Max and Range domains.
5. **Validation messages** = ALG Error Messages tab.
6. **Forms** = Form pages with Mandatory/Conditional/Optional logic. Conditional attachment is computed from ALG, not user selected.
7. **Per-state variation** = overlay state exceptions on CW; check DOC file for unsupported / Refer-to-Company items before designing.
8. **Test oracle** = TC file Input/Calculations.
9. Company rule (`PAS_ARCHITECTURE`/`frontend-ui`): evaluate every requirement Builder-first; ERC page fields should translate to Builder configuration, not new React code.

## 12. Gaps / open questions
- Guide has **no Umbrella-specific** field, page, or rating detail — only the p.79 hierarchy. All Umbrella specifics must come from the CU RC/DS/ALG files.
- Which screens does "new LOB" need: only Quote/Policy pages, or forms and schedules too?
- Which of the two CU packages (AK, CW) is the template, and are other states coming?
- Guide edition (Oct 2019, Parser 4.0.8) vs content files effective 12/01/2020: confirm the structure still matches (Page columns, ERC+software fields removed since Oct 2018).
- Lookup-direction inconsistency in §8.
- Related guides referenced but not provided: ISO ERC Maintenance Guide, ISO Rating Content XML Guide, On-line Help.
