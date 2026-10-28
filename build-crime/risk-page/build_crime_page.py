"""Crime FRC (countrywide) -> crime_metadata.json for the Risk page Crime tab. FRC only.
Policy (22 fields) -> 7 group Summary pages (0..1) -> 1 Detail form each. Group visibility = Condition on the Summary page.
usage: py -I build_crime_page.py <crime frc-data-full dir> <out json>
"""
import csv
import json
import re
import sys
from pathlib import Path

D, OUT = Path(sys.argv[1]), Path(sys.argv[2])
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
    return {"source": "FRC-CR-CW-06012022-V01 (Page, Page Fields, Domain Tables/Keys/Entries)", "policy": fl("Policy"), "groups": groups, "forms": forms(), "domains": domains()}


if __name__ == "__main__":
    m = build()
    OUT.write_text(json.dumps(m, separators=(",", ":")), encoding="utf-8")
    print("wrote", OUT, len(m["policy"]), "policy fields;", [(g["name"], len(g["detail"])) for g in m["groups"]], len(m["domains"]), "domains")
