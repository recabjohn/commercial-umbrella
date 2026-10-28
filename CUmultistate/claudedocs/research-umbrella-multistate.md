# Research: Commercial Umbrella / Excess as an extension of underlying policies, and the multi-state case

Tags: [SOURCE] = stated in a fetched or searched page. [INFERENCE] = my reasoning, not found in a source. "not found" = searched, nothing usable.
Most sources are secondary (educational and broker pages). Primary ISO/ACORD text is paywalled or returned 403, so wording should be checked against the filed forms.

## 1. Umbrella vs excess, follow-form, drop-down, retention, layers

- Excess liability covers only above underlying limits and follows the underlying policy's terms. A true umbrella also covers some risks the underlying does not. [SOURCE] https://www.structuremag.org/article/a-look-at-insurance-options-excess-versus-umbrella-insurance/ and https://www.cottinghambutler.com/post/umbrella-coverage-vs-excess-liability
- Follow-form excess covers only losses the underlying policy also covers and adds dollars. Umbrellas are "typically" follow-form but with their own broader grants. [SOURCE] https://fa-mag.com/news/personal-umbrella-policy-differences-44706.html?page=2
- The ISO CU 00 01 umbrella supplements CGL, Business Auto and Employers Liability, and responds when underlying limits are exhausted by a covered claim. [SOURCE] https://insurancexdate.com/insurance-forms/CU/CU-00-01/
- Drop-down: if an underlying aggregate is exhausted by earlier claims, the umbrella pays as primary on a new covered occurrence, subject to its own terms and any SIR. [SOURCE] https://open-exam-prep.com/study-guides/vt-property-casualty/national-pc-other-lines-2/pcnat-15-commercial-umbrella-excess-liability
- SIR/retained limit:
  - The SIR is the amount the insured bears before the umbrella attaches. It applies to claims not covered by underlying, and can carry defense and claim-administration duties.
  - It is not a deductible, and paying it does not create coverage for an excluded exposure. [SOURCE] https://open-exam-prep.com/study-guides/ca-claims-adjuster/specialty-marine-bonds-flood/umbrella-excess-retentions
  - Retained limit = underlying limits for scheduled policies, or the SIR where underlying does not apply. [INFERENCE] from the CU DS 01 note below.
- Per-occurrence / aggregate: the CU DS 01 declarations list limits for each occurrence, personal and advertising injury, and aggregate. Defense inside or outside limits affects exhaustion at each layer. [SOURCE] https://insurancexdate.com/insurance-forms/CU/CU-DS-01/ and the exam-prep page above.
- Layers in $1M increments (e.g. $1M primary umbrella, then $5M excess of $1M): not found as a rule in any source. The layering idea (excess over umbrella) appears in the general sources. The $1M step is [INFERENCE], market practice only.

## 2. Underlying schedule and minimum limits

- ACORD 131 (Umbrella/Excess Section) is used together with ACORD 125. It captures agency, carrier, policy number, effective date, insureds, limits of liability, retained limit, locations/subsidiaries, and Underlying Insurance. [SOURCE] https://www.fmh.com/docs/agbrokeragesolutionslibraries/accord-forms/excess-casualty/acord-131-umbrella.pdf (via search summary), https://docsumo.com/blog/acord-131-processing
- Per underlying policy, ACORD 131 captures: carrier, policy number, effective and expiration dates, limits, annual renewal premium. Automobile is shown explicitly in the extraction docs. [SOURCE] https://docs.uipath.com/document-understanding/automation-suite/2.2510/user-guide/acord131-ml-package
- A per-underlying "state" field on ACORD 131: not found in what I could read. The ACORD page returned 403 (https://www.merchantsgroup.com/edu/university/acord-forms/acord-131/). The form has a Locations section (state is implicit there). Treat per-row state as [INFERENCE].
- ISO CU DS 01 declarations carry a schedule of underlying insurance: each policy (CGL, auto, EL, liquor, hired/non-owned, foreign), carrier, limits, and effective/expiration dates. Policies not on the schedule are not "underlying insurance". [SOURCE] https://insurancexdate.com/insurance-forms/CU/CU-DS-01/
- Typical required underlying: CGL $1M occurrence / $2M aggregate, Business Auto $1M CSL, Employers Liability $500K/$500K/$500K. [SOURCE] https://open-exam-prep.com/study-guides/vt-property-casualty/national-pc-other-lines-2/pcnat-15-commercial-umbrella-excess-liability. These are "typical" market minimums, not an ISO-mandated number. Other groups (Aircraft, Watercraft, Liquor, BOP, Dealers): not found, so per-carrier.
- If underlying is below minimum or lapses, the umbrella responds as if the required underlying were in place. The insured absorbs the gap, and the umbrella does not drop to the lower actual limit. [SOURCE] same exam-prep pages (including https://open-exam-prep.com/study-guides/ca-claims-adjuster/specialty-marine-bonds-flood/umbrella-excess-retentions).
- SIR applies when the claim is not covered by underlying but is covered by the umbrella. [SOURCE] same pages.
- "Warnings" in a screen are a system behaviour, not a source item. Not found, see section 5.

## 3. Real-time behaviour in a PAS

Searched for PAS-specific behaviour documentation and found none. Everything below is [INFERENCE], derived from the coverage mechanics in sections 1-2.

- Underlying added or changed: recompute required-limit check, retained limit and schedule totals. Rating and UW referral may be re-evaluated. [INFERENCE]
- Underlying removed: the gap still falls on the insured, per the failure-to-maintain rule in section 2 [SOURCE]. A PAS would typically flag or refer this, because the unscheduled policy stops being "underlying insurance" [SOURCE on the unscheduled rule]. [INFERENCE] on the flag.
- Limits drop below minimum: warn and refer. The umbrella still treats the minimum as the attachment point, per the above. [INFERENCE] on warn/refer.
- Underlying expires or cancels mid-term: this is a coverage gap for the insured. The carrier typically needs a notice and a decision (replace, endorse, cancel). [INFERENCE]
- Period alignment: umbrella and underlying are separate policies, often on aligned terms (the ACORD 131 captures each underlying's effective and expiry). Whether terms must be aligned: not found, [INFERENCE] that alignment is a UW preference only.
- Rating dependency: umbrella rating usually depends on the underlying exposures and classes. ISO rating detail was behind paywalls, so not found. [INFERENCE]

## 4. Multi-state

- Governing / primary state: not found as a CU rule. The NRRA "home state" (principal place of business) is the controlling state for surplus-lines tax. [SOURCE] https://www.insurancejournal.com/magazines/features/2011/01/10/186022.htm. For admitted business, a "primary/governing state" for forms and amendatory endorsements is [INFERENCE], typically the insured's mailing / principal state.
- State amendatory endorsements and exclusions: ISO CU forms use edition dates (e.g. 12 20 and 09 00) which suggests state-specific filings, but no state provisions were detailed. [SOURCE for editions] https://insurancexdate.com/insurance-forms/CU/CU-DS-01/. State-by-state amendatory list: not found. Territory is handled by endorsement, e.g. CU 21 85 (worldwide with exceptions). [SOURCE] https://insurancexdate.com/insurance-forms/CU/CU-21-85/
- Monopolistic workers comp states (ND, OH, WA, WY): WC is bought only from the state fund (WA allows some large self-insurance). [SOURCE] https://nextinsurance.com/workers-compensation-insurance/edu/monopolistic-states, https://www.progressivecommercial.com/business-insurance/workers-compensation-insurance/monopolistic-states/
  - How EL (stop-gap) sits under umbrella in these states: not found in the sources I found. Stop-gap EL is the usual private-market substitute [INFERENCE]. It would be the scheduled EL underlying row for those states.
- Surplus lines vs admitted:
  - Under the NRRA, only the insured's home state may regulate and tax nonadmitted insurance and collect premium tax. [SOURCE] https://www.insurancejournal.com/magazines/features/2011/01/10/186022.htm
  - States may enter allocation agreements (NIMA, SLIMPACT) so the home state distributes tax to the risk states. [SOURCE] same page.
  - For admitted umbrella, premium tax is generally by state of risk or allocation. [INFERENCE]
- Premium allocation by state: the allocation basis for CU multi-state is not found. [INFERENCE] options are payroll/receipts/locations by state.
- ISO CLM/ERC packages (countrywide + state layers) and state exceptions: not found. Searching CU 00 01 circulars returned only form pages, with no mention of state exception rules. Paywalled ISO circulars would be needed.
- How PAS screens model it: not found in public sources. Options are in section 5. [INFERENCE]

## 5. Proposals (all [INFERENCE], not requirements)

### Option A: one underlying schedule, State column on each row

- Policy header holds a Primary/Governing State flag (selected from the state list).
- Add a "States" table with one row per state (state, primary flag, exposure/premium basis, form edition).
- Schedule stays 9 groups. Each row adds State (single, or "All/Multiple" for countrywide policies).
- Pros: small change to the existing single-state screen, one grid, easy totals, familiar to users.
- Cons: a countrywide underlying policy (one GL policy covering many states) must show as "Multiple". Per-state limit checks are harder. Monopolistic states need special handling inside the EL group.

### Option B: per-state sub-schedules

- State tabs or a state selector. Each state has its own schedule with the 9 groups, plus a countrywide section for policies that span states.
- Pros: per-state required-limit and form checks, clear stop-gap EL for monopolistic states, maps to state amendatory and tax.
- Cons: duplicates data for countrywide policies, much larger screen change, more validation, heavier for a typical small number of states.

Suggested starting point: Option A (lower effort, single schedule retained), moving to B only if state-specific underlying is common. This is a judgement call, not a sourced finding.

### Real-time behaviours the screen could show (proposals)

1. Underlying summary vs umbrella limit: per group, the total of scheduled limits against the required minimum, plus the retained limit / SIR in effect.
2. Required-limit warning when a scheduled limit is below the typical minimum (GL 1M/2M, Auto 1M CSL, EL 500/500/500). Wording: "umbrella responds as if the required limit were maintained; gap falls on insured". Minimums configurable. [SOURCE for the rule, INFERENCE for the UI]
3. Missing-underlying warning when a group the insured has is not scheduled, because unscheduled policies are not underlying. [SOURCE for the rule]
4. Period alignment: flag when an underlying expiry falls before the umbrella expiry, or terms differ.
5. Primary state flag: exactly one primary state, which must be among the state rows.
6. Monopolistic state flag: when ND/OH/WA/WY is added, prompt for stop-gap EL in that state rather than WC EL.
7. Surplus lines vs admitted indicator: when surplus lines, home state is the tax state; show the note.
8. Change impact: adding, changing or removing an underlying row recalculates the summary and shows referral reasons.
9. Per-state exposures required where premium allocation is used.

## Gaps

Not found: ISO CLM/ERC state exceptions, per-underlying state in ACORD 131, EL under umbrella in monopolistic states, PAS-specific behaviour, $1M layer rule, state premium allocation basis. Paywalled / 403: ISO circulars, ACORD 131 content page.

## Added context (user-supplied web page, Vouch broker blog, 2026-06-05) - single broker/marketing source, verify before relying
- [SOURCE: blog] Umbrella extends GL, Commercial Auto and Employer's Liability in one layer; activates only after an underlying limit is exhausted (attachment point). Worked example: GL 1M, claim 2M -> GL pays 1M, umbrella pays 1M.
- [SOURCE: blog] Extends limits, not scope: follows underlying exclusions; no E&O, cyber, D&O, own-property cover. Defense costs for covered claims sit inside umbrella limits.
- [SOURCE: blog] BOP bundles GL + property; umbrella sits above the liability part only.
- [SOURCE: blog] Excess liability usually extends ONE policy (e.g. auto only); umbrella extends several. Illinois, New York, Texas use the term "Excess Liability" (verify - one source).
- [SOURCE: blog] Price drivers: industry, claims history, auto exposure, underlying limits, geography/litigation environment. Indicative cost 1M ~ $800-900, 5M ~ $2,500-3,000 a year (market anecdote, not a rule).
- [SOURCE: blog] Limit is usually driven by contract requirements (customers, leases); typical ranges 1M-5M standard, 5M-10M enterprise-facing.
- [INFERENCE] Implications for screens: required-underlying check should treat BOP as satisfying GL; umbrella vs excess form may differ per state; show attachment/limit stack; optional contract-required-limit input (not in FRC).

## Added context 2 (user-supplied web page, The Hartford, "Commercial Umbrella Insurance: What Is It?") - single carrier marketing page
- [SOURCE: Hartford] Extends over underlying policies once their limits are reached, and may also fill gaps the underlying does not cover.
- [SOURCE: Hartford] "Drop down": many umbrellas respond as first-dollar/primary for liabilities excluded from standard GL (examples: non-owned watercraft and aircraft, advertising liability). A deductible or self-insured retention (SIR) typically applies first for those losses.
- [SOURCE: Hartford] The umbrella should be concurrent with the primary policies (same time periods).
- [SOURCE: Hartford] Not for professional liability/malpractice.
- [SOURCE: Hartford] Rate is based on the business's risk exposures; limit option chosen with an insurance professional. Example: GL 1M, judgment 2M, 1M umbrella pays the difference.
- [INFERENCE] Screen implications: (1) period-alignment check is now sourced (needs umbrella dates from somewhere on the page or the insured/quote step); (2) the SIR field matters for drop-down exposures: Aircraft, Watercraft, Other Liability groups; (3) the "required underlying" check applies to GL / Auto / EL only, not to the drop-down groups.
