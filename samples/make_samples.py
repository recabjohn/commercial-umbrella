"""Sample data for all four CU sites, taken from the Test Case workbooks (Input sheet):
  AK = ERC-CU-AK-12012020-V01 / TC-CU-AK-12012020-V01.xlsx
  KY = ERC-CU-KY-12012023-V03 / TC-CU-KY-12012023-V03.xlsx   AR = ERC-CU-AR-01012026-V01 / TC-CU-AR-01012026-V01.xlsx
Only TC fields that exist on the screens are filled (TC-only fields such as 'Policy Issued To Operators Of Aerial Recreational Devices'
and 'Terrorism Factor' are skipped); screen fields the TC leaves out get an assumed value (marked ASSUMED below).
Writes seed_<kind>.html (head script, loads the chosen sample into sessionStorage before the Risk page runs) and
bar_<kind>.html (sample selector bar). kinds: single, v2, v3, v4.   usage: py -I make_samples.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
M1 = "1,000,000"
COMBINED = "Commercial Umbrella Coverage Form and Commercial Excess Liability Coverage Form"


def hdr(kind, carrier, num, eff, exp):
    return {"UnderlyingPolicyType": kind, "NameID": carrier, "UnderlyingPolicyNumber": num, "UnderlyingEffectiveDate": eff, "UnderlyingExpirationDate": exp}


def ky_rows():
    h = lambda kind, carrier="AQS": hdr(kind, carrier, "123456", "2013-10-01", "2014-10-01")  # noqa: E731
    auto = {**h("Commercial Auto"), "UnderlyingLiabilityLimit": M1}
    for k in ("PrivatePassengerTypes", "LightTrucks", "MediumTrucks", "HeavyTrucks", "ExtraHeavyTrucks", "TruckTractors",
              "ExtraHeavyTruckTractors", "Trailers", "ZoneRated", "PublicTransportation"):
        auto[f"LiabilityPremium{k}"] = "1000"
        auto[f"NumberOfVehicles{k}"] = "1"
    auto["LiabilityPremiumOther"] = "1000"
    return [
        ("Aircraft Liability", {**h("Aircraft Liability"), "UnderlyingLiabilityPremium": "250000", "UnderlyingLiabilityLimit": M1}),
        ("BOP", {**h("BOP"), "UnderlyingLiabilityPremium": "1000", "UnderlyingEachOccurrenceLimit": M1,
                 "UnderlyingProductsCompletedOperationsAggregateLimit": M1, "UnderlyingGeneralAggregateLimit": M1}),
        ("Commercial Auto", auto),
        ("Auto Dealers", {**h("Auto Dealers", "Carrier Ins"), "UnderlyingLiabilityPremium": "1000", "UnderlyingEachAccidentLimitAutoOnly": M1,
                          "UnderlyingEachAccidentLimitOtherThanAuto": M1, "UnderlyingAggregateLimit": M1, "UnderlyingHiredAutoLimit": M1}),
        ("General Liability", {**h("General Liability"), "CoverageForm": "Occurrence", "UnderlyingEachOccurrenceLimit": M1,
                               "UnderlyingPersonalAdvertisingLiabilityLimit": M1, "UnderlyingGeneralAggregateLimit": M1,
                               "UnderlyingProductsCompletedOperationsAggregateLimit": M1,
                               "LiabilityPremiumPremisesTable1": "1000", "LiabilityPremiumPremisesTable2": "1000", "LiabilityPremiumPremisesTable3": "1000",
                               "LiabilityPremiumProductsTableA": "1000", "LiabilityPremiumProductsTableB": "1000", "LiabilityPremiumProductsTableC": "1000",
                               "UnderlyingHiredAndNonOwnedAutoLimit": "1,500,000", "UnderlyingHiredAndNonOwnedAutoPremium": "250000"}),
        ("Employers Liability", {**h("Employers Liability"), "UnderlyingLiabilityPremium": "1000", "UnderlyingBIByAccidentEachAccidentLimit": M1,
                                 "UnderlyingBIByDiseaseEachEmployeeLimit": M1, "UnderlyingBIByDiseaseEachPolicyLimit": M1}),
        ("Liquor", {**h("Liquor Liability"), "UnderlyingLiabilityPremium": "1000", "UnderlyingEachCommonCauseLimit": M1, "UnderlyingAggregateLimit": M1}),
        ("Watercraft", {**h("Watercraft Liability"), "UnderlyingLiabilityPremium": "100000", "UnderlyingLiabilityLimit": "4,500,000"}),
        ("Other Liability", {**h("Other LOB"), "CoverageForm": "Occurrence", "UnderlyingLiabilityPremium": "250000", "UnderlyingLiabilityLimit": M1}),
    ]


def ar_rows():
    # TC detail block says Carrier 'Test' (the summary line leaves it blank). The TC has an Aircraft Liability row only.
    return [("Aircraft Liability", {**hdr("Aircraft Liability", "Test", "123456789", "2026-01-01", "2026-12-31"),
                                    "UnderlyingLiabilityPremium": "10000", "UnderlyingLiabilityLimit": M1})]


def ak_rows():
    h = lambda kind, carrier="CU_AL_12012019_V01", eff="2020-12-01", exp="2021-12-01": hdr(kind, carrier, "000123", eff, exp)  # noqa: E731
    auto = {**h("Commercial Auto"), "UnderlyingLiabilityLimit": M1, "LiabilityPremiumTruckTractors": "0", "NumberOfVehiclesTruckTractors": "0",
            "LiabilityPremiumExtraHeavyTruckTractors": "0", "NumberOfVehiclesExtraHeavyTruckTractors": "0", "LiabilityPremiumTrailers": "0",
            "NumberOfVehiclesTrailers": "0", "LiabilityPremiumZoneRated": "0", "NumberOfVehiclesZoneRated": "0",
            "LiabilityPremiumPublicTransportation": "0", "NumberOfVehiclesPublicTransportation": "0", "LiabilityPremiumOther": "0"}
    for k, n in (("PrivatePassengerTypes", 5), ("LightTrucks", 4), ("MediumTrucks", 3), ("HeavyTrucks", 2), ("ExtraHeavyTrucks", 1)):
        auto[f"LiabilityPremium{k}"] = "100000"
        auto[f"NumberOfVehicles{k}"] = str(n)
    return [
        ("Aircraft Liability", {**h("Aircraft Liability"), "UnderlyingLiabilityPremium": "100000", "UnderlyingLiabilityLimit": M1}),
        ("BOP", {**h("BOP"), "UnderlyingLiabilityPremium": "100000", "UnderlyingEachOccurrenceLimit": M1,
                 "UnderlyingProductsCompletedOperationsAggregateLimit": M1, "UnderlyingGeneralAggregateLimit": M1}),
        ("Commercial Auto", auto),
        ("Auto Dealers", {**h("Auto Dealers", "CU_AL_12012020_V01"), "UnderlyingLiabilityPremium": "100000", "UnderlyingEachAccidentLimitAutoOnly": M1,
                          "UnderlyingEachAccidentLimitOtherThanAuto": M1, "UnderlyingAggregateLimit": M1, "UnderlyingHiredAutoLimit": M1}),
        ("General Liability", {**h("General Liability"), "CoverageForm": "Occurrence", "UnderlyingEachOccurrenceLimit": M1,
                               "UnderlyingPersonalAdvertisingLiabilityLimit": M1, "UnderlyingGeneralAggregateLimit": M1,
                               "UnderlyingProductsCompletedOperationsAggregateLimit": M1,
                               "LiabilityPremiumPremisesTable1": "1000", "LiabilityPremiumPremisesTable2": "1000", "LiabilityPremiumPremisesTable3": "1000",
                               "LiabilityPremiumProductsTableA": "1000", "LiabilityPremiumProductsTableB": "1000", "LiabilityPremiumProductsTableC": "1000",
                               "UnderlyingHiredAndNonOwnedAutoLimit": M1, "UnderlyingHiredAndNonOwnedAutoPremium": "10000"}),
        ("Employers Liability", {**h("Employers Liability", exp="2020-12-01"), "UnderlyingLiabilityPremium": "10000", "UnderlyingBIByAccidentEachAccidentLimit": M1,
                                 "UnderlyingBIByDiseaseEachEmployeeLimit": M1, "UnderlyingBIByDiseaseEachPolicyLimit": M1}),
        ("Liquor", {**h("Liquor Liability"), "UnderlyingLiabilityPremium": "10000", "UnderlyingEachCommonCauseLimit": M1, "UnderlyingAggregateLimit": M1}),
        ("Watercraft", {**h("Watercraft Liability"), "UnderlyingLiabilityPremium": "10000", "UnderlyingLiabilityLimit": M1}),
        ("Other Liability", {**h("Test"), "CoverageForm": "Not Applicable", "UnderlyingLiabilityPremium": "10000", "UnderlyingLiabilityLimit": M1}),
    ]


def policy(state, terrorism, manual="10000"):
    p = {"State": state, "PolicyCoverageForm": COMBINED, "LegalEntity": "Corporation", "Limit": M1, "SelfInsuredRetention": "10,000",
         "ExcessLiabilityLimit": M1, "ExcessLiabilitySelfInsuredRetention": "10,000", "TRIPTerminatesBeforeExpirationDate": "No",
         "TerrorismCoverage": terrorism, "ExcludeOtherActsOutsideUS": "No",
         "CommercialUmbrellaExcessLiabilityCoverage.ManualPremium": manual}
    if terrorism == "Yes":
        p["ExcludePunitiveDamagesRelatedToCertifiedActOfTerrorism"] = "No"
    else:
        p["TerrorismCoverageSpecificLimitations"] = "No"
    return p


AK_FORMS = [("Businessowners Liability Changes (CU 25 03 12 19)", 10000), ("Disclosure Pursuant To Terrorism Risk Insurance Act (IL 09 85 12 20)", 10000)]
KY_FORMS = [("Auto Dealers Endorsement (CU 22 31 09 18)", 250000), ("Businessowners Liability Changes (CU 24 29 12 19)", 250000)]
AR_FORMS = [("Arkansas Changes (CX 01 26 04 13)", 100), ("Condition - Litigation Funding Mutual Disclosure (CX 99 02 01 26)", 1000),
            ("Exclusion - Assault Or Battery (CU 34 68 01 26)", 10000), ("Exclusion - Assault Or Battery (CX 34 11 01 26)", 1000),
            ("Exclusion - Generative Artificial Intelligence (CU 34 69 01 26)", 2000), ("Exclusion - Generative Artificial Intelligence (CX 34 12 01 26)", 2000),
            ("Exclusion - Generative Artificial Intelligence, Coverage B Only (CU 34 70 01 26)", 3000), ("Exclusion - Human Trafficking (CU 34 71 01 26)", 4000),
            ("Exclusion - Human Trafficking (CX 34 13 01 26)", 3000), ("Exclusion - Punitive Damages (CU 34 72 01 26)", 5000),
            ("Exclusion - Punitive Damages (CX 34 14 01 26)", 4000),
            ("Terrorism (c) - premium carried from the TC (Terrorism Factor .12 x 55,100; the factor is not a screen field)", 6612)]

SAMPLES = {
    "AK": {"pol": policy("AK", "Yes", "100000"), "rows": [{"g": g, "v": v} for g, v in ak_rows()], "forms": [{"name": n, "premium": x} for n, x in AK_FORMS]},
    "KY": {"pol": policy("KY", "No"), "rows": [{"g": g, "v": v} for g, v in ky_rows()], "forms": [{"name": n, "premium": x} for n, x in KY_FORMS]},
    "AR": {"pol": policy("AR", "Yes"), "rows": [{"g": g, "v": v} for g, v in ar_rows()], "forms": [{"name": n, "premium": x} for n, x in AR_FORMS]},
}

# JS that builds cuRiskState for each site structure (S = SAMPLES, ch = chosen sample: KY | AR | KY+AR | NONE)
BUILD = {
    "single": """const k=ch.split('+')[0],d=S[k];st={forms:d.forms,pol:d.pol,rows:d.rows.map(r=>({g:r.g,v:{...r.v,NameID:'',UnderlyingPolicyNumber:''}}))};""",  # main site: Carrier / Policy Number left empty (lookup)
    "v2": """const ks=ch.split('+'),d=S[ks[0]];st={forms:ks.flatMap(k=>S[k].forms),pol:d.pol,states:ks.slice(1).map(k=>S[k].pol.State),
 rows:ks.flatMap(k=>S[k].rows.map(r=>({g:r.g,v:{...r.v,States:S[k].pol.State}})))};""",
    "v3": """const ks=ch.split('+'),d=S[ks[0]];st={forms:ks.flatMap(k=>S[k].forms),pol:d.pol,
 states:ks.slice(1).map(k=>({code:S[k].pol.State,pol:{...S[k].pol,SolartisIsPrimaryState:'No'}})),
 rows:ks.flatMap(k=>S[k].rows.map(r=>({g:r.g,v:{...r.v,States:S[k].pol.State}})))};""",
    "v4": """const ks=ch.split('+'),d=S[ks[0]];st={forms:ks.flatMap(k=>S[k].forms),pol:d.pol,
 states:ks.map(k=>({code:S[k].pol.State,rows:S[k].rows}))};""",
}
OPTS = {"single": [("AK", "AK - TC-CU-AK-12012020-V01"), ("KY", "KY - TC-CU-KY-12012023-V03"), ("AR", "AR - TC-CU-AR-01012026-V01"), ("NONE", "None (empty)")],
        "v2": None, "v3": None, "v4": None}
MULTI = [("AK+KY+AR", "AK + KY + AR (three states)"), ("KY+AR", "KY + AR (two states)"), ("AK", "AK only"), ("KY", "KY only"), ("AR", "AR only"), ("NONE", "None (empty)")]
for k in ("v2", "v3", "v4"):
    OPTS[k] = MULTI

for kind, build in BUILD.items():
    default = "AK" if kind == "single" else "AK+KY+AR"
    seed = ("<script>(function(){const S=" + json.dumps(SAMPLES, separators=(",", ":")) + ";"
            f"const ch=sessionStorage.getItem('cuSample')||'{default}';sessionStorage.setItem('cuSample',ch);"
            "if(sessionStorage.getItem('cuRestore')||ch==='NONE')return;let st;" + build.replace("\n", "") +
            "sessionStorage.setItem('cuRiskState',JSON.stringify(st));sessionStorage.setItem('cuRestore','1')})()</script>")
    opts = "".join(f'<option value="{v}">{t}</option>' for v, t in OPTS[kind])
    bar = ("<script>(function(){const b=document.createElement('div');b.style.cssText='display:flex;gap:10px;align-items:center;font-size:13px;color:#444;margin:4px 0 8px';"
           f"b.innerHTML='Sample data (Test Case workbooks): <select>{opts}</select>';const s=b.querySelector('select');"
           f"s.value=sessionStorage.getItem('cuSample')||'{default}';"
           "s.onchange=()=>{sessionStorage.setItem('cuSample',s.value);sessionStorage.removeItem('cuRestore');sessionStorage.setItem('cuFlow','1');location.reload()};"
           "document.querySelector('.card').prepend(b)})()</script>")
    (OUT / f"seed_{kind}.html").write_text(seed, "utf-8")
    (OUT / f"bar_{kind}.html").write_text(bar, "utf-8")
(OUT / "samples.json").write_text(json.dumps(SAMPLES, indent=1), "utf-8")
print("wrote", sorted(p.name for p in OUT.glob("*")))
