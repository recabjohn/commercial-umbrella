# CU (Commercial Umbrella) screen task — findings index

| File | What | Source scope |
|---|---|---|
| `01-iso-erc-suite-product-guide.md` | ISO ERC Suite Product Guide analysis; CU/GL/BOP hierarchy diagrams (pp.73, 79, 82) | PDF only |
| `02-runtime-ui-configuration-flow.md` | How hierarchy/screens are configured and rendered at runtime (Builder import sheets, Application Service, navigation) | `claude-config` docs only |
| `03-cu-frc-page-field-domain-analysis.md` | CU hierarchy from FRC Page / Page Field / Domain Table (AK primary, CW compared). **Current best hierarchy answer.** | FRC XML |
| `04-cu-hierarchy-other-systems-and-recommendation.md` | Web/industry check (ACORD 131, ISO CU DS 01) + recommended CU hierarchy (Option A/B) | Web |
| `05-gl-runtime-page-and-cu-mapping.md` | GL Risk/Coverage runtime behaviour from live metadata + screenshots; CU mapping | User-pasted metadata |
| `06-frc-full-sheet-review-and-other-sheets.md` | Complete read of Page / Page Fields / Domain sheets (all columns) + DS / ALG / TC / DOC assessment for UI | FRC, DS, ALG, TC, DOC xlsx |
| `07-cu-screens-build-log-versions-and-design.md` | Everything built after the FRC review: 4 live Vercel sites, Program Selection page, TC samples (AK/KY/AR), premium logic + verified totals, lookup dropdown, bugs, tests, limits | Session work + TC xlsx |
| `08-cu-multistate-research-gemini-check-and-open-questions.md` | ISO CU DS 01 multistate research, Gemini claim check, open questions for Teena | Web + FRC |
| `frc-data/` | CSV exports of FRC pages, fields, domains (AK, CW) | FRC XML |
| `_unrequested-erc-prelim/` | Early read of CU ERC files (AK, CW) done before being asked. **Unreviewed, not authoritative.** Includes extraction scripts. | ERC files |

Build output: `../../build/lob-page/` — CU "Line Of Business" page metadata (`cu_lob_page_metadata.json`), generator `build_lob_page.py`, check `test_lob_page.py`. Risk/Coverage page: `../../build/risk-page/` (metadata JSON, `cu_risk_screen.html`, `test_risk_page.py`, `test_risk_screen.py`). Assumptions are listed at the top of each generator.

Supporting: `../source-md/iso-erc-suite-product-guide.md` (markitdown conversion), `../source-md/pages/*.png` (rendered guide pages).

**Convention:** `[G p.N]` = guide page, `[CC: file]` = claude-config doc, `[INFERENCE]` = unverified.
**Pending:** user to specify which ERC files/checks; GL Builder spreadsheet or metadata sample to confirm runtime hierarchy mapping.
