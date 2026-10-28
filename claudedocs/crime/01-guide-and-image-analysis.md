# Crime 01 - ISO guide and your image (guide only, no ERC files)

Sources: `Crime/ISO ERC Suite Product Guide - October 2019 version for Parser 4.0.8.pdf` (same PDF as CU; converted text `source-md/iso-erc-suite-product-guide.md`, page image `source-md/pages/p80.png`) and `Crime/image (3).png`.

## 0. Recheck (PDF searched page by page, PDF page number = printed page number)
Crime / Fidelity / Kidnap / Forgery / Extortion appear only on **pp.3 (contents), 5 (line list), 77 (CPP picture), 80 (Crime Hierarchy)**. Nothing else in the 83 pages is Crime-specific. Image text equals p.80 text word for word.

## 1. The image
- It is **guide p.80, "Crime Hierarchy"** (cropped). Checked against the rendered page: same boxes, same names, same layout.
- Shows: **Crime (Quote or Policy)** at the top, 7 boxes under it, each with two small boxes: **Coverages** and **Forms**.
- The 7 boxes: Commercial Fidelity; Commercial Crime; Employee Theft & Forgery; Government Fidelity; Government Crime; Government Employee Theft and Forgery; Kidnap/Ransom and Extortion.

## 2. What the guide says that applies
| Point | Guide location | Meaning for Crime |
|---|---|---|
| One policy per record; risks, forms and coverages hang off the policy | Types of Tables, p.21 | Crime = one Policy level with children |
| Policy page -> children are risk pages or form pages; risks = pages of type Summary whose parent is the policy; forms = type Form | pp.44-45 (Page tab; example for Commercial Property on p.49) | How to find the groups in the FRC: filter Summary under the policy page, ignore forms |
| "The majority of pages ... are forms" | p.44 | Same as CU: forms are most of the pages |
| Crime is one of the lines ERC covers (p.5) and is one of 5 lines directly under the Commercial Package Policy (Commercial Auto, Crime, Inland Marine, General Liability, Commercial Property; CU is not drawn there) | p.5, p.77 | Crime can sit inside a package policy |
| Hierarchy pictures are shown for BOP p.73, CU p.79, Crime p.80 ... | pp.73-83 | Pictures show structure, not fields |

## 3. How Crime differs from CU in the guide
| | CU (p.79) | Crime (p.80) |
|---|---|---|
| Policy-level children | Forms, Coverages, then 8 risk groups side by side | 7 groups only |
| Forms and Coverages | one box each, at policy level | one **Coverages** and one **Forms** box under **each** group |
| Group names | Aircraft, BOP, Commercial Auto, ... | Fidelity / Crime / Theft & Forgery, Commercial and Government, plus Kidnap/Ransom and Extortion |
| Levels below groups | none drawn | none drawn (Coverages and Forms are leaf boxes) |

## 4. What the guide does NOT say
- Whether a group allows one or many rows, field lists, labels, required flags, or what a "Coverages" box contains (page, table or field). The picture shows no Location or other schedule level.
- Anything about State or multi-state for Crime (guide only covers state/countrywide packaging, same as CU).

## 5. Open for the next step (ERC files, not guide)
- Check the FRC page tree against this picture (first look already done, see README: 7 Summary groups under Policy; names differ for the two "Employee Theft" boxes).
- Find where "Coverages" live in the FRC (fields on each group's Detail page, or separate pages).
