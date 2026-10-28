"""Export Page, Page Field and Domain Table content from FRC XML to CSV.

usage: frc_export.py <ERC batch dir> <out dir>
"""
import csv
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PAGE_COLS = ("Type", "Name", "ParentName", "TableName", "MinOccurs", "MaxOccurs", "Sequence",
             "Number", "Condition", "Hidden", "HidePremium", "Scheduled", "Variable",
             "DisplayMode", "CombineWithDetail", "AttachmentCondition", "BureauRuleNumber")
FIELD_COLS = ("Sequence", "ColumnName", "Type", "Label", "QuoteDisplay", "QuoteRequired",
              "QuoteReadOnly", "PolicyDisplay", "PolicyRequired", "PolicyReadOnly", "Default",
              "Minimum", "Maximum", "Condition", "RequiredCondition", "DomainTableName",
              "RefTableName", "BureauRuleNumber")


def path_of(st: str, batch: Path, kind: str) -> Path:
    d = batch / f"ERC-CU-{st}-12012020-V01" / f"ERC-CU-{st}-12012020-V01" / f"RC-CU-{st}-12012020-V01" / f"RC-CU-{st}-12012020-V01"
    return d / f"{kind}-CU-{st}-12012020-V01.xml"


def child_pages(node):
    return [f for w in node.findall("Forms") for f in w.findall("Form")]


def walk(node, depth, parent_path, pages, fields):
    name = node.findtext("Name", "")
    page_path = f"{parent_path}/{name}" if parent_path else name
    kids = child_pages(node)
    flds = node.findall("Field")
    row = {"Depth": depth, "Path": page_path, "NFields": len(flds), "NChildPages": len(kids)}
    row.update({c: node.findtext(c, "") for c in PAGE_COLS})
    pages.append(row)
    for f in flds:
        r = {"PagePath": page_path, "PageType": row["Type"], "PageTable": row["TableName"]}
        r.update({c: f.findtext(c, "") for c in FIELD_COLS})
        fields.append(r)
    for k in kids:
        walk(k, depth + 1, page_path, pages, fields)


def domains(root):
    out = []
    for d in root.findall("DomainTable"):
        entries = d.findall("DomainTableEntry")
        keys = d.findall("DomainTableKey")
        out.append({
            "Name": d.findtext("Name", ""), "Type": d.findtext("Type", ""),
            "XmlType": d.findtext("XmlType", ""), "BureauRuleNumber": d.findtext("BureauRuleNumber", ""),
            "NKeys": len(keys), "NEntries": len(entries),
            "Sample": "|".join((e.findtext("DataValue") or e.findtext("MinimumValue") or "") for e in entries[:6]),
        })
    return out


def write(path: Path, rows, cols):
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main(batch: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for st in ("AK", "CW"):
        root = ET.parse(path_of(st, batch, "FRC")).getroot()
        pages, fields = [], []
        for top in root.find("Forms").findall("Form"):
            walk(top, 0, "", pages, fields)
        write(out / f"frc_{st}_pages.csv", pages, ["Depth", "Path", "NFields", "NChildPages", *PAGE_COLS])
        write(out / f"frc_{st}_fields.csv", fields, ["PagePath", "PageType", "PageTable", *FIELD_COLS])
        dom = domains(root)
        write(out / f"frc_{st}_domains.csv", dom, ["Name", "Type", "XmlType", "BureauRuleNumber", "NKeys", "NEntries", "Sample"])
        print(st, "pages", len(pages), "fields", len(fields), "domains", len(dom))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
