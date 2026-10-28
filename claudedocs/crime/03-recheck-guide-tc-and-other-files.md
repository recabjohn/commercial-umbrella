# Crime 03 - Recheck: guide, TC file and other ERC files (state and coverage questions)

Files read: guide (p.18 TC file, pp.21-25 RC/DS/hierarchy, p.80 Crime Hierarchy), `TC-CR-AL-06012022-V01.xlsx`, `DOC` (AL), `Readme.txt`, `RC-CR-AL` (Properties, Hierarchy, Page), `DS-CR-CW` (xml), `CrimeDeletionReport.xml` (CW), ALG sheet list. Not read in depth: AMF, RCRN, ALG rule bodies.

## State
- **TC file (AL) has no State input.** Input sheet: Policy (Multiple Named Insured, Entity Type, Legal Entity, Policy Type, Coverage Type, premises, employees, ERISA, Classification, SIC) -> Policy Form Summary (AL forms such as "Alabama Changes - Actual Cash Value" appear) -> Coinsurance -> Commercial Fidelity (summary) -> Commercial Fidelity Detail. The Policy fields equal the FRC Policy page.
- **RC Properties (AL):** Line of Business "Crime and Fidelity", State "Alabama". **Hierarchy:** "ISO Crime and Fidelity AL" sits on "ISO Crime and Fidelity Country Wide" on AscendantOne base content. Guide p.25: countrywide layer = multistate section; state layer = exceptions (State Exception section). Guide p.25: State column is blank in a countrywide file.
- **DS (CW):** table `Crime` (type policy, 149 columns) has columns `State` and `CPPGoverningState`. Not on the FRC Policy page, so a data column filled by the system/upstream, not a Crime screen field.
- **RC Page (AL):** the AL-only content on the screen side is forms only (Alabama Changes ...; Binding Arbitration forms marked CW-only in the other package).
- So: state is a package/data attribute. Not found as a Crime screen field in FRC, TC, or guide.

## Coverages and "Additional Coverage"
- **Coverages sit under each group**: in DS each group risk table has coverage-type child tables (Commercial Crime 27, Commercial Fidelity 19, Government Crime 18, Government Fidelity 17, Kidnap/Ransom 7, Commercial Fidelity And Forgery 5, Government Fidelity And Forgery 4, Employee Theft And Forgery 3, Government Employee Theft and Forgery 3), plus form children. Matches guide p.80 (Coverages + Forms under each group).
- Not found: any page/table/field named "Additional Coverage" in Crime FRC, DS table names, TC or guide p.80.

## Open point found
- DS has **9** group risk tables. FRC pages use **7**. Two DS tables carry the guide's exact names and have **no FRC page**: `CrimeEmpTheftAndForgeryInsuringAgreements` ("Employee Theft And Forgery") and `CrimeGovernmentEmployeeTheftandForgeryInsuringAgreements` ("Government Employee Theft and Forgery").
- FRC pages "Commercial Fidelity And Forgery" / "Government Fidelity And Forgery" use tables `CrimeCommlFidelityAndForgery...` / `CrimeGovtFidelityAndForgery...` (DS descriptions "Commercial Fidelity And Forgery", "Government  Fidelity And Forgery Insuring Agreements").
- So the guide's "Employee Theft & Forgery" matches the DS table name, not the FRC page name. Earlier assumption (FRC "Commercial Fidelity And Forgery" = guide "Employee Theft & Forgery") is now uncertain. Not found in the files: which one the screen should show.
- Also: DS shows risk-type child `CrimeCommlCrimePremises` under Commercial Crime (and one under Government Crime); no FRC page uses it (not found in Page sheet).
