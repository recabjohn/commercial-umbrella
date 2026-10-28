# Findings 05 — GL Risk/Coverage page (live metadata) and CU mapping

Source: user-pasted getApplicationMetadata responses + screenshots for the GL Risk/Coverage step (SWP_1_3_V1, UAT). Session tokens in the pastes were NOT copied; field/entity names only. Tokens should be rotated if the pastes were shared.

## 1. What GL actually does at runtime (observed)
| Step | Sub-application (type) | Entity | Notes |
|---|---|---|---|
| Page chrome | breadcrumb child tab "General Liability" (one tab per ticked subline) + ExpandPanel "Details" strip | – | LocationValidation (OutputLabel "Note: At least one State and Classification need to be added.") + NavigationButtonsSubmission |
| "STATE" accordion, click **+** | PolicyDetail_2 (Detail) | `Policy` (id 1619294) | First only `State` (SelectAutoComplete, AjaxNeeded) |
| pick State | same sub-app, re-fetched with State=AL | `Policy` | `Subline` Select appears (DependentComponent `StateSubline`; DuplicateCheck State+Subline) |
| pick Subline | same sub-app, re-fetched | `Policy` | ~35 policy-level fields load (limits, deductibles, coverage form, legal entity, terrorism, composite rating, premium output). **Save** → `SaveGeneralLiabilityPolicydetails_1.1.0.0`, parent = GL entity id (`generalliablityID`), keeps `PolicyStateID` |
| after Save | AdditionalCoverage (Summary table, add-popup) | none (delete uses `PARENTID=PolicyStateID`, Hierarchy "Policy Detail") | |
| after Save | "RISK SCHEDULE" accordion with Action menu → "LOCATION AND CLASSIFICATION INFORMATION" | – | |
| expand | Location (Summary) → LocationDetail (Detail, expands in row) | `GeneralLiabilityLocation` (id 1618969) | `PARENTPOLICYID` "Subline State" dropdown = the Policy rows saved above; address, deductibles, territory. Save → `SaveGeneralLiabilityLocationDetails_1.1.0.0`, `ID=StatePolicyID`, `PARENTID=generalliablityID`. ReviewChanges dialog + BulkSave → `BulkUpdate_1.1` |
| Classification | not yet shown | `GeneralLiabilityClassification` | confirmed only by BulkUpdate target path below |

Full entity path (from BulkUpdate `targetLevel`): `Account.Insured.GeneralLiability.Policy.GeneralLiabilityLocation.GeneralLiabilityClassification`.

## 2. Principles that transfer to any LOB
1. **Parent first, child later.** Each level is a collapsed accordion; child content is not rendered/fetched until the parent row is saved (IDs carried in context: `generalliablityID` → `PolicyStateID` → `StatePolicyID`).
2. **Progressive fields via re-fetch.** One Detail sub-app is fetched again with state (and subline) in the request; fields show in stages (State → Subline → rest).
3. **Summary + Detail per level**, Detail opens inside the row; row Action = Edit/Delete.
4. **Entity name = hierarchy level**, set on sub-app and on every attribute (`EntityHierarchyName/Id`); `SubApplicationEntity` maps tile → entity.
5. **Policy is per State(+Subline)**, not one per LOB: GL can hold many Policy rows under one `GeneralLiability`.
6. Entity is per **subline** (GeneralLiability), so a CU entity `CommercialUmbrella` sits beside it under Insured (the LOB page already saves `CommercialUmbrellaID` via `SaveSelectedSubline`).

## 3. CU mapping (inference, from findings 01/03/04 + this GL pattern)
```
Account.Insured.CommercialUmbrella
  └ Policy                      (State accordion: State [+ Subline if CU config requires], Policy Detail fields, Save)
      ├ Coverage / Additional   (policy-level coverages: 1st-5th million, ExcessLiability, ... as Summary/Detail)
      └ Risk schedule  "Underlying Insurance"  (replaces GL's Location -> Classification)
          └ 9 risk groups, each Summary -> Detail:
            Aircraft Liability, Auto Dealers, BOP, Commercial Auto, Employers Liability,
            General Liability, Liquor, Other Liability, Watercraft
```
- CU has **no Location/Classification** (ERC flat: Policy -> risk group). Risk schedule is one level deep, so the cascade is State -> Policy detail -> Underlying Insurance rows.
- Policy Detail (26 fields, 13 SELECT / 13 TEXT per FRC) is the CU analogue of PolicyDetail_2; stage it like GL: State first, then the rest.
- Each risk group Detail mirrors the ERC page (7-27 fields); Summary shows Carrier, Policy Number, Effective, Expiration.
- Forms excluded per instruction.

## 4. Open / unverified
- Whether CU needs a `Subline` field (GL's list is GL-specific: Prem/Ops, Liquor, ...). ERC shows none; assume State only. **[INFERENCE]**
- Classification page for GL not seen; confirm how a third level renders (same in-row Detail?) before reusing for any deeper LOB.
- Real CU entity names/ids and event names (`SaveCommercialUmbrellaPolicydetails_x`) come from Builder; placeholders needed.
- GL `ExpandPanel` and `LocationValidation` note text are GL-specific; CU note should read e.g. "At least one State and one Underlying Insurance need to be added." **[INFERENCE]**

## 5. Update: GL Location/Classification pages received (confirmed)
- **Classification is a sibling table inside the Location row, not a nested accordion.** Expanding a Location row shows: LocationDetail form (Save / BulkSave) -> Location-level Additional Coverages table -> Classification table (+) -> row expands to ClassificationDetail (entity `GeneralLiabilityClassification`, parent = `LocationID` from context, Save event `SaveGeneralLiabilityClassficationDetails_1.1.0.0`). Class Code is a lookup loaded on open (`GetClassCodeDetails_1.1.0.0`, request carries State + Subline). Premium fields are read-only outputText.
- Pattern at every level: **Summary table (+) -> row expands in place -> Detail form -> Save writes the row, parent id comes from context**. Deleting a row uses the same parent id.
- CU applies this one level deep: Policy row -> 9 risk-group tables (each = Summary table + Detail form). No Classification-style third level.

## 6. Build (Risk/Coverage page) - see `../../build/risk-page/`
`build_risk_page.py` (metadata from FRC AK), `build_risk_screen.py` (HTML), `test_risk_page.py`, `test_risk_screen.py`, output `cu_risk_screen.html`.
- Metadata files: `cu_risk_page` (note + Previous/Next), `cu_policy_detail` (State + 26 FRC fields + Save), `cu_additional_coverage`, `cu_risk_groups` (9 x Summary + Detail, 150 attrs).
- FRC `Condition` text is carried in `Custom1` and evaluated by the screen (e.g. Excess limits show only for Excess form). `PackagePolicy` fields (RiskType) are hidden because no such field exists on Policy Detail.
- Placeholders: event names `SaveCommercialUmbrella*_1.0.0.0`, entity ids (0), parent key `commercialumbrellaID`. Carrier (ERC BUTTON) rendered as a text box. Forms excluded.
- Not modelled: Additional Coverages dialog, carrier lookup, class-style lookups, state-specific (CW vs AK) differences.
