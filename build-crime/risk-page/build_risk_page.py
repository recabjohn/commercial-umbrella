"""Build CU "Risk/Coverage" page metadata (getApplicationMetadata shape) from the FRC exports.

Hierarchy (findings 03/05): CommercialUmbrella -> Policy (State) -> Underlying Insurance risk groups
(9 x Summary+Detail, direct children of Policy; no Location/Classification). Mirrors the GL runtime
pattern: entity per level, State first then the rest, Summary table with in-row Detail, Save per level.

usage: py -I build_risk_page.py <frc-data-full dir> <domains.json> <out dir>
Writes: cu_risk_page / cu_policy_detail / cu_additional_coverage / cu_risk_groups _metadata.json
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lob-page"))
import build_lob_page as b  # noqa: E402  attr(), sub_app(), envelope(), REQUEST_SESSION, WF

# ---- assumptions (Builder assigns the real values) ---------------------------
PARENT_LOB_KEY = "commercialumbrellaID"      # LOB page saves CommercialUmbrellaID under this key
POLICY_ENTITY = "Policy"
POLICY_CTX = "PolicyStateID"                 # same context key GL uses for the saved Policy row
SAVE_VER = "1.0.0.0"                         # placeholder event versions
STATES = dict(zip("AK AL AR AZ CA CO CT DC DE FL GA HI IA ID IL IN KS KY LA MA MD ME MI MN MO MS MT NC ND NE NH NJ NM NV NY OH OK OR PA PR RI SC SD TN TX UT VA VT WA WI WV WY".split(),
    "Alaska|Alabama|Arkansas|Arizona|California|Colorado|Connecticut|District of Columbia|Delaware|Florida|Georgia|Hawaii|Iowa|Idaho|Illinois|Indiana|Kansas|Kentucky|Louisiana|Massachusetts|Maryland|Maine|Michigan|Minnesota|Missouri|Mississippi|Montana|North Carolina|North Dakota|Nebraska|New Hampshire|New Jersey|New Mexico|Nevada|New York|Ohio|Oklahoma|Oregon|Pennsylvania|Puerto Rico|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Virginia|Vermont|Washington|Wisconsin|West Virginia|Wyoming".split("|")))
GROUPS = ("Aircraft Liability", "Auto Dealers", "BOP", "Commercial Auto", "Employers Liability",
          "General Liability", "Liquor", "Other Liability", "Watercraft")
NOTE = "Note: At least one State and one Underlying Insurance need to be added."
# -----------------------------------------------------------------------------

DOMAINS: dict = {}
DS: dict = {}          # (entity, column) -> (type, size, scale) from the DS Column Details sheet


def clean(s: str) -> str:
    return re.sub(r"<[^>]+>|&nbsp;", "", s).strip()


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", s)


def values(domain: str) -> list:
    return [{"DisplayValue": v or "Select", "Sequence": str(i), "Value": v}
            for i, v in enumerate([""] + DOMAINS.get(domain, []), start=1)]


def field(sub: str, entity: str, row: dict, summary: bool = False) -> dict:
    """One FRC 'Page Fields' row -> one metadata attribute (quote-side flags)."""
    label, name, typ = clean(row["Label"]), row["Field"], row["Type"]
    readonly, required = row["Quote ReadOnly"] == "Yes", row["Quote Required"] == "Yes"
    if row["Comment"].startswith("Header") or "<u>" in row["Label"]:
        ctype = "Subheading"                                      # FRC marks header rows with Comment=Header / underlined label
    elif typ == "Select":
        ctype = "SELECT"
    elif readonly or summary:
        ctype = "outputText"
    elif "Date" in name:
        ctype = "Date"
    else:
        ctype = "Text"
    extra = {}
    if typ == "Select":
        extra["SubApplicationAttributeValueList"] = values(row["Domain Table"])
    cond, rcond = row["Condition"], row["Required Condition"]
    dtype, size, scale = DS.get((row["Field Table Name"], name), (None, None, None))
    if dtype not in ("Decimal", "Integer", "Date", "Text"):
        dtype = None
    if dtype == "Decimal" and ctype != "Text":
        dtype = None
    return b.attr(sub, name, ctype, int(row["Sequence"]), label, entity,
                  DefaultValue=row["Default"], IsRequired="Y" if required and not summary and ctype != "Subheading" else "N",
                  RequiredMessage=f"{label} is required." if required else "",
                  IsReadonly=readonly, IsInvisible="Y" if "PackagePolicy" in cond else "N",   # PackagePolicy is not a Policy Detail field
                  MinValue=row["Min"] or "0", MaxValue=row["Max"] or "0", Tooltip=row["Help Text"],
                  Custom1=cond,                                   # display condition (evaluated by the screen)
                  Custom2=rcond,                                  # required-only-when condition
                  Custom3="Y" if row["Display Controller"] == "Yes" else "",    # other fields' conditions depend on this one
                  Custom4="Y" if row["Trigger Automatic Rating"] == "Yes" else "",  # change re-rates the quote
                  AjaxNeeded="true" if cond or typ == "Select" else "false",
                  AttributeDataType=dtype or "String", Custom5=scale or "",   # Custom5 = decimal scale (DS)
                  **{"MaxLength": size or ""}, **extra)


def save_button(sub: str, entity: str, target: str, parent_src: str, ctx_parent: bool, ctx_key: str = "") -> dict:
    session = [d for d in b.REQUEST_SESSION if d["RequestKey"] != "ID"]
    if not ctx_parent:                                        # Policy: parent is the LOB entity
        session = [*session, {"SourceAttribute": parent_src, "RequestKey": "ID"}]
    mapping = {"SessionState": session}
    if ctx_parent:                                            # risk group: parent is the saved Policy row
        mapping = {**mapping, "contextState": [{"SourceAttribute": POLICY_CTX, "RequestKey": "PARENTID"}]}
    action = {
        "ResponseTranslation": {"TranslateResponse": True, "ParentState": [{"ResponseKey": entity, "TargetAttribute": f"{sub.lower()}_dataList"}],
                                "contextState": [{"ResponseKey": f"{entity}/ID", "TargetAttribute": ctx_key}] if ctx_key else []},
        "RequestConstruction": "Y", "URLVersion": "PlatformWFService_V4", "dynamicButton": True, "ButtonLoaderNeeded": "Y",
        "URL": "/core/invokeWorkflowEvent",
        "EventMapping": {**b.WF, "TargetEventName": target},
        "RequestMapping": mapping,
    }
    return b.attr(sub, "SaveButton", "SubmitV3", 99000, "Save", entity, StyleClass="pull-right", Size="", MaxLength="0",
                  AttributeDataType="String", Action=action)


def row_actions(delete_event: str, entity: str, max_rows: int) -> dict:
    return {
        "pagination": {"rowsPerPageOptions": [5, 10, 15], "rowsPerPage": 5, "isNeeded": True},
        "editRow": {"onExpand": "onExpand", "editRowFunction": "EditRow", "isNeeded": True},
        "sorting": {"isNeeded": False}, "selectable": {"isNeeded": False},
        "childComponent": {"renderTemplate": True, "renderTemplateName": f"{entity}Detail"},
        "ActionList": {"ActionType": "Delete", "ActionDisplayName": "Delete", "rowAction": {
            "successToastNotificationMessage": "Deleted Successfully", "LoaderNeeded": "Y",
            "URLVersion": "PlatformWFService_V4", "URL": "/core/invokeWorkflowEvent",
            "EventMapping": {"EventName": delete_event},
            "RequestMapping": {"SessionState": b.REQUEST_SESSION[:1] + b.REQUEST_SESSION[2:],
                               "contextState": [{"SourceAttribute": POLICY_CTX, "RequestKey": "PARENTID"}],
                               "localState": [{"SourceAttribute": "ID", "RequestKey": "ID"}],
                               "CustomProperties": [{"CustomKey": "EntityName", "CustomValue": entity},
                                                    {"CustomKey": "RepositoryName", "CustomValue": "Submission"}]}}},
        "addRow": {"addRowFunction": "AddRow", "isNeeded": True, "maxRows": max_rows},
    }


def rows(frc: Path, page: str) -> list:
    return [r for r in csv.DictReader(open(frc / "AK_fields.csv", encoding="utf-8")) if r["Page"] == page]


def group_pages(frc: Path) -> list:
    """Risk groups = Summary pages directly under Policy Detail, in FRC page-sequence order, with MaxOccurs."""
    pg = [r for r in csv.DictReader(open(frc / "AK_page.csv", encoding="utf-8"))
          if r["Parent"] == "Policy Detail" and r["Type"] == "Summary" and r["Name"] in GROUPS]
    return [(r["Name"], int(r["Max Occurs"])) for r in sorted(pg, key=lambda r: int(r["Sequence"]))]


def page_chrome() -> dict:
    sub = "LocationValidation"
    note = b.attr(sub, "Validation", "OutputLabel", 10, NOTE, IsRequired="Y", AttributeStyleClass="pull-right",
                  AttributeDataType="String", AdjacentLabel="N")
    return b.envelope([b.sub_app(sub, [note], Description="Location Validation", FileName=f"{sub}_V1"), b.navigation_buttons()],
                      {"NavigationButtonsSubmission": "", sub: ""}, ProductName=b.PRODUCT_NAME, TemplatePageUrl="")


def policy_detail(frc: Path) -> dict:
    sub = "PolicyDetail"
    state = b.attr(sub, "State", "SelectAutoComplete", 1, "State", POLICY_ENTITY, IsRequired="Y", Size="12", MaxLength="100",
                   RequiredMessage="State is required.", AjaxNeeded="true", AttributeDataType="String",
                   DependentComponent=[f"{sub}__StateFullName"],
                   SubApplicationAttributeValueList=[{"DisplayValue": n, "Sequence": str(i), "Value": c} for i, (c, n) in enumerate(STATES.items(), 1)],
                   Action={"ResponseTranslation": {"contextState": [{"ResponseKey": "State", "TargetAttribute": "policyState"}]},
                           "SetStateCode": "Y"})
    attrs = [state] + [field(sub, POLICY_ENTITY, r) for r in rows(frc, "Policy Detail")]
    attrs.append(save_button(sub, POLICY_ENTITY, f"SaveCommercialUmbrellaPolicydetails_{SAVE_VER}", PARENT_LOB_KEY, False, POLICY_CTX))
    return b.envelope([b.sub_app(sub, attrs, POLICY_ENTITY, Description="Policy Detail", FileName="PolicyDetail_1", LookUpInstance="northStarApplicationManagedBeanV1")],
                      {sub: POLICY_ENTITY}, ProductName=b.PRODUCT_NAME, TemplatePageUrl="")


def additional_coverage() -> dict:
    sub = "AdditionalCoverage"
    col = b.attr(sub, "CoverageDisplayName", "OutputText", 10, "Coverage", IsRequired="Y", AttributeDataType="String")
    return b.envelope([b.sub_app(sub, [col], Type="Summary", Description="Additional Coverages", FileName="AdditionalCoverage_1_0",
                                 mAction={"pagination": {"rowsPerPageOptions": [5, 10, 15], "rowsPerPage": 5, "isNeeded": True},
                                          "addRow": {"addRowFunction": "showDialog", "isNeeded": True}})],
                      {sub: ""}, ProductName=b.PRODUCT_NAME, TemplatePageUrl="")


def risk_groups(frc: Path) -> dict:
    subs, ents = [], {}
    for g, max_rows in group_pages(frc):
        entity = f"CommercialUmbrella{slug(g)}"
        s_name, d_name = slug(g), f"{slug(g)}Detail"
        summ = [field(s_name, entity, r, summary=True) for r in rows(frc, g)]
        det = [field(d_name, entity, r) for r in rows(frc, f"{g} Detail")]
        for a in det:
            if a["AttributeName"] == "UnderlyingPolicyType":
                a["DefaultValue"] = g                         # fixed by the risk group
        det.append(save_button(d_name, entity, f"SaveCommercialUmbrella{slug(g)}Details_{SAVE_VER}", "", True))
        subs += [b.sub_app(s_name, summ, entity, Type="Summary", Description=g, FileName=f"{s_name}_1",
                           mAction=row_actions(f"RemoveCommercialUmbrella{slug(g)}Detail_{SAVE_VER}", entity, max_rows)),
                 b.sub_app(d_name, det, entity, Description=f"{g} Detail", FileName=f"{d_name}_1",
                           LookUpInstance="northStarApplicationManagedBeanV1")]
        ents |= {s_name: entity, d_name: entity}
    return b.envelope(subs, ents, ProductName=b.PRODUCT_NAME, TemplatePageUrl="")


def _norm(x: str) -> str:
    return re.sub(r"[^a-z0-9]", "", x.lower())


def validation_rules(frc: Path) -> dict:
    """ALG 'Err-*' sheets -> UI rules. 'X Is Equal To 0.0' chains become allZero; the GL hired/non-owned pair is typed by hand."""
    alg = json.loads((frc / "AK_alg_errors.json").read_text("utf-8"))
    out = {"policy": [], "groups": {}}
    for g, _ in group_pages(frc):
        names = {_norm(r["Field"]): r["Field"] for r in rows(frc, f"{g} Detail")}
        rules = []
        for r in alg.get(f"Err-{slug(g)}", []):
            if "HiredAndNonOwned" in r["rule"]:
                kind = "limitNeedsPremium" if "PremiumMustBeGreaterThan0" in r["rule"] else "premiumNeedsLimit"
                rules.append({"t": kind, "limit": "UnderlyingHiredAndNonOwnedAutoLimit", "prem": "UnderlyingHiredAndNonOwnedAutoPremium", "msg": r["msg"]})
                continue
            toks = [re.sub(r"^(\(\s*)*(And|Or)?\s*", "", c).strip() for c in r["cond"]]
            labels = [toks[i - 1] for i, c in enumerate(r["cond"]) if c.strip().endswith("Is Equal To 0.0") and i]
            fields = [names[_norm(t)] for t in labels if _norm(t) in names]
            off_page = [t for t in labels if _norm(t) not in names]   # DB-only fields (e.g. Employee Benefits premium): not on the screen, count as 0
            assert fields, r["rule"]
            rules.append({"t": "allZero", "f": fields, "msg": r["msg"], "offPage": off_page})
        out["groups"][g] = rules
    for r in alg.get("Err-ExcessLiabilityCoverage", []):
        out["policy"].append({"t": "gt0", "f": "CommercialUmbrellaExcessLiabilityCoverage.ManualPremium", "msg": r["msg"]})
    return out


def build_all(frc: Path) -> dict:
    return {"cu_risk_page": page_chrome(), "cu_policy_detail": policy_detail(frc),
            "cu_additional_coverage": additional_coverage(), "cu_risk_groups": risk_groups(frc)}


if __name__ == "__main__":
    frc, dom, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    DOMAINS.update(json.loads(dom.read_text("utf-8")))
    DS.update({(c[0], c[1]): (c[2], c[3], c[4]) for c in json.loads((frc / "AK_ds_columns.json").read_text("utf-8"))["cols"]})
    (out / "cu_validation_rules.json").write_text(json.dumps(validation_rules(frc), indent=2), encoding="utf-8")
    for name, page in build_all(frc).items():
        (out / f"{name}_metadata.json").write_text(json.dumps(page, indent=4), encoding="utf-8")
        print("wrote", name, sum(len(s["AttributeDetailList"]) for s in page["ApplicationDetail"]["SubApplicationDetailList"]), "attrs")
