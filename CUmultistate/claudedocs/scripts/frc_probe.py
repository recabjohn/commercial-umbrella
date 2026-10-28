import xml.etree.ElementTree as ET, sys, collections

b = sys.argv[1]
for st in ("AK", "CW"):
    d = f"{b}/ERC-CU-{st}-12012020-V01/ERC-CU-{st}-12012020-V01/RC-CU-{st}-12012020-V01/RC-CU-{st}-12012020-V01"
    r = ET.parse(f"{d}/FRC-CU-{st}-12012020-V01.xml").getroot()
    print("==", st, dict(collections.Counter(c.tag for c in r)))
    fm = r.find("Forms")
    tops = fm.findall("Form")
    print("top forms:", len(tops), "| all Form nodes:", sum(1 for _ in fm.iter("Form")))
    f0 = tops[0]
    print("top form children tags:", dict(collections.Counter(c.tag for c in f0)))
    print({t: f0.findtext(t) for t in ("Type", "Name", "TableName", "MinOccurs", "MaxOccurs")})
    fld = f0.find("Field")
    print("Field node:", None if fld is None else [c.tag for c in fld][:50])
    dt = r.find("DomainTable")
    print("DomainTable sample tags:", [c.tag for c in dt])
