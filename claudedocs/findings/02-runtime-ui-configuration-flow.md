# Findings 02 — How a LOB hierarchy is configured and rendered at runtime (from claude-config)

**Scope:** `claude-config` docs only. No ERC files used. `[CC: file]` = stated in that doc. `[INFERENCE]` = mine.
**Read:** `areas/frontend-ui/{BUILDER_GUIDE,ARCHITECTURE,SCENARIOS,CLAUDE}.md`, `areas/platform-development/{iso-erc-processing,metadata-ui-service}.md`, `projects/msig/lobs/general-liability/CLAUDE.md`, `projects/erc-project/context/04-inheritance-chain.md`, `projects/iso-erc-consumption-automation/CLAUDE.md`, grep of `projects/runtime-UIUX`.
**Not found:** any doc showing a concrete LOB (GL or other) turned from ERC pages into Builder sections, or a sample Builder import / `getApplicationMetadata` response for a hierarchical LOB. Searched only the paths above, not all ~100 projects.

## 1. Configuration chain (design time)
ERC content → ERC Parser → ProductConfigDB / product version [CC: iso-erc-processing] → **Builder UI import spreadsheet** (`*_UIUX-V4_*.xlsx`) → metadata tables (`CNF_UIUX_*`).

Builder sheets, fill in order [CC: BUILDER_GUIDE]:
`Summary → Page List → Page Jurisdiction → Section List → Section Jurisdiction → Section Group Details → Questions List → Question Jurisdiction → Question Value → Questions for Datatable`

## 2. Where hierarchy lives in the runtime config (Section List columns) [CC: BUILDER_GUIDE]
| Column | Role |
|---|---|
| `Section Type` | `Detail` (form) / `Summary` (paginated list) / `Data table` (inline grid) / `Form` |
| `Parent Section Name` | Section renders inside another section |
| `Dependent Question Name` | Section appears based on a parent question's value |
| `Hierarchy Level` | Numeric, required when Parent Section Name is set |
| `Product Data Structure Name` / `Data Structure Version Number` | e.g. `Common_V2` / `Common_V2_Hierarchy_1.0` |
| `Parent Entity Name` / `Entity Name` | e.g. parent `Building`, entity `Location` — the product entity the section writes to |

Application Service model fields: `entityHierarchyId`, `hierarchyLevel`, `parentSubApplicationId`; sub-applications "can be hierarchical" [CC: runtime-UIUX/ApplicationService/ApplicationCore/CONTEXT.md]. Application Service **V7 = hierarchical sub-application rendering, UI hierarchies**; V8 added max-priority rate versions "for ISO implementations" [CC: ARCHITECTURE].

## 3. Runtime flow [CC: ARCHITECTURE, SCENARIOS]
1. Browser → Express BFF → Java `/core/getApplicationMetadata`.
2. Service: validate token → resolve mode/environment → privileges → product + application info → **sub-application list (XPath display conditions drop sections)** → **attributes (XPath marks read-only/drops)** → actions, values, defaults.
3. Returns JSON tree of sub-applications and attributes. `RenderTemplate` resolves layout; `DynamicRender` walks sub-applications:
   - template `summary` → **Data Table** (list of rows, e.g. locations, vehicles)
   - template `detail` → **form**
   - template `dialog` → hidden modal
4. Navigation is a **separate** call (`getNavInfo/V4`) → `PageNavigation` (page order per transaction), `TemplateInfo` (layout shell); keyed by GroupName + UserRole + ProductVerNum + SublineName + FlowName in `CNF_UIUX_MENU_CACHE`. Stale cache is the usual cause of "my change doesn't show".
5. Conditions: Builder `Section Display Condition` → `renderConditions`, evaluated against Redux (`UIFlowReducer` + `metadataReducer`).
6. Jurisdiction: every section and question needs a `CW` jurisdiction row or it never renders.

## 4. GL as the reference LOB
- GL structure: **policy → locations → classifications**; multi-location, multi-class; "first reference LOB… template for all future LOBs" [CC: msig GL CLAUDE.md]. That file states intent only; it has no screen/section list.
- Matches ERC guide p.82 (Policy → Location → Classification).

## 5. Mapping ERC hierarchy to runtime config
Not documented in claude-config. **[INFERENCE]** by analogy only:
| ERC concept | Probable runtime artifact |
|---|---|
| Policy Detail page | `Detail` section(s) on the policy-level page, entity = policy |
| Risk Summary page (repeating) | `Summary`/`Data table` section (list of rows) |
| Risk Detail page | `Detail` section, child of the Summary, with `Parent Section Name` / `Hierarchy Level` / `Parent Entity Name` |
| Page Field | `Questions List` row |
| Domain table | `Question Value` rows |
| Field Condition / Required Condition | `Question Display condition` / `Question Required Condition` (XPath) |
| Form pages | ? (conditional attachment is rating-side; UI treatment not documented) |

## 6. What this means for CU (conditional on §5)
- Runtime depth is driven by `Parent Section Name` + `Hierarchy Level` + `Parent Entity`. A flat ERC hierarchy (Policy → risk groups) implies **one parent level**, not GL's three.
- Runtime may differ from the ERC tree: sections can be grouped (`Section Group Details` tabs), shown or hidden by XPath, and split across pages. So the ERC hierarchy is an input, not the final screen map.
- Builder-first rule applies: all of this is import-spreadsheet configuration; no React code unless a control is missing [CC: frontend-ui/CLAUDE.md].

## 7. Open questions (need a real example)
1. A configured GL (or other ISO LOB) **Builder import spreadsheet or `getApplicationMetadata` response** to confirm how Policy/Location/Classification map to sections, entity names and Hierarchy Level.
2. How ISO form pages appear in runtime (separate page, section, or not shown).
3. Which Application Service version / data structure (`Common_V2`?) CU would use.
4. Transaction page flow (NB / quote / bind / endorse / renew) for the LOB: lives in `CNF_UIUX_WORKFLOW` / menu tables, not documented per-LOB here.
