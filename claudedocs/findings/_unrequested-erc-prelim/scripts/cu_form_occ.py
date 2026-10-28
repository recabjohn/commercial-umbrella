import xml.etree.ElementTree as ET, sys, collections

b = sys.argv[1]
f = f"{b}/ERC-CU-CW-12012020-V01/ERC-CU-CW-12012020-V01/RC-CU-CW-12012020-V01/RC-CU-CW-12012020-V01/RC-CU-CW-12012020-V01.xml"
top = ET.parse(f).getroot().find("Forms")
c = collections.Counter()
for x in top.iter("Form"):
    t = x.findtext("Type")
    key = (t, x.findtext("MinOccurs"), x.findtext("MaxOccurs"),
           "cond" if x.findtext("Condition") else "nocond",
           "attach" if x.findtext("AttachmentCondition") else "noattach")
    c[key] += 1
for k, v in sorted(c.items()):
    print(v, k)
