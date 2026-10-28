"""Build the CU "Line Of Business" page metadata (getApplicationMetadata shape).

Mirrors the SWP pages: ProgramInformation + NavigationButtonsSubmission (the page)
and ExpandPanel (the Details strip, a separate metadata call in the live app).

usage: py -I build_lob_page.py <lob_page.json> <expand_panel.json>
"""
import json
import sys
from pathlib import Path

# ---- assumptions (change here, rebuild) -------------------------------------
PRODUCT_NAME = "CU_1_0_V1"          # placeholder: real product name comes from Builder
OWNER_ID = 1
STATE = "CW"
SUBLINES = (                         # (AttributeName, label, SublineName code, ResponseTranslation target or "" = derived)
    ("GeneralLiability", "General Liability", "GL", "generalliablityID"),   # target spelled as in the SWP sample
    ("CommercialAutomobile", "Commercial Automobile", "AU", ""),
    ("CommercialProperty", "Commercial Property", "CF", ""),
    ("CommercialUmbrella", "Commercial Umbrella", "CU", ""),
    ("Crime", "Crime", "CR", ""),                    # subline code CR is an assumption (not in the sources read)
)
ENTITY = "SelectedSublines"
ENTITY_ID = 0                        # assigned by Builder import
WF = {"RepositoryName": "Submission", "EventName": "SolartisMaster_WF_1.0.0"}
SAVE_EVENT = "SaveSelectedSubline_3.1.0"
SAVE_EVENT_AGG = "SaveSelectedSubline_2.0.0"
DETAILS = (                          # (AttributeName, label, sample value) -> ExpandPanel; values are session data at runtime
    ("Name", "Agency Name", "TestAgency9590"),
    ("AgentName", "Agent Name", "testagent1003 testagent1003"),
    ("SubmissionNumber", "Submission Number", "SN196153"),
    ("SubmissionStatus", "Submission Status", "In Progress"),
    ("InsuredName", "Insured Name", "flow test"),
)
# -----------------------------------------------------------------------------

ATTR_DEFAULTS = {
    "ImageStyle": {}, "DefaultValue": "", "IsRequired": "N", "ColumnHeading": "",
    "TableHeading": "", "OnKeyUpAction": "", "StyleClass": "", "AttributeStyleClass": "",
    "OnBlurAction": "", "OnChangeAction": "", "OnClickAction": "", "OnKeyDownAction": "",
    "MinValue": "0", "MaxValue": "0", "Width": "0", "Size": "0", "MaxLength": "",
    "Height": "0", "TableWidth": "", "GroupName": "", "RowHeadingStyle": "", "Tooltip": "",
    "AttributeDataType": "Text", "AttributeValue": "", "InputFormatPattern": "",
    "OutputFormatPattern": "", "RequiredMessage": "", "ValidatorMessage": "",
    "RenderValue": True, "IsDisabled": False, "AttributeParams": "", "LookupInstanceName": "",
    "LookupType": "", "ChildComponent": "", "LookupItemlabelTemplate": "",
    "ParentComponentInstance": "", "ParentAttributeParams": "", "ItemTipParams": "",
    "IsInvisible": "N", "IsReadonly": False, "PlaceHolderText": "", "Immediate": "false",
    "AjaxNeeded": "false", "ValidationRegex": "", "NavigationParam": "",
    "AttributeTypeCondition": "", "TextRows": 0, "TextColumns": 0,
    "MandatoryAttributeStyleClass": "", "LinkText": "", "ResponseKey": "",
    "DynamicSubapplicationName": "", "EventName": "", "SubApplicationAttributeValueList": [],
    "SubApplicationDetailList": [], "ChildAttributeList": [], "Custom1": "", "Custom2": "",
    "Custom3": "", "Custom4": "", "Custom5": "", "Action": {}, "AdjacentLabel": "",
    "MinMaxValidationMessage": "", "ImageName": "", "ImageType": "", "ImageSource": "",
    "ImagePosition": "", "LabelSize": "",
}

REQUEST_SESSION = [
    {"SourceAttribute": "pageData/submissionID", "RequestKey": "ROOTID"},
    {"SourceAttribute": "pageData/insuredID", "RequestKey": "ID"},
    {"SourceAttribute": "productDetails/ProductNumber", "RequestKey": "ProductNumber"},
    {"SourceAttribute": "productDetails/ProductVerNumber", "RequestKey": "ProductVerNumber"},
]


def attr(sub: str, name: str, ctype: str, order: int, label: str, entity: str = "", **over) -> dict:
    base = {
        **ATTR_DEFAULTS,
        "SubApplicationName": sub, "ComponentType": ctype, "Order": order, "Sequence": order,
        "ComponentLabel": label, "ComponentId": name, "AttributeName": name,
        "EntityHierarchyName": entity, "EntityHierarchyId": ENTITY_ID if entity else 0,
    }
    return {**base, **over}


def sub_app(tile: str, attrs: list, entity: str = "", **over) -> dict:
    base = {
        "IsExpandable": "N", "PageNameUrl": "", "LookUpInstance": "", "HeaderFtlName": "",
        "FooterFtlName": "", "FileName": f"{tile}_V1", "TileName": tile,
        "IsSubmitButtonNeeded": "", "IsEmptyFormNeeded": "N", "ButtonType": "", "mAction": {},
        "SubApplicationId": 0, "OwnerId": OWNER_ID, "ApplicationNumber": "1.0",
        "ApplicationSubNumber": "1.0", "ApplicationName": tile, "Description": "V1",
        "Type": "Detail", "NumberOfRowsFixed": "", "NumberOfRowsAvailable": "",
        "CurrentVersionId": 0, "SubApplicationStatus": "", "SubmitButtonName": "",
        "AdditionalButtonName": "", "AdditionalButtonClickEvent": "",
        "SubApplicationVersionId": 0, "SubApplicationVersionNumber": "V1",
        "EntityHierarchyName": entity, "EntityHierarchyId": ENTITY_ID if entity else 0,
        "AttributeDetailList": attrs, "ChildSubApplicationList": [], "NumberOfRowsAvilable": "",
    }
    return {**base, **over}


def save_action(response_key: str, target: str, event: str, subline: str | None) -> dict:
    mapping = {"SessionState": REQUEST_SESSION}
    if subline:
        mapping = {**mapping, "CustomProperties": [{"CustomKey": "SublineName", "CustomValue": subline}]}
    action = {
        "SaveDataInSession": "Y", "LoaderNeeded": "Y",
        "ResponseTranslation": {"SessionState": [{"ResponseKey": response_key, "TargetAttribute": target}]},
        "RequestConstruction": "Y", "URLVersion": "PlatformWFService_V4", "handlerNeeded": True,
        "URL": "/core/invokeWorkflowEvent",
        "EventMapping": {**WF, "TargetEventName": event},
        "RequestMapping": mapping,
    }
    return {**action, "entitiesNeeded": ENTITY} if subline else action


def program_information() -> dict:
    sub = "ProgramInformation"
    attrs = [
        attr(sub, sub, "Heading", 10, "Program Information", ENTITY, IsRequired="Y", Size="12", Immediate="False"),
        attr(sub, sub, "SubHeading", 20, "Select Program", ENTITY, IsRequired="Y", Size="4", Immediate="False"),
        attr(sub, ENTITY, "MultipleCheckBoxtest", 30, "Select Program", ENTITY,
             Size="8", MaxLength="0", MinValue="", MaxValue="", IsInvisible="Y", AjaxNeeded="true",
             Action=save_action(f"{ENTITY}/ProgramID", "programID", SAVE_EVENT_AGG, None)),
    ]
    for i, (name, label, code, target) in enumerate(SUBLINES, start=1):
        attrs.append(attr(
            sub, name, "CheckBox", 30 + i * 10, label, ENTITY,
            AttributeDataType="String", MinValue="1", MaxLength="100", AdjacentLabel="N",
            Action=save_action(f"{ENTITY}/{name}ID", target or f"{name.lower()}ID", SAVE_EVENT, code),
        ))
    return sub_app(sub, attrs, ENTITY, FileName="ProgramInformation_V1",
                   mAction={"ComponentProperties": {"isCardNeeded": True}})


def not_selected(name: str) -> dict:
    """Next is read-only while the subline checkbox is not 'Yes'."""
    key = f"ProgramInformation/{name}"
    return {"conditions": [
        {"logicalOperator": "OR", "key": key, "operator": "nothas"},
        {"value": "Yes", "key": key, "operator": "notequal"},
    ]}


def navigation_buttons() -> dict:
    sub = "NavigationButtonsSubmission"
    # Sample SWP page has one condition block per subline, all must be true to lock Next.
    # ponytail: with a single subline there is one block; add blocks if more sublines are added.
    blocks = [not_selected(s[0]) for s in SUBLINES]
    blocks = [{"logicalOperator": "AND", **blocks[0]}, *blocks[1:]]
    prev = attr(sub, "PreviousYear", "ButtonV3", 1, "Previous", Width="6", Size="6", MaxLength="100",
                Action={"goto": "previous", "dynamicButton": True, "ButtonLoaderNeeded": "Y"})
    nxt = attr(sub, "NextYear", "ButtonV3", 2, "Next", StyleClass="pull-right", Width="100", Size="6",
               MaxLength="100", AttributeDataType="String",
               Action={"goto": "next", "UIReadOnlyConditions": blocks, "dynamicButton": True})
    return sub_app(sub, [prev, nxt], IsSubmitButtonNeeded="N")


def expand_panel() -> dict:
    sub = "ExpandPanel"
    attrs = [
        attr(sub, name, "OutputText", i, label, DefaultValue=value, StyleClass="auto-width font-bold _disabled",
             AttributeStyleClass="TextUnderValue font-bold", Width="100", Size="2",
             AttributeDataType="String", IsDisabled=True, IsReadonly=True)
        for i, (name, label, value) in enumerate(DETAILS, start=1)
    ]
    return sub_app(sub, attrs, IsExpandable="Y", Description="Details")


def envelope(subs: list, entities: dict, **detail) -> dict:
    return {
        "ResponseStatus": "SUCCESS",
        "ApplicationDetail": {
            "ApplicationId": 0, "OwnerId": OWNER_ID, "ApplicationVerId": 0, "ObjectId": 0,
            "ObjectVerId": 0, "ObjectName": "PRODUCT", "State": STATE,
            "SubApplicationDetailList": subs, "SubApplicationEntity": entities, **detail,
        },
    }


def build() -> dict:
    return envelope(
        [program_information(), navigation_buttons()],
        {"NavigationButtonsSubmission": "", "ProgramInformation": ENTITY},
        ProductName=PRODUCT_NAME, TemplatePageUrl="",
    )


def build_expand() -> dict:
    return envelope([expand_panel()], {"ExpandPanel": ""})


if __name__ == "__main__":
    for path, page in ((sys.argv[1], build()), (sys.argv[2], build_expand())):
        Path(path).write_text(json.dumps(page, indent=4), encoding="utf-8")
        print("wrote", path)
