"""Local-only preview: the CU screens pre-filled with the AK Test Case (TC-CU-AK-12012020-V01.xlsx, 'Input' sheet).
Values below are copied from that sheet (labels mapped to the screen's attribute names). Nothing here is deployed and the real
screen defaults are untouched: start.html seeds sessionStorage, then the normal Risk page replays the values through its own UI.
usage: py -I make_tc_preview.py   (run deploy/make_site.py first)
"""
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[2]
site, out = root / "deploy" / "commercialumbrella", Path(__file__).resolve().parent / "preview"

POLICY = {
    "State": "AK",
    "PolicyCoverageForm": "Commercial Umbrella Coverage Form and Commercial Excess Liability Coverage Form",
    "LegalEntity": "Corporation",
    "Limit": "1,000,000", "SelfInsuredRetention": "10,000",
    "ExcessLiabilityLimit": "1,000,000", "ExcessLiabilitySelfInsuredRetention": "10,000",
    "TRIPTerminatesBeforeExpirationDate": "No",
    "TerrorismCoverage": "Yes",
    "ExcludeOtherActsOutsideUS": "No",
    "ExcludePunitiveDamagesRelatedToCertifiedActOfTerrorism": "No",
    "CommercialUmbrellaExcessLiabilityCoverage.ManualPremium": "100000",
}


def base(kind: str, carrier: str, eff: str = "2020-12-01", exp: str = "2021-12-01") -> dict:
    return {"UnderlyingPolicyType": kind, "NameID": carrier, "UnderlyingPolicyNumber": "000123",
            "UnderlyingEffectiveDate": eff, "UnderlyingExpirationDate": exp}


C19, C20, M1 = "CU_AL_12012019_V01", "CU_AL_12012020_V01", "1,000,000"
ROWS = [
    ("Aircraft Liability", {**base("Aircraft Liability", C19), "UnderlyingLiabilityPremium": "100000", "UnderlyingLiabilityLimit": M1}),
    ("BOP", {**base("BOP", C19), "UnderlyingLiabilityPremium": "100000", "UnderlyingEachOccurrenceLimit": M1,
             "UnderlyingProductsCompletedOperationsAggregateLimit": M1, "UnderlyingGeneralAggregateLimit": M1}),
    ("Commercial Auto", {**base("Commercial Auto", C19), "UnderlyingLiabilityLimit": M1,
                         "LiabilityPremiumPrivatePassengerTypes": "100000", "NumberOfVehiclesPrivatePassengerTypes": "5",
                         "LiabilityPremiumLightTrucks": "100000", "NumberOfVehiclesLightTrucks": "4",
                         "LiabilityPremiumMediumTrucks": "100000", "NumberOfVehiclesMediumTrucks": "3",
                         "LiabilityPremiumHeavyTrucks": "100000", "NumberOfVehiclesHeavyTrucks": "2",
                         "LiabilityPremiumExtraHeavyTrucks": "100000", "NumberOfVehiclesExtraHeavyTrucks": "1",
                         "LiabilityPremiumTruckTractors": "0", "NumberOfVehiclesTruckTractors": "0",
                         "LiabilityPremiumExtraHeavyTruckTractors": "0", "NumberOfVehiclesExtraHeavyTruckTractors": "0",
                         "LiabilityPremiumTrailers": "0", "NumberOfVehiclesTrailers": "0",
                         "LiabilityPremiumZoneRated": "0", "NumberOfVehiclesZoneRated": "0",
                         "LiabilityPremiumPublicTransportation": "0", "NumberOfVehiclesPublicTransportation": "0",
                         "LiabilityPremiumOther": "0"}),
    ("Auto Dealers", {**base("Auto Dealers", C20), "UnderlyingLiabilityPremium": "100000", "UnderlyingEachAccidentLimitAutoOnly": M1,
                      "UnderlyingEachAccidentLimitOtherThanAuto": M1, "UnderlyingAggregateLimit": M1, "UnderlyingHiredAutoLimit": M1}),
    ("General Liability", {**base("General Liability", C19), "CoverageForm": "Occurrence", "UnderlyingEachOccurrenceLimit": M1,
                           "UnderlyingPersonalAdvertisingLiabilityLimit": M1, "UnderlyingGeneralAggregateLimit": M1,
                           "UnderlyingProductsCompletedOperationsAggregateLimit": M1,
                           "LiabilityPremiumPremisesTable1": "1000", "LiabilityPremiumPremisesTable2": "1000", "LiabilityPremiumPremisesTable3": "1000",
                           "LiabilityPremiumProductsTableA": "1000", "LiabilityPremiumProductsTableB": "1000", "LiabilityPremiumProductsTableC": "1000",
                           "UnderlyingHiredAndNonOwnedAutoLimit": M1, "UnderlyingHiredAndNonOwnedAutoPremium": "10000"}),
    ("Employers Liability", {**base("Employers Liability", C19, exp="2020-12-01"), "UnderlyingLiabilityPremium": "10000",
                             "UnderlyingBIByAccidentEachAccidentLimit": M1, "UnderlyingBIByDiseaseEachEmployeeLimit": M1,
                             "UnderlyingBIByDiseaseEachPolicyLimit": M1}),
    ("Liquor", {**base("Liquor Liability", C19), "UnderlyingLiabilityPremium": "10000", "UnderlyingEachCommonCauseLimit": M1, "UnderlyingAggregateLimit": M1}),
    ("Watercraft", {**base("Watercraft Liability", C19), "UnderlyingLiabilityPremium": "10000", "UnderlyingLiabilityLimit": M1}),
    ("Other Liability", {**base("Test", C19), "CoverageForm": "Not Applicable", "UnderlyingLiabilityPremium": "10000", "UnderlyingLiabilityLimit": M1}),
]
# TC 'Policy Detail Form Summary' forms that carry a premium (Manual Premium in each form's own input block)
FORMS = [{"name": "Businessowners Liability Changes Including Products-Completed Operations Aggregate Limit Of Insurance (CU 25 03 12 19)", "premium": 10000},
         {"name": "Disclosure Pursuant To Terrorism Risk Insurance Act (IL 09 85 12 20)", "premium": 10000}]

STATE = {"forms": FORMS, "pol": POLICY, "rows": [{"g": g, "v": v} for g, v in ROWS]}

out.mkdir(exist_ok=True)
for f in ("index.html", "risk.html", "program.html"):
    shutil.copy(site / f, out / f)
seed = json.dumps(STATE, separators=(",", ":"))
(out / "start.html").write_text(
    f"<!DOCTYPE html><meta charset=utf-8><title>AK TC preview</title><script>"
    f"sessionStorage.setItem('cuRiskState',{json.dumps(seed)});sessionStorage.setItem('cuRestore','1');"
    f"sessionStorage.setItem('cuFlow','1');location.replace('risk.html')</script>", "utf-8")
print("wrote", out / "start.html")
