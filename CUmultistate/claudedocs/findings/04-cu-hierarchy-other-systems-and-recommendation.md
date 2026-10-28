# Findings 04 — CU hierarchy: what other systems show, and recommendation

## 1. What was checked
| Source | Result |
|---|---|
| claude-config docs | Generic runtime/Builder mechanics only; no worked LOB hierarchy example (finding 02) |
| ISO ERC guide + CU FRC (AK, CW) | CU is flat: Policy → risk groups (Summary → Detail) (findings 01, 03) |
| Local prototypes `endo-nav`, `findinsured` | Shell/LOB page only; no hierarchy example |
| **Not yet read (on this machine)** | `Documents\CF template\SWP_1_Entity Hierarchy V6_*.xlsx` (SWP entity hierarchy), GL/AU/CP `savesubmission.json` (real transaction data shape), `Documents\lob-flow` (Risk/Program screenshots). Probe script written (`_scripts/probe_others.py`), not run. User redirected to web search first |
| Web (this finding) | Industry forms only. **No vendor (Guidewire, Duck Creek, Insurity…) umbrella screen/data-model documentation found.** Searches returned marketing pages |

## 2. Web evidence (industry, not another PAS)
- **ACORD 131 (Umbrella/Excess application)** [sonant.ai/blog/acord-131]: sections = Policy Information/Transaction Type; Limits of Liability and Retained Limit; Underlying Coverage Details; **Schedule of Underlying Policies**; Employee Benefits Liability exposure; Vehicle and Property risks. Schedule columns: type of insurance, carrier + NAIC code, policy number, each-occurrence and aggregate limits, effective/expiration dates.
- **ISO CU DS 01 declarations** [insurancexdate.com/insurance-forms/CU/CU-DS-01]: Named Insured, Policy Period, Limits (each occurrence, aggregate), **Schedule of Underlying Insurance** (insurer, policy number, period, minimum required limits), Self-Insured Retention, Premium, Endorsements.
- Typical underlying lines named by the sources: CGL, Business Auto, Employers Liability/Workers' Comp, Professional, Watercraft, Aircraft [search summary].

## 3. What this implies (inference)
Industry structure for umbrella = **Policy (limits, SIR, premium) + one flat Schedule of Underlying Insurance**. No Location/Classification tiers. This matches the ERC finding (flat, 2 levels). Three independent sources agree on shape; the web sources say nothing about UI screens.

## 4. Recommended CU runtime hierarchy (for the Builder metadata)
```
Page: Policy / Risk-Coverage
 Policy level (Detail sections, parent entity = Policy)
   Policy Information : RiskType, PolicyCoverageForm, LegalEntity
   Limits             : Limit, SelfInsuredRetention, ExcessLiabilityLimit, ExcessLiabilitySIR
   Terrorism          : TRIA / TerrorismCoverage questions
   Premium (read-only): Nth-million premiums, excess manual premium
 Underlying Insurance (child of Policy, hierarchy level 1)
   per type x9: [Summary table: Carrier | Policy No | Effective | Expiration]
                 -> [Detail: type-specific limits/premiums]
```
- **Option A (recommended): 9 Summary+Detail sections**, one per ERC risk group. Reason: 1:1 with the FRC pages, so the parser can generate it with no mapping rules; field sets differ a lot by type (GL 20 fields, Commercial Auto 27, Aircraft 7).
- **Option B: one "Underlying Insurance" Summary with a Type column** (matches ACORD 131/CU DS 01 and is friendlier), with a type-driven Detail using display conditions. Needs custom mapping from the ERC pages and a decision on how to merge 8 field sets. Not recommended for the first build.
- Forms excluded per instruction.

## 5. Open items
1. Run `probe_others.py` on `CF template` (entity hierarchy xlsx, GL/AU/CP JSON) to confirm the entity names and levels used by existing LOBs (e.g. what GL's Location/Classification are called in the data structure).
2. Look at `lob-flow` Risk screens for how existing LOBs present the risk step.
3. Await the GL page from the user to confirm the section/entity mapping before building CU's Risk/Coverage.
4. Newer CU content exists locally (`Commercial Umbrella\2023`, `2026`, e.g. CW 01/01/2026 V01): check whether the 2026 hierarchy still matches the 12/2020 batch.

Sources: [ACORD 131 guide](https://www.sonant.ai/blog/acord-131), [ISO CU DS 01](https://insurancexdate.com/insurance-forms/CU/CU-DS-01/), [ISO CU 00 01](https://insurancexdate.com/insurance-forms/CU/CU-00-01/).
