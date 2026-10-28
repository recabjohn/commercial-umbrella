"""Check built page against the SWP sample's key shape. Run: py -I test_lob_page.py"""
import build_lob_page as b

SAMPLE_ATTR_KEYS = set("""ImageStyle SubApplicationName ComponentType DefaultValue IsRequired Order ColumnHeading
ComponentLabel TableHeading OnKeyUpAction StyleClass AttributeStyleClass OnBlurAction OnChangeAction OnClickAction
OnKeyDownAction MinValue MaxValue Width Size MaxLength ComponentId Height TableWidth GroupName RowHeadingStyle Tooltip
AttributeName AttributeDataType AttributeValue InputFormatPattern OutputFormatPattern RequiredMessage ValidatorMessage
RenderValue IsDisabled AttributeParams LookupInstanceName LookupType ChildComponent LookupItemlabelTemplate
ParentComponentInstance ParentAttributeParams ItemTipParams IsInvisible IsReadonly PlaceHolderText Immediate AjaxNeeded
ValidationRegex NavigationParam AttributeTypeCondition TextRows TextColumns MandatoryAttributeStyleClass LinkText
ResponseKey DynamicSubapplicationName EventName EntityHierarchyName EntityHierarchyId SubApplicationAttributeValueList
SubApplicationDetailList ChildAttributeList Custom1 Custom2 Custom3 Custom4 Custom5 Action AdjacentLabel
MinMaxValidationMessage ImageName ImageType ImageSource ImagePosition LabelSize Sequence""".split())

SAMPLE_SUB_KEYS = set("""IsExpandable PageNameUrl LookUpInstance HeaderFtlName FooterFtlName FileName TileName
IsSubmitButtonNeeded IsEmptyFormNeeded ButtonType mAction SubApplicationId OwnerId ApplicationNumber
ApplicationSubNumber ApplicationName Description Type NumberOfRowsFixed NumberOfRowsAvailable CurrentVersionId
SubApplicationStatus SubmitButtonName AdditionalButtonName AdditionalButtonClickEvent SubApplicationVersionId
SubApplicationVersionNumber EntityHierarchyName EntityHierarchyId AttributeDetailList ChildSubApplicationList
NumberOfRowsAvilable""".split())


def shape_errs(page: dict) -> list[str]:
    errs = []
    for s in page["ApplicationDetail"]["SubApplicationDetailList"]:
        if set(s) != SAMPLE_SUB_KEYS:
            errs.append(f"{s['TileName']}: sub-app keys differ {set(s) ^ SAMPLE_SUB_KEYS}")
        for a in s["AttributeDetailList"]:
            if set(a) != SAMPLE_ATTR_KEYS:
                errs.append(f"{a['AttributeName']}: attr keys differ {set(a) ^ SAMPLE_ATTR_KEYS}")
    return errs


def check(page: dict) -> list[str]:
    errs = shape_errs(page)
    subs = page["ApplicationDetail"]["SubApplicationDetailList"]
    pi = subs[0]["AttributeDetailList"]
    boxes = [a for a in pi if a["ComponentType"] == "CheckBox"]
    if [a["AttributeName"] for a in boxes] != [s[0] for s in b.SUBLINES]:
        errs.append("checkbox list != SUBLINES")
    nxt = subs[1]["AttributeDetailList"][1]["Action"]["UIReadOnlyConditions"]
    if len(nxt) != len(b.SUBLINES):
        errs.append("Next read-only blocks != number of sublines")
    return errs


if __name__ == "__main__":
    good = b.build()
    assert check(good) == [], check(good)
    bad = b.build()                       # known-bad input must fail (verifying the verifier)
    del bad["ApplicationDetail"]["SubApplicationDetailList"][0]["AttributeDetailList"][0]["Sequence"]
    assert check(bad), "checker passed a broken page"
    assert shape_errs(b.build_expand()) == [], shape_errs(b.build_expand())
    labels = [a["ComponentLabel"] for a in b.build_expand()["ApplicationDetail"]["SubApplicationDetailList"][0]["AttributeDetailList"]]
    assert labels == [l for _, l, _ in b.DETAILS]
    print("ok: LOB page + ExpandPanel match SWP key shape; broken page is rejected")
