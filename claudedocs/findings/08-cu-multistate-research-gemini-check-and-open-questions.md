# 08 - CU multistate: research, Gemini check, open questions

Status: 2026-10-27. Companion to doc 07. Tags: **[SOURCE]**, **[INFERENCE]**, **[NOT FOUND]**.

## 1. Question

Can one Commercial Umbrella (CU) policy be multistate, and should a second state repeat the policy fields (Policy Coverage Form, limits, SIR, etc.)?

## 2. What the sources say

- **[SOURCE]** ISO CU DS 01 declarations: one limit, one SIR, one aggregate and one coverage form for the whole policy; a Schedule of Underlying Insurance lists the underlying policies; unscheduled policies do not count. https://insurancexdate.com/insurance-forms/CU/CU-DS-01/
- **[SOURCE]** Verisk (search snippet only; page fetch failed): ISO publishes multistate commercial liability umbrella declarations, forms and endorsements. So an umbrella can cover several states.
- **[SOURCE]** FRC: Policy page has State as its first field (26 policy fields). GL runtime metadata pasted by the user: one policy record per state with SolartisIsPrimaryState.
- **[INFERENCE]** Policy terms are not repeated per state in ISO paper; state-level data (state, underlying policies/exposure) can differ. Solartis ERC may still model it as one record per state.
- **[NOT FOUND]** in any file or searched page: how the Solartis CU ERC models several states (own limit/SIR per state or shared); Guidewire / Duck Creek multistate umbrella screens.

Answer given to the user: CU can be multistate; policy terms are not repeated per state in the ISO form; the Solartis model is unconfirmed.

## 3. Gemini advice check (user pasted two texts)

| Gemini claim | Verdict |
|---|---|
| Underlying rows need a State | **True** - FRC underlying rows have no State field. Built as v2 State dropdown / v4 nesting (proposal). |
| Retro Date missing | **True** - not on the FRC screen. Not added (FRC only). |
| Umbrella rating applies state LCMs / table factors | **Unsupported** - TC Calculations show underlying premium x Policy Type Factor (=1) only. |
| Only one GL table | **Unsupported** - TC has GL Tables 1-3 / A-C premium fields. |
| Limits should start at 1M | **Unsupported** - FRC domain lists the allowed values. |
| Policy must be split from State | **Unsupported** - FRC puts State on Policy; GL metadata has policy per state. v4 builds the split as a proposal. |

## 4. Design options built (all proposals, see doc 07 section 4)

v2 one policy + state rows + State dropdown on underlying rows; v3 full policy block per state; v4 policy container + States section with underlying per state. Decision between v2/v3/v4 is pending with the user ("will confirm which to proceed later").

## 5. Open questions for Teena (all **[NOT FOUND]** in the files)

1. Does the CU ERC allow a different Umbrella Limit / SIR per state, or one for the policy?
2. How is an underlying policy that spans states ("All States") rated/split?
3. Real Policy Type Factor tables (TCs use 1).
4. Premium rule for 2nd-5th million (TC limit 1M gives $0).
5. Rules for policy-level form premiums and Terrorism Factor (.12 in AR TC) - not screen fields.
6. Is Retro Date required for claims-made underlying coverage?
7. Does Program Selection show one risk-schedule row per state?
8. Should Carrier / Underlying Policy Number be a lookup (built in main site as a proposal; FRC says free text)?

## 6. Handling notes

User pasted default-page API JSON/HTML containing session tokens; none were copied into any file. If shared further, rotate them. ERC/TC files are untrusted: read with `py -I`, scripts kept outside the data folders.
