"""Check risk-page metadata. Run: py -I test_risk_page.py"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "lob-page"))
import test_lob_page as t  # noqa: E402

DETAIL_FIELDS = {"AircraftLiability": 7, "AutoDealers": 10, "BOP": 9, "CommercialAuto": 27, "EmployersLiability": 9,
                 "GeneralLiability": 20, "Liquor": 8, "OtherLiability": 8, "Watercraft": 7}   # FRC AK counts

for name in ("cu_risk_page", "cu_policy_detail", "cu_additional_coverage", "cu_risk_groups"):
    page = json.loads((HERE / f"{name}_metadata.json").read_text("utf-8"))
    for s in page["ApplicationDetail"]["SubApplicationDetailList"]:
        for a in s["AttributeDetailList"]:                       # State carries DependentComponent in the live sample
            a.pop("DependentComponent", None)
    assert t.shape_errs(page) == [], (name, t.shape_errs(page))

pd = json.loads((HERE / "cu_policy_detail_metadata.json").read_text("utf-8"))["ApplicationDetail"]["SubApplicationDetailList"][0]
assert [a["AttributeName"] for a in pd["AttributeDetailList"]][:2] == ["State", "RiskType"]
assert len(pd["AttributeDetailList"]) == 1 + 26 + 1
assert pd["EntityHierarchyName"] == "Policy"

subs = {s["TileName"]: s for s in json.loads((HERE / "cu_risk_groups_metadata.json").read_text("utf-8"))["ApplicationDetail"]["SubApplicationDetailList"]}
for g, n in DETAIL_FIELDS.items():
    assert len(subs[g]["AttributeDetailList"]) == 4 and subs[g]["Type"] == "Summary", g
    assert len(subs[g + "Detail"]["AttributeDetailList"]) == n + 1, (g, len(subs[g + "Detail"]["AttributeDetailList"]))   # + Save
    assert subs[g]["EntityHierarchyName"] == "CommercialUmbrella" + g

raw = "".join(p.read_text("utf-8") for p in HERE.glob("cu_*_metadata.json"))
assert "AMT_loggerToken" not in raw and "eyJ" not in raw       # no session tokens copied from pastes
print("ok: risk-page metadata matches SWP key shape and FRC field counts")

for name in ("cu_policy_detail", "cu_risk_groups"):                  # every Select must carry real options (a missing domain gave an empty list once)
    for s in json.loads((HERE / f"{name}_metadata.json").read_text("utf-8"))["ApplicationDetail"]["SubApplicationDetailList"]:
        for a in s["AttributeDetailList"]:
            if a["ComponentType"] == "SELECT":
                assert len(a["SubApplicationAttributeValueList"]) > 2 or a["AttributeName"] == "CoverageForm", (s["TileName"], a["AttributeName"])
print("ok: all Select fields have option lists")
