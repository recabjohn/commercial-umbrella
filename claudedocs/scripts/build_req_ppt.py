"""Build the Commercial Umbrella screen-requirements deck (field -> source file) in the Renewal deck style.
Every number/field below is read from the exports in claudedocs/findings/frc-data-full and build/risk-page.

usage: py -I build_req_ppt.py <CU screen root> <out.pptx> <version label, e.g. v1>
"""
import csv
import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT, OUT, VER = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
FULL = ROOT / "claudedocs/findings/frc-data-full"
RISK = ROOT / "build/risk-page"

NAVY, GOLD, PANEL, TEXT, GREY = (RGBColor.from_string(c) for c in ("0B3B7A", "E8A317", "EEF2F9", "1F2937", "6B7280"))
ACCENTS = [RGBColor.from_string(c) for c in ("2272C3", "5B4BB0", "138A6B", "0B3B7A", "CC3340", "E8A317")]
DECK = "Commercial Umbrella"
HEADER = f"{DECK} · Screen Requirements · {VER}"
FOOTER = f"{DECK} · Screen Requirements · {VER} · Draft · Confidential"

# ---------- data ----------
def rd(name):
    return list(csv.DictReader(open(FULL / name, encoding="utf-8")))

FIELDS, PAGES = rd("AK_fields.csv"), rd("AK_page.csv")
DOM = json.loads((RISK / "domains.json").read_text("utf-8"))
RULES = json.loads((RISK / "cu_validation_rules.json").read_text("utf-8"))
DS = {(c[0], c[1]): c[2] for c in json.loads((FULL / "AK_ds_columns.json").read_text("utf-8"))["cols"]}
GROUPS = [(r["Name"], int(r["Max Occurs"])) for r in sorted(
    (p for p in PAGES if p["Parent"] == "Policy Detail" and p["Type"] == "Summary" and p["Name"] in (
        "Aircraft Liability", "Auto Dealers", "BOP", "Commercial Auto", "Employers Liability", "General Liability", "Liquor", "Other Liability", "Watercraft")),
    key=lambda p: int(p["Sequence"]))]
POLICY = [f for f in FIELDS if f["Page"] == "Policy Detail"]
DETAIL = {g: [f for f in FIELDS if f["Page"] == f"{g} Detail"] for g, _ in GROUPS}
MINE = POLICY + [f for g, _ in GROUPS for f in FIELDS if f["Page"] in (g, f"{g} Detail")]


def clean(s):
    import re
    return re.sub(r"<[^>]+>|&nbsp;", "", s).strip()


def plain(c):
    if not c:
        return "Always"
    if "PackagePolicy" in c:
        return "Package policy only"
    if c.startswith("PolicyCoverageForm[.='Commercial Excess"):
        return "Excess form, or both forms"
    if c.startswith("PolicyCoverageForm[.='Commercial Umbrella"):
        return "Umbrella form, or both forms"
    if c.startswith("TRIPTerminates"):
        return "TRIP ends early = Yes"
    if c == "TerrorismCoverage[.='No']":
        return "Terrorism coverage = No"
    if "SpecificLimitations ='No'" in c:
        return "Terrorism = Yes, or No with specific limits = No"
    if "SpecificLimitations ='Yes'" in c:
        return "Terrorism = Yes, or No with specific limits = Yes"
    return c


# ---------- drawing helpers ----------
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
page_no = [0]


def box(sl, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE):
    s = sl.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.shadow.inherit = False
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
    return s


def text(sl, x, y, w, h, t, size=16, bold=False, color=TEXT, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False):
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap, tf.vertical_anchor = True, anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    lines = t if isinstance(t, list) else [t]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = ln
        r.font.size, r.font.bold, r.font.italic, r.font.name = Pt(size), bold, italic, "Calibri"
        r.font.color.rgb = color
        p.space_after = Pt(4)
    return tb


def slide(title, source=None, notes=None):
    sl = prs.slides.add_slide(BLANK)
    page_no[0] += 1
    box(sl, 0, 0, 13.333, 1.05, NAVY)
    text(sl, 0.55, 0.28, 10.5, 0.6, title, 30, True, RGBColor(255, 255, 255))
    text(sl, 9.0, 0.06, 4.2, 0.3, HEADER, 10, color=RGBColor(255, 255, 255), align=PP_ALIGN.RIGHT)
    text(sl, 0.5, 7.12, 10.5, 0.3, FOOTER, 10, color=GREY)
    text(sl, 12.2, 7.12, 0.7, 0.3, str(page_no[0]), 10, color=GREY, align=PP_ALIGN.RIGHT)
    if source:
        text(sl, 0.5, 6.72, 12.3, 0.35, "Source: " + source, 11, color=GREY, italic=True)
    if notes:
        sl.notes_slide.notes_text_frame.text = notes
    return sl


def table(sl, x, y, w, cols, rows, widths, size=11, row_h=0.34, head_h=0.38):
    gs = sl.shapes.add_table(len(rows) + 1, len(cols), Inches(x), Inches(y), Inches(w), Inches(head_h + row_h * len(rows)))
    tb = gs.table
    tb.first_row = True
    for i, wd in enumerate(widths):
        tb.columns[i].width = Inches(wd)
    tb.rows[0].height = Inches(head_h)
    for r in range(1, len(rows) + 1):
        tb.rows[r].height = Inches(row_h)
    for c, name in enumerate(cols):
        cell(tb.cell(0, c), name, size, True, RGBColor(255, 255, 255), NAVY)
    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            cell(tb.cell(r, c), val, size, False, TEXT, PANEL if r % 2 == 0 else RGBColor(255, 255, 255))
    return tb


def cell(c, val, size, bold, color, fill):
    c.fill.solid()
    c.fill.fore_color.rgb = fill
    c.margin_left = c.margin_right = Inches(0.06)
    c.margin_top = c.margin_bottom = Inches(0.025)
    c.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = c.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = str(val)
    r.font.size, r.font.bold, r.font.name = Pt(size), bold, "Calibri"
    r.font.color.rgb = color


def cards(sl, items, x0=0.55, y0=1.45, cols=2, w=5.95, h=1.5, gap=0.25, size=17):
    for i, it in enumerate(items):
        x, y = x0 + (i % cols) * (w + gap), y0 + (i // cols) * (h + gap)
        box(sl, x, y, w, h, PANEL)
        box(sl, x, y, 0.1, h, ACCENTS[i % len(ACCENTS)])
        text(sl, x + 0.25, y, w - 0.4, h, it, size, anchor=MSO_ANCHOR.MIDDLE)


# ---------- slides ----------
# 1 title
sl = prs.slides.add_slide(BLANK)
page_no[0] += 1
box(sl, 0, 0, 13.333, 7.5, NAVY)
text(sl, 0.95, 1.55, 11, 0.4, "COMMERCIAL UMBRELLA  ·  POLICY SCREEN", 15, True, RGBColor(190, 205, 235))
text(sl, 0.95, 2.1, 11.4, 1.8, "Screen Requirements — Which Fields, From Which File", 42, True, RGBColor(255, 255, 255))
box(sl, 0, 5.18, 13.333, 0.06, GOLD)
text(sl, 0.95, 5.45, 11.4, 0.4, f"Source files: ISO ERC package CU-AK and CU-CW dated 12/01/2020 V01  ·  {VER} · Draft", 14, color=RGBColor(255, 255, 255))

# 2 what we built
sl = slide("What We Built", "Prototype in build/lob-page and build/risk-page; live copy at commercialumbrella.vercel.app")
cards(sl, [
    "Page 1: Line Of Business — choose General Liability, Commercial Automobile, Commercial Property or Commercial Umbrella",
    "Page 2: Risk/Coverage — add a State, fill the Policy, then add underlying insurance",
    f"Policy page has {len(POLICY)} fields; underlying insurance has {len(GROUPS)} groups and {sum(len(v) for v in DETAIL.values())} detail fields",
    "Checks and messages come from the rules in the ERC files, not from our own ideas",
    "Look and flow copy the General Liability screens you showed us",
    "Forms and endorsements are left out for now (see Left Out and Why)",
], h=1.45)

# 3 sources
sl = slide("Where the Information Came From", "File names in the last slide; descriptions of each file from the package Readme.txt", notes=(
    "FRC = Addition-Inheritance Full Content report; DS = Data structure; ALG = Algorithms; TC = Sample Test Case; DOC = State Refer to Company & Unsupported Rules; "
    "RC = Addition-Deletion Content report. All descriptions quoted from Readme.txt in the ERC package."))
table(sl, 0.5, 1.3, 12.35, ["File", "Sheet or part we read", "What we took from it"], [
    ["ISO ERC Suite Product Guide (PDF)", "Hierarchy pictures, p.79 (CU), p.82 (GL); Page / Page Field / Domain sections", "How a CU product is laid out; what each ERC sheet means"],
    ["FRC (full content) CU-AK, CU-CW", "Page, Page Fields, Domain Tables, Domain Table Keys, Domain Table Entries", "Pages, fields, labels, required, defaults, dropdown lists, show/hide conditions"],
    ["DS (data structure) CU-AK", "Column Details", "Field type and size (number, date, text length)"],
    ["ALG (algorithms) CU-AK, human readable", "Err-* sheets and ErrorMessages", "Check rules and their exact messages"],
    ["TC (sample test case), DOC", "Input; Refer to Company", "Sample values and manual-rating notes (reference only)"],
    ["General Liability and SWP screens you sent", "Page data, screenshots", "Screen flow: State, then Policy, then lower levels; page look"],
    ["Web: ACORD 131, ISO CU DS 01", "Public form descriptions", "Cross-check only: umbrella = policy + one list of underlying policies"],
], [3.5, 4.55, 4.3], size=11, row_h=0.62)
text(sl, 0.5, 6.15, 12.3, 0.5, "Read but not used for screens: RC (changes report), AMF feed, release notes, ALG rating sheets, rating tables.", 12, color=GREY)

# 4 hierarchy diagram
sl = slide("How the Screen Is Organised", "Guide p.79; FRC Page sheet (Parent column); General Liability screens", notes=(
    "Level 1 CommercialUmbrella = Page sheet: 'Policy Detail' table CommercialUmbrella. Level 3 groups = Page sheet rows Type=Summary whose Parent is 'Policy Detail'. "
    "State level is an INFERENCE from the General Liability screens: the FRC has no State field because states are separate files (CU-AK, CU-CW)."))
def node(x, y, w, h, t, sub, fill):
    box(sl, x, y, w, h, fill)
    text(sl, x, y + 0.05, w, h * 0.55, t, 15, True, RGBColor(255, 255, 255), PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    text(sl, x, y + h * 0.5, w, h * 0.5, sub, 10.5, False, RGBColor(235, 240, 250), PP_ALIGN.CENTER)
node(0.7, 1.5, 3.4, 0.95, "Commercial Umbrella", "LOB page checkbox", ACCENTS[3])
node(4.5, 1.5, 3.4, 0.95, "Policy (one per State)", "Policy Detail page", ACCENTS[0])
node(8.3, 1.5, 4.3, 0.95, "Underlying insurance", "9 groups, direct children of Policy", ACCENTS[2])
for x in (4.12, 7.92):
    text(sl, x - 0.02, 1.62, 0.45, 0.6, "▶", 18, False, GREY, PP_ALIGN.CENTER)
for i, (g, mx) in enumerate(GROUPS):
    x, y = 0.7 + (i % 3) * 4.1, 3.0 + (i // 3) * 1.15
    box(sl, x, y, 3.9, 0.95, PANEL)
    box(sl, x, y, 0.09, 0.95, ACCENTS[i % 6])
    text(sl, x + 0.2, y + 0.08, 3.6, 0.4, f"{i + 1}. {g}", 15, True)
    text(sl, x + 0.2, y + 0.5, 3.6, 0.4, f"Summary table + Detail form · {'1 row only' if mx == 1 else 'many rows'}", 11.5, color=GREY)
text(sl, 0.7, 6.4, 12, 0.35, "No Location or Classification level, unlike General Liability.", 13, True, NAVY)

# 5 why
sl = slide("Why This Hierarchy", "Guide p.79 and p.82; FRC Page sheet; user-supplied General Liability metadata; ACORD 131; ISO CU DS 01")
table(sl, 0.5, 1.3, 12.35, ["Evidence", "File", "What it shows"], [
    ["Guide diagram for CU", "ISO ERC Suite Product Guide p.79", "Flat: Policy with Forms, Coverages and 8 risk groups. No Location level"],
    ["FRC page tree", "FRC Page sheet", f"{len(GROUPS)} risk groups under Policy Detail. Adds Auto Dealers and Other Liability; has no Garage (guide lists Garage)"],
    ["Groups come in a fixed order", "FRC Page sheet, Sequence column", "Order and row limits (Auto Dealers = 1 row, others many) taken from the sheet"],
    ["General Liability screens", "SWP_1_3_V1 metadata and screenshots you sent", "State → Policy → Location → Classification. Each level opens in place with a Save"],
    ["Industry forms", "ACORD 131; ISO CU DS 01 (web)", "Umbrella = policy details + one list of underlying policies. Agrees with the flat layout"],
    ["State level", "General Liability screens (inference)", "FRC has no State field; CU-AK and CU-CW are separate state files. Kept State as the first step"],
], [2.9, 3.9, 5.55], size=11.5, row_h=0.72)

# 6 LOB page
sl = slide("Line Of Business Page", "SWP LOB page metadata and screenshots you sent; build/lob-page/cu_lob_page_metadata.json", notes=(
    "The CU checkbox is the only addition; the other three (General Liability, Commercial Automobile, Commercial Property) are the SWP page's own. Next stays locked until one is ticked. "
    "Sample Details values (agency, submission number) are from the pasted test data, not real data."))
table(sl, 0.5, 1.3, 12.35, ["Item on the page", "Value", "Where it came from"], [
    ["Checkbox 1–3", "General Liability, Commercial Automobile, Commercial Property", "SWP Line Of Business page (your metadata)"],
    ["Checkbox 4", "Commercial Umbrella", "Added by us for this product"],
    ["Details strip", "Agency Name, Agent Name, Submission Number, Submission Status, Insured Name", "SWP ExpandPanel metadata"],
    ["Steps bar", "Agency & Agent, Insured Details, Line Of Business, Risk/Coverage, Program Selection", "SWP page (breadcrumb)"],
    ["Buttons", "Previous, Next (Next locked until a box is ticked)", "SWP Navigation buttons metadata"],
], [2.6, 5.4, 4.35], size=12, row_h=0.8)

# 7 state & policy page
sl = slide("State and Policy Page", "General Liability metadata (State, then Subline, then fields); FRC Page Fields sheet, page 'Policy Detail'")
cards(sl, [
    "Step 1: only State is shown (list of states from the General Liability screen)",
    f"Step 2: after a State is picked, the {len(POLICY)} Policy fields appear",
    "Step 3: Save the Policy. Then Additional Coverages and the Risk Schedule appear",
    "No Subline for Commercial Umbrella: no Subline field in the FRC (open point: confirm)",
], h=1.55)

# 7a/7b risk page: part -> file
sl = slide("Risk Page — Where Each Part Came From (1 of 2)", "Files in CUP Batch 1 ERC Files; column names are the column headers in each sheet", notes=(
    "FRC = FRC-CU-AK-12012020-V01.xlsx (AK) and FRC-CU-CW-12012020-V01.xlsx (CW). On the pages used here AK and CW are identical (167 fields)."))
table(sl, 0.4, 1.2, 12.55, ["Part of the Risk page", "File", "Sheet → column"], [
    ["Policy fields: which fields, labels, order", "FRC-CU-AK / CU-CW", "Page Fields → Page = Policy Detail; Field, Label, Sequence"],
    ["Required stars and default values", "FRC-CU-AK / CU-CW", "Page Fields → Quote Required, Required Condition, Default"],
    ["Show / hide rules (for example Excess limits)", "FRC-CU-AK / CU-CW", "Page Fields → Condition, Display Controller"],
    ["Section headings (Premium 1st–5th Million)", "FRC-CU-AK / CU-CW", "Page Fields → Comment = Header"],
    ["Hint text on Terrorism field; number ranges", "FRC-CU-AK / CU-CW", "Page Fields → Help Text; Min, Max"],
    ["Dropdown values (limits, forms, legal entity, yes/no)", "FRC-CU-AK / CU-CW", "Domain Tables, Domain Table Entries → Display Value, DataValue"],
    ["The 9 underlying-insurance groups, their order, 1 row or many", "FRC-CU-AK / CU-CW", "Page → Parent = Policy Detail, Type = Summary; Sequence, Max Occurs"],
    ["Table columns of each group (Carrier, Policy Number, dates)", "FRC-CU-AK / CU-CW", "Page Fields → Page = <group> (Summary page)"],
    ["Detail form of each group", "FRC-CU-AK / CU-CW", "Page Fields → Page = <group> Detail"],
], [4.6, 2.5, 5.45], size=11, row_h=0.5)
sl = slide("Risk Page — Where Each Part Came From (2 of 2)", "Files named in the table; items marked 'ours' are our own choice, not taken from a file")
table(sl, 0.4, 1.2, 12.55, ["Part of the Risk page", "File", "Sheet or part"], [
    ["Number, date and text-length limits on fields", "DS-CU-AK-12012020-V01.xlsx", "Column Details → Type, Size, Scale"],
    ["Messages such as 'Underlying Liability Premium Must Be Greater Than 0'", "ALG-CU-AK-12012020-V01_HR.xlsx", "Err-<group> sheets, ErrorMessages"],
    ["State list (52 states) and State → Policy order", "General Liability Policy page data you sent (SWP_1_3_V1)", "PolicyDetail State field and its values"],
    ["Additional Coverages table; Risk Schedule section; row opens in place; Save button", "General Liability page data and screenshots you sent", "AdditionalCoverage, Location, Classification pages"],
    ["Step bar, Details strip, Previous / Next, note text", "SWP Line Of Business and Risk pages you sent", "ExpandPanel, NavigationButtons, LocationValidation"],
    ["Page look: header, side menu, colours", "endo-nav site you pointed us to (index.html)", "Style rules copied and trimmed"],
    ["Sample Details values (agency, submission number)", "Test data in the pages you sent", "Sample only, not real data"],
    ["Next unlocks after one Policy and one underlying row (ours)", "Note text on the SWP page", "Our reading of the note"],
    ["Save and delete event names, ids, parent key (ours)", "No file yet", "Placeholders until the real setup exists"],
], [4.6, 3.9, 4.05], size=11, row_h=0.5)

# 8 policy fields
sl = slide("Policy Fields — Cover and Limits", "FRC Page Fields sheet, page 'Policy Detail' (Quote Required, Default, Domain Table, Condition columns)", notes=(
    "Columns read: Field, Label, Type, Quote Required, Required Condition, Default, Domain Table, Condition. Premium rows are on the next slide."))
prem = lambda f: "Premium" in f["Field"]
rows = []
for f in (x for x in POLICY if not prem(x)):
    req = "Yes" if f["Quote Required"] == "Yes" else "No"
    if f["Required Condition"]:
        req += " (when shown)"
    vals = f["Domain Table"] or ("Date" if "Date" in f["Field"] else "Free text")
    rows.append([clean(f["Label"]), f["Type"], req, f["Default"] or "—", vals, plain(f["Condition"])])
table(sl, 0.4, 1.2, 12.55, ["Label", "Type", "Required", "Default", "List", "Shown when"], rows,
      [4.7, 0.65, 1.2, 1.3, 1.7, 3.0], size=9.5, row_h=0.34, head_h=0.34)

# 9 premium rows
sl = slide("Policy Fields — Premium Rows", "FRC Page Fields sheet, page 'Policy Detail'; Comment column = 'Header'")
pr = [f for f in POLICY if prem(f)]
table(sl, 0.5, 1.3, 12.35, ["Row", "Count", "Shown as", "Shown when"], [
    ["Commercial Umbrella Premium 1st to 5th Million (heading + Premium)", str(sum(1 for f in pr if "Million" in f["Field"])), "Heading, then a read-only Premium line", plain(next(f for f in pr if f["Field"] == "Premium1stMillion")["Condition"])],
    ["Excess Liability Manual Premium", "1", "Entered amount, required", plain(next(f for f in pr if "ManualPremium" in f["Field"])["Condition"])],
    ["Excess Liability Premium", "1", "Read-only Premium line", plain(next(f for f in pr if f["Field"].endswith("ExcessLiabilityCoverage.PolicyTermPremium"))["Condition"])],
], [5.2, 1.0, 3.2, 2.95], size=12, row_h=0.8)
text(sl, 0.5, 4.5, 12.3, 1.2, ["The five 'Million' headings are section headings, not entry fields (FRC Comment column says Header).",
                               "Premium amounts are worked out by rating, which this prototype does not do, so they stay blank."], 14)

# 10 conditions
sl = slide("When a Field Shows or Is Required", "FRC Page Fields sheet: Condition, Required Condition and Display Controller columns")
conds = sorted({f["Condition"] for f in POLICY if f["Condition"]})
rows = []
for c in conds:
    rows.append([plain(c), ", ".join(clean(f["Label"])[:34] for f in POLICY if f["Condition"] == c)[:150]])
table(sl, 0.5, 1.3, 12.35, ["Rule", "Fields it controls"], rows, [4.2, 8.15], size=11, row_h=0.62)
ctrl = [clean(f["Label"])[:30] for f in POLICY if f["Display Controller"] == "Yes"]
text(sl, 0.5, 6.0, 12.3, 0.6, f"Fields that change what else shows (Display Controller = Yes): {len(ctrl)}. Two also trigger re-rating when changed: Policy Coverage Form and Accept Certified Acts of Terrorism.", 12, color=GREY)

# 11 groups
sl = slide("Underlying Insurance — Nine Groups", "FRC Page sheet (Sequence, Max Occurs); FRC Page Fields sheet (field counts)")
rows = []
for i, (g, mx) in enumerate(GROUPS, 1):
    pg = next(p for p in PAGES if p["Name"] == g and p["Type"] == "Summary")
    rows.append([str(i), g, pg["Sequence"], "1 row" if mx == 1 else "Many", "4", f"{len(DETAIL[g])} ('{g} Detail')"])
table(sl, 0.5, 1.3, 12.35, ["Order", "Group (FRC page)", "FRC sequence", "Rows allowed", "Table columns", "Detail fields (FRC page)"], rows,
      [0.8, 3.0, 1.5, 1.6, 1.6, 3.85], size=12, row_h=0.46)
text(sl, 0.5, 5.9, 12.3, 0.7, "Table columns on every group: Carrier, Policy Number, Effective Date, Expiration Date (FRC Summary page).", 13, color=NAVY)

# 12 what each group asks
sl = slide("What Each Group Asks", "FRC Page Fields sheet, pages '<group> Detail'")
common = {"UnderlyingPolicyType", "NameID", "UnderlyingPolicyNumber", "UnderlyingEffectiveDate", "UnderlyingExpirationDate"}
rows = []
for g, _ in GROUPS:
    labs = list(dict.fromkeys(clean(f["Label"]) for f in DETAIL[g] if f["Field"] not in common))
    s = "; ".join(labs[:5]) + (f"; plus {len(labs) - 5} more" if len(labs) > 5 else "")
    rows.append([g, f"{len(DETAIL[g])} fields in all. After the common ones: " + s])
table(sl, 0.5, 1.25, 12.35, ["Group", "Fields after the 5 common ones (type, carrier, policy no., dates)"], rows, [2.4, 9.95], size=10, row_h=0.56)

# 13 lists
sl = slide("Dropdown Lists", "FRC Domain Tables and Domain Table Entries sheets; Page Fields 'Domain Table' column")
used = {}
for f in MINE:
    if f["Domain Table"]:
        used[f["Domain Table"]] = used.get(f["Domain Table"], 0) + 1
rows = [[k, str(len(DOM[k])), str(v), ", ".join(DOM[k][:3]) + ("…" if len(DOM[k]) > 3 else "")] for k, v in sorted(used.items())]
table(sl, 0.5, 1.3, 12.35, ["List name", "Values", "Fields using it", "First values"], rows, [3.4, 1.2, 1.9, 5.85], size=12, row_h=0.46)
text(sl, 0.5, 5.7, 12.3, 0.7, "Value shown = value stored for every entry. The five keyed lists (County, City, and so on) are not used by any Commercial Umbrella field.", 12, color=GREY)

# 14 formats
sl = slide("Field Format Rules", "DS (data structure) CU-AK, sheet Column Details; matched to FRC fields by table and field name")
cnt = {}
for f in MINE:
    t = DS.get((f["Field Table Name"], f["Field"]))
    if t in ("Decimal", "Integer", "Date", "Text"):
        cnt[t] = cnt.get(t, 0) + 1
rows = [["Decimal (10 digits, 2 after the point)", "Premiums and amounts", str(cnt.get("Decimal", 0)), "Number box, steps of 0.01"],
        ["Date", "Effective and expiration dates", str(cnt.get("Date", 0)), "Date picker"],
        ["Text (80 or 128 characters)", "Policy number, labels", str(cnt.get("Text", 0)), "Text box with a length limit"],
        ["Integer", "Counts, such as number of vehicles", str(cnt.get("Integer", 0)), "Whole-number box"]]
table(sl, 0.5, 1.3, 12.35, ["Data type", "Typical use", "Fields on our pages", "On screen"], rows, [4.0, 3.4, 2.0, 2.95], size=12, row_h=0.7)
text(sl, 0.5, 4.9, 12.3, 1.0, ["Min and Max on the FRC (for example 0 to 99,999,999) set the allowed range.",
                               "Fields found in neither file default to plain text."], 13)

# 15 checks
sl = slide("Checks and Messages", "ALG CU-AK (human readable), sheets Err-<group> and ErrorMessages; wording copied as written")
rows = []
for g, rs in RULES["groups"].items():
    for r in rs:
        rows.append([g, r["msg"]])
rows.append(["Policy", RULES["policy"][0]["msg"]])
table(sl, 0.5, 1.25, 12.35, ["Where", "Message shown"], rows, [3.0, 9.35], size=10.5, row_h=0.37)

# 16 left out
sl = slide("Left Out and Why", "FRC Page sheet (Type = Form); DS Tables sheet; your instruction to ignore forms for now")
forms = sum(1 for p in PAGES if p["Type"] == "Form")
cards(sl, [
    f"Forms and endorsements: {forms} form pages in the FRC, left out as you asked",
    "Form rules (for example, only one of two forms can be attached): belong to the form pages",
    "Premium calculation: the ALG rating sheets are not read; premiums stay blank",
    "No FRC pages for Garage, Underlying Liability, Payments, Electronic Signature, Quote Letter (they exist only in DS)",
    "Risk Type: hidden, it needs a Package Policy field that is not on the page",
    "Additional Coverages window: shown as an empty table only",
], h=1.45, size=15)

# 17 assumptions
sl = slide("Assumptions and Open Points", "Our own notes; each item is unconfirmed until someone with the Builder setup checks it")
cards(sl, [
    "No Subline field. The platform may still need a fixed Subline value behind the scenes",
    "State shown as a list on the Policy page; the ERC has no State field (state is the file)",
    "Event names, ids and product name are placeholders until the real setup exists",
    "Only the 12/01/2020 package was read; newer 2023 and 2026 CU packages are not compared",
    "CU-AK and CU-CW are identical on these pages; they differ only on form pages",
    "Carrier is a text box here; the ERC marks it as a lookup button",
], h=1.45, size=15)

# 18 sources appendix
sl = slide("Source Files", "Folder: CUP Batch 1 ERC Files; other items as listed")
table(sl, 0.5, 1.25, 12.35, ["File", "Used for"], [
    ["FRC-CU-AK-12012020-V01.xlsx / FRC-CU-CW-12012020-V01.xlsx", "Pages, fields, lists, conditions"],
    ["DS-CU-AK-12012020-V01.xlsx", "Field types and sizes"],
    ["ALG-CU-AK-12012020-V01_HR.xlsx", "Check rules and messages"],
    ["TC-CU-AK-12012020-V01.xlsx; DOC-CU-AK-12012020-V01.xlsx", "Reference only"],
    ["ISO ERC Suite Product Guide (PDF, Oct 2019)", "Hierarchy pictures, sheet meanings"],
    ["SWP_1_3_V1 page data and screenshots (Line Of Business, Policy, Location, Classification)", "Screen flow and look"],
    ["Our notes: claudedocs/findings 01–06", "Full reasoning for every decision"],
], [8.0, 4.35], size=12, row_h=0.6)

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(OUT)
print("saved", OUT, page_no[0], "slides")
