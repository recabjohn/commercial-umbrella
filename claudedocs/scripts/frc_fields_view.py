import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

d = Path(sys.argv[1])
st = "AK"
F = list(csv.DictReader((d / f"frc_{st}_fields.csv").open(encoding="utf-8")))
P = list(csv.DictReader((d / f"frc_{st}_pages.csv").open(encoding="utf-8")))
D = {r["Name"]: r for r in csv.DictReader((d / f"frc_{st}_domains.csv").open(encoding="utf-8"))}


def show(path):
    print(f"\n## {path}")
    for f in F:
        if f["PagePath"] == path:
            print(f"  {f['Sequence']:>5} {f['ColumnName'][:48]:48} {f['Type']:10} lbl={f['Label'][:34]!r:36} Q(d/r/ro)={f['QuoteDisplay']}/{f['QuoteRequired']}/{f['QuoteReadOnly']} P(d/r/ro)={f['PolicyDisplay']}/{f['PolicyRequired']}/{f['PolicyReadOnly']} dom={f['DomainTableName']} cond={f['Condition'][:40]!r} req={f['RequiredCondition'][:40]!r}")


show("Policy Detail")
for risk in ("Aircraft Liability", "Commercial Auto", "General Liability"):
    show(f"Policy Detail/{risk}")
    show(f"Policy Detail/{risk}/{risk} Detail")

# Do all risk Detail pages share one field set?
sets = defaultdict(list)
for p in P:
    if p["Type"] == "Detail" and p["Depth"] == "2":
        cols = tuple(f["ColumnName"] for f in F if f["PagePath"] == p["Path"])
        sets[cols].append(p["Name"])
print("\n## distinct risk Detail field sets:", len(sets))
for cols, names in sets.items():
    print(len(cols), "fields ->", names)

print("\n## Policy Detail field type counts:", Counter(f["Type"] for f in F if f["PagePath"] == "Policy Detail"))
print("## Domain tables total:", len(D), Counter(r["Type"] for r in D.values()))
used = {f["DomainTableName"] for f in F if f["DomainTableName"]}
print("## domain tables referenced by fields:", len(used), "| not referenced:", len(set(D) - used))
print("## sample domains:", [(n, D[n]["Type"], D[n]["NEntries"], D[n]["NKeys"]) for n in list(D)[:12]])
