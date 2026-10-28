import csv
import sys
from collections import Counter
from pathlib import Path

d = Path(sys.argv[1])


def load(name):
    with (d / name).open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


for st in ("AK", "CW"):
    P, F = load(f"frc_{st}_pages.csv"), load(f"frc_{st}_fields.csv")
    print(f"===== {st}: pages={len(P)} fields={len(F)}")
    print("by (depth,type):", sorted(Counter((int(p['Depth']), p['Type']) for p in P).items()))
    print("pages with fields by type:", Counter(p['Type'] for p in P if int(p['NFields']) > 0))
    print("-- depth<=1 non-Form pages")
    for p in P:
        if int(p["Depth"]) <= 1 and p["Type"] != "Form":
            print(f"  d{p['Depth']} {p['Type']:7} {p['Name']:28} tbl={p['TableName']:38} occ={p['MinOccurs']}/{p['MaxOccurs']} flds={p['NFields']} kids={p['NChildPages']} seq={p['Sequence']} hid={p['Hidden']} dm={p['DisplayMode']}")
    print("-- Form pages: depth distribution & children", Counter((int(p['Depth']), p['Type'], int(p['NFields']) > 0) for p in P if p['Type'] == 'Form'))

A = {p["Path"] for p in load("frc_AK_pages.csv")}
C = {p["Path"] for p in load("frc_CW_pages.csv")}
print("\nonly in CW:", len(C - A), sorted(C - A)[:8])
print("only in AK:", len(A - C), sorted(A - C)[:8])
