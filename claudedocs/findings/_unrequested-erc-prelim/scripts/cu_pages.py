import xml.etree.ElementTree as ET, sys, collections

b = sys.argv[1]
FIELDS = ("Type", "TableName", "MinOccurs", "MaxOccurs", "Sequence", "AddChangeDeleteFlag")


def children(node):
    return [f for w in node.findall("Forms") for f in w.findall("Form")]


def walk(node, depth, stats, out):
    p = {t: node.findtext(t, "") for t in FIELDS + ("Name", "ParentName", "Number", "Condition")}
    stats[p["Type"]] += 1
    kids = children(node)
    if p["Type"] != "Form" or kids:
        out.append(
            "  " * depth
            + f"{p['Type']}: {p['Name']} | table={p['TableName']} | occ={p['MinOccurs']}/{p['MaxOccurs']}"
            + f" | seq={p['Sequence']} | flag={p['AddChangeDeleteFlag']} | forms_below={sum(1 for k in kids if k.findtext('Type') == 'Form')}"
        )
    for k in kids:
        if k.findtext("Type") != "Form" or children(k):
            walk(k, depth + 1, stats, out)
        else:
            stats["Form"] += 1


for st in ("CW", "AK"):
    d = f"{b}/ERC-CU-{st}-12012020-V01/ERC-CU-{st}-12012020-V01/RC-CU-{st}-12012020-V01/RC-CU-{st}-12012020-V01"
    top = ET.parse(f"{d}/RC-CU-{st}-12012020-V01.xml").getroot().find("Forms")
    stats, out = collections.Counter(), []
    for f in top.findall("Form"):
        walk(f, 0, stats, out)
    print("==", st, dict(stats))
    print("\n".join(out))
