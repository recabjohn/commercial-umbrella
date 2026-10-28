"""Crime FRC (countrywide) -> crime_metadata.json for the Risk page Crime tab. FRC only.
Policy (22 fields) -> 7 group Summary pages (0..1) -> 1 Detail form each. Group visibility = Condition on the Summary page.
v2: adds (1) State on Policy (not in the Crime FRC - requested) and (2) 2 groups that exist only in DS (no FRC page): fields derived from DS columns, see ds_group().
usage: py -I build_crime_page.py <crime frc-data-full dir> <out json> <DS-CR-CW xml>
"""
import csv
import json
import re
import sys
from pathlib import Path

D, OUT, DS = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
import xml.etree.ElementTree as ET  # noqa: E402
STATES = "Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|District of Columbia|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Puerto Rico|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming".split("|")
CODES = "AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA PR RI SC SD TN TX UT VT VA WA WV WI WY".split()
# DS-only groups: DS table -> (group name, shown with Policy Type)   [policy-type link is an inference: same "...And Forgery" policy types]
DS_GROUPS = (("CrimeEmpTheftAndForgeryInsuringAgreements", "Employee Theft And Forgery", ["Commercial Fidelity And Forgery"]),
             ("CrimeGovernmentEmployeeTheftandForgeryInsuringAgreements", "Government Employee Theft And Forgery", ["Government Fidelity And Forgery"]))
rd = lambda n: list(csv.DictReader(open(D / f"CW_{n}.csv", encoding="utf-8")))  # noqa: E731
clean = lambda s: re.sub(r"<[^>]+>|&nbsp;", "", s).strip()  # noqa: E731


def domains() -> dict:
    """Entries sheet has 3 block layouts: plain (Seq,Display,Data,Status), keyed (Key,Seq,Display,Data), range (Key,Seq,Min,Max)."""
    keys = {r["Domain Table"]: r["Key"] for r in rd("domainkeys")}
    out, mode = {}, None
    for r in csv.reader(open(D / "CW_entries.csv", encoding="utf-8")):
        r += [""] * (5 - len(r))
        if r[0] in ("Table", "Domain Table"):
            continue
        if "Display Value" in r[2:4] or r[3] == "MinimumValue":
            mode = "range" if r[3] == "MinimumValue" else "keyed" if r[3] == "Display Value" else "plain"
            out[r[0]] = {"key": keys.get(r[0]) if mode != "plain" else None, "range": mode == "range", "items": []}
            continue
        if r[0] not in out:
            continue
        if mode == "plain":
            out[r[0]]["items"].append({"v": r[3], "d": r[2]})
        elif mode == "keyed":
            out[r[0]]["items"].append({"k": r[1], "v": r[4], "d": r[3]})
        else:
            out[r[0]]["items"].append({"k": r[1], "min": r[3], "max": r[4]})
    return out


def field(r: dict) -> dict:
    hdr = r["Comment"].startswith("Header") or "<u>" in r["Label"]
    return {"n": r["Field"], "t": "Subheading" if hdr else r["Type"], "l": clean(r["Label"]), "seq": int(r["Sequence"]),
            "req": r["Quote Required"] == "Yes", "reqCond": r["Required Condition"], "ro": r["Quote ReadOnly"] == "Yes",
            "cond": r["Condition"], "def": r["Default"], "dom": r["Domain Table"], "help": r["Help Text"]}


def nice(n: str) -> str:
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", n)


def ds_group(table: str, name: str, show: list, seq: int) -> dict:
    """No FRC page exists. Fields = DS columns ending Included/Limit/Ded (insured inputs); label = column name split into words (inference)."""
    t = next(x for x in ET.parse(DS).getroot().iter("Table") if x.findtext("Name") == table)
    cols = [c.findtext("Name") for c in t.findall("Column")]
    out, n = [], 100
    for c in cols:
        if not c.endswith("Included"):
            continue
        pre = c[:-8]
        out.append({"n": c, "t": "Radio", "l": nice(c), "seq": n, "req": True, "reqCond": "", "ro": False, "cond": "", "def": "No", "dom": "YesNo", "help": ""})
        for suf, typ, dom in (("Limit", "Text", "CoverageLimit"), ("Ded", "Select", "Ded")):
            if pre + suf in cols:
                n += 1
                out.append({"n": pre + suf, "t": typ, "l": "    " + suf.replace("Ded", "Deductible"), "seq": n, "req": True, "reqCond": f"{c}[.='Yes']", "ro": False,
                            "cond": f"{c}[.='Yes']", "def": "0" if suf == "Limit" else "", "dom": dom, "help": ""})
        n += 100
    return {"name": name, "table": table, "seq": seq, "max": "1", "showWhen": show, "summary": [{"n": "PolicyTermPremium", "t": "Text", "l": "Premium", "seq": 1, "req": False, "reqCond": "", "ro": True, "cond": "", "def": "", "dom": "", "help": ""}], "detail": out, "source": "DS only (no FRC page)"}


def forms() -> dict:
    """Policy-level Form pages (Parent=Policy) per package: Mandatory + Optional only. Conditional forms are attached by rules the FRC does not define (AttachmentCondition = Legacy)."""
    out = {}
    for tag in ("AL", "CW"):
        pages = csv.DictReader(open(D / f"{tag}_page.csv", encoding="utf-8"))
        out[tag] = [{"name": p["Name"], "number": p["Number"], "type": p["Form Type"], "cond": p["Condition"], "max": p["Max Occurs"]}
                    for p in sorted((p for p in pages if p["Parent"] == "Policy" and p["Type"] == "Form" and p["Form Type"] in ("Mandatory", "Optional")), key=lambda p: int(p["Sequence"]))]
    return out


def build() -> dict:
    page, flds = rd("page"), rd("fields")
    fl = lambda p: [field(r) for r in sorted((r for r in flds if r["Page"] == p), key=lambda r: int(r["Sequence"]))]  # noqa: E731
    groups = []
    for s in sorted((p for p in page if p["Parent"] == "Policy" and p["Type"] == "Summary"), key=lambda p: int(p["Sequence"])):
        g = s["Name"]
        groups.append({"name": g, "table": s["Table"], "seq": int(s["Sequence"]), "max": s["Max Occurs"],
                       "showWhen": sorted(set(re.findall(r"(?:Monoline|Package)PolicyType='([^']+)'", s["Condition"]))),
                       "summary": fl(g), "detail": fl(g + " Detail")})
    groups += [ds_group(t, g, show, 90000 + i) for i, (t, g, show) in enumerate(DS_GROUPS)]
    dom = domains()
    dom["__State"] = {"key": None, "range": False, "items": [{"v": c, "d": n} for c, n in sorted(zip(CODES, STATES), key=lambda x: x[1])]}
    state = {"n": "State", "t": "Select", "l": "State", "seq": 0, "req": True, "reqCond": "", "ro": False, "cond": "", "def": "", "dom": "__State", "help": ""}
    return {"source": "FRC-CR-CW-06012022-V01 + State (requested) + 2 DS-only groups", "policy": [state] + fl("Policy"), "groups": groups, "forms": forms(), "domains": dom}


if __name__ == "__main__":
    m = build()
    OUT.write_text(json.dumps(m, separators=(",", ":")), encoding="utf-8")
    print("wrote", OUT, len(m["policy"]), "policy fields;", [(g["name"], len(g["detail"])) for g in m["groups"]], len(m["domains"]), "domains")
