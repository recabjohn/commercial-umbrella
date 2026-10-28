"""Lookup data for the Underlying Policy fields (Carrier, Underlying Policy Number), per LOB group.
Source: the underlying policy header values in the AK / KY / AR Test Case workbooks (same data as make_samples.py).
Writes lookup.json = {group: [{carrier, number, eff, exp}]}.   usage: py -I make_lookup.py"""
import importlib.util
import json
from pathlib import Path

here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("make_samples", here / "make_samples.py")
ms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ms)

out: dict = {}
for sample in ms.SAMPLES.values():
    for r in sample["rows"]:
        v = r["v"]
        e = {"carrier": v["NameID"], "number": v["UnderlyingPolicyNumber"], "eff": v["UnderlyingEffectiveDate"], "exp": v["UnderlyingExpirationDate"]}
        lst = out.setdefault(r["g"], [])
        if e not in lst:
            lst.append(e)
# Extra made-up sample policies (NOT from the TCs) so the lookup has more to pick from; fictional carriers.
PREFIX = {"Aircraft Liability": "AV", "BOP": "BP", "Commercial Auto": "CA", "Auto Dealers": "AD", "General Liability": "GL",
          "Employers Liability": "EL", "Liquor": "LQ", "Watercraft": "WC", "Other Liability": "OL"}
CARRIERS = ["Prime Insurance", "Solartis Insurance", "Northwind Mutual", "Summit Insurance Co", "Harbor Specialty",
            "Lakeshore Casualty", "Evergreen Mutual", "Crestview Indemnity"]
for g, pre in PREFIX.items():
    lst = out.setdefault(g, [])
    for i, c in enumerate(CARRIERS):
        for j, (eff, exp) in enumerate((("2026-01-01", "2027-01-01"), ("2026-08-01", "2027-08-01"), ("2026-03-15", "2027-03-15"))):
            lst.append({"carrier": c, "number": f"{pre}-{100231 + i * 111 + j * 7}", "eff": eff, "exp": exp})
(here / "lookup.json").write_text(json.dumps(out, indent=1), "utf-8")
print({g: len(v) for g, v in out.items()})
