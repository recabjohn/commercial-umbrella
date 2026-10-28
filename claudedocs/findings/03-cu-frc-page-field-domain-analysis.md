# Findings 03 — CU hierarchy from FRC (Page, Page Field, Domain Table)

**Source:** `FRC-CU-AK-12012020-V01.xml` (primary) and `FRC-CU-CW-12012020-V01.xml` (comparison), read from the **XML** version of the FRC. The XML holds the same Page / Page Field / Domain Table content as the xlsx sheets; the xlsx files were not opened. FRC = full inheritance report (CW + state merged), so it is the right base for metadata.
**Guide basis:** ISO ERC Suite Product Guide pp.44-55 (Page, Page Fields, Domain Tables).
**Scope limits:** Not used: Page Related Fields, rate tables, ALG, DOC, TC, RCRN. AK is one state; other states not checked.
**Data exports (CSV, reproducible):** `findings/frc-data/frc_{AK,CW}_{pages,fields,domains}.csv`. Scripts: `claudedocs/scripts/frc_*.py`.
**Convention:** `[G p.N]` guide, `[INFERENCE]` mine.

## 1. Page tree = the hierarchy (AK, 377 pages, 937 page fields)

```
Policy Detail                         (CommercialUmbrella, 0/1, 26 fields)
├─ Risk group × 9   [Summary, 4 fields] ─► [Detail, 7–27 fields]
│    Aircraft Liability (0/999)    Auto Dealers (0/1)
│    BOP (0/999)                   Commercial Auto (0/999)
│    Employers Liability (0/999)   General Liability (0/999)
│    Liquor (0/999)                Other Liability (0/999)
│    Watercraft (0/999)
└─ Form pages × 254                 each Form (own fields) ─► optional [Summary ─► Detail] schedule
        217 forms have fields, 37 have none; 52 have a schedule Summary→Detail pair
```
| Depth | Type | Count (AK) | Meaning |
|---|---|---|---|
| 0 | Detail | 1 | Policy Detail |
| 1 | Summary | 9 | Risk list pages |
| 1 | Form | 254 | ISO forms |
| 2 | Detail | 9 | Risk entry pages |
| 2 | Summary | 52 | Form schedule lists |
| 3 | Detail | 52 | Form schedule entry pages |

**Hierarchy conclusion (from Page tab):** CU has **one risk level**: Policy → risk group (Summary → Detail). Nothing nests below a risk Detail. Max page depth is 3 only because of form schedules (Policy → Form → Summary → Detail), not risks.
GL by contrast is Policy → Location → Classification [G p.82].

Not in the page tree although present in DS: Garage, UnderlyingLiability, Payments, ElectronicSignature, QuoteLetter (searched AK and CW `Forms` trees; not found there). Guide diagram p.79 lists Garage but no Auto Dealers / Other Liability; the data is the opposite (Auto Dealers, Other Liability present; Garage absent). Guide is Oct 2019, content 12/2020. **[INFERENCE]** guide diagram is stale; Garage page may have been removed.

## 2. Policy Detail — 26 page fields (13 SELECT, 13 TEXT)
| Group | Fields | Notes |
|---|---|---|
| Policy info | `RiskType` (domain RiskType, 9), `PolicyCoverageForm` (3), `LegalEntity` (28) | `RiskType` shown only when `PackagePolicy[.='Yes']` |
| Limits | `Limit` (1M–5M, 5 values), `SelfInsuredRetention`, `ExcessLiabilityLimit`, `ExcessLiabilitySelfInsuredRetention` | Display/required driven by `PolicyCoverageForm` value |
| Terrorism | `TRIPTerminatesBeforeExpirationDate`, `TRIAExtended`, `TRIAExpirationDate`, `TerrorismCoverage`, `TerrorismCoverageSpecificLimitations`, `ExcludeOtherActsOutsideUS`, `ExcludePunitiveDamagesRelatedToCertifiedActOfTerrorism` | Chain of Yes/No conditions |
| Premium (read-only) | `Premium1stMillion`…`Premium5thMillion` + `CommercialUmbrellaNthMillionCoverage.PolicyTermPremium`, `CommercialUmbrellaExcessLiabilityCoverage.ManualPremium` / `.PolicyTermPremium` | `Table.Column` fields = coverage premium outputs [G p.54]; Excess manual premium is editable |

`PolicyCoverageForm` values: *Commercial Umbrella Coverage Form*; *Commercial Excess Liability Coverage Form*; *Commercial Umbrella Coverage Form and Commercial Excess Liability Coverage Form*. It switches which limit/premium fields appear.
Coverages (8 in DS) all surface on **Policy Detail only**; none on risk pages.
**[INFERENCE]** `PackagePolicy` is referenced in a condition but is not a Policy Detail page field. It is probably supplied by the package (CPP) context; verify.

## 3. Risk groups — "scheduled underlying insurance"
- **Summary (all 9, 4 fields, all read-only):** Carrier (`NameID`), Policy Number, Effective Date, Expiration Date. This is the list/grid columns.
- **Detail (8 distinct field sets):**

| Risk Detail | Fields | Distinguishing content |
|---|---|---|
| Aircraft Liability, Watercraft | 7 (identical set) | `UnderlyingLiabilityPremium`, `UnderlyingLiabilityLimit` |
| Auto Dealers | 10 | — |
| BOP | 9 | — |
| Employers Liability | 9 | — |
| Liquor | 8 | — |
| Other Liability | 8 | — |
| General Liability | 20 | `CoverageForm` (Occurrence / Claims Made), 4 underlying limits, premises Tables 1–3, products Tables A–C, hired & non-owned auto |
| Commercial Auto | 27 | Premium + vehicle count for each vehicle class (private passenger, light/medium/heavy/extra-heavy trucks, tractors, trailers, zone rated, public transportation, other) |

- Common pattern seen in the three Detail pages inspected (Aircraft, Commercial Auto, GL): `UnderlyingPolicyType` (read-only), `NameID` (**BUTTON**, carrier lookup), `UnderlyingPolicyNumber`, `UnderlyingEffectiveDate`, `UnderlyingExpirationDate`; these are **policy-required, not quote-required** (QuoteRequired 0, PolicyRequired 1). The other five Details were not field-inspected.
- Confirms the earlier guess: risk groups are **underlying insurance schedules by type**, not locations/classes. **[INFERENCE → now supported by field names]**.
- Occurrence: 8 groups 0/999 (repeating); **Auto Dealers 0/1** (single).

## 4. Form pages (254)
- 580 fields on form pages: 511 TEXT, 35 CHECKBOX, 19 TEXTAREA, 12 SELECT, 2 HIDDEN, 1 RADIO.
- Field flags: 228 read-only, 249 policy-required, 103 neither.
- Forms are children of **Policy Detail** (flat). A form with a schedule becomes Form → Summary → Detail (52 in AK, 54 in CW).
- Form page `MinOccurs/MaxOccurs` and Condition / AttachmentCondition patterns were found in the RC file earlier (25 conditional 0/0, 226 optional with Condition 0/1, 4 optional unconditional); not re-verified on FRC.
- AK vs CW: FRC AK has 377 pages, CW 382. 61 CW form pages are replaced by 53 AK-named ones ("Alaska …" variants, e.g. Alaska Auto Coverage – Exclusion Of Terrorism). **State FRC is a merged result, so build metadata from the state FRC and expect per-state form-page differences.**

## 5. Domain tables (AK: 49, all picklist, 0 range)
- Only **12 of 49** are referenced by a page field. Most used: `LiabilityLimit` (23 fields, 81 values: 10,000 … ), `LiabilityLimitNotApplicable` (10), `YesNo` (7), `Limit` (2), `Act` (2), `LiabilityLimitEL` (2), then `RiskType`, `PolicyCoverageForm`, `LegalEntity`, `LiabilityLimitELAggregate`, `CoverageForm`, `CoverageFormNotApplicable`.
- The other 37 (e.g. `BoatType`, `ConstructionType`, `CityTown`, `County`, `ConstructionCode`, `ElectronicSignature`) are not on any CU page field. **[INFERENCE]** they serve rate-table keys, ALG, or pages that don't exist in CU; keyed ones (CityTown 1 key, County 2, ConstructionCode 1) look inherited from the shared base.
- Dropdown content to carry into `Question Value`: Display = `DisplayValue`, Data = `DataValue` [G p.32].

## 6. Assumed runtime hierarchy for CU (inference, to validate with a GL metadata sample)
```
Page: Policy / Quote
 ├─ Section PolicyInfo / Limits / Terrorism / Premium   [Detail, entity=Policy, level 0]
 ├─ Section Underlying <Type> × 9                       [Summary data table, parent=Policy, level 1]
 │     └─ Underlying <Type> Detail                      [Detail form/dialog, parent=Summary, level 2]
 └─ Forms (254; 52 with schedule lists)                  [placement not determined]
```
- Maps to Builder `Section Type` Summary/Detail with `Parent Section Name` + `Hierarchy Level` (see finding 02). Each risk group = one entity under Policy.
- Page field → Question; `Condition` → Question Display condition; `RequiredCondition` → Question Required Condition; domain table → Question Value; QuoteRequired/PolicyRequired → quote vs policy mandatory handling (needs a decision).
- Condition syntax in FRC (`Field[.='Yes']`, and sometimes `Field='Yes' or (...)`) is XPath-like; Builder uses `//Section__Question[.='Yes']`. Section prefix and a normalised syntax would be needed. **[INFERENCE]**

## 7. Open points to decide / verify
1. Forms: do they get Builder sections, or are they attachment-only at runtime? (254 pages; none are rating inputs.)
2. Quote vs policy flags differ (e.g. underlying policy number: policy-required only). How the Builder handles that split.
3. Garage / UnderlyingLiability / Payments / ElectronicSignature / QuoteLetter: no FRC pages. Confirm in ALG/DS whether UI is expected.
4. Source of `PackagePolicy`.
5. Confirm `NameID` BUTTON behaviour (carrier search; guide says buttons apply to Unique Identifiers linked to Address/Company/Human [G p.51]).
6. Check other states in the batch (only AK and CW provided).
7. Domain-table keys / Page Related Fields (cascades) not analysed since only 3 sheets were requested.
