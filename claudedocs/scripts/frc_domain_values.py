import sys
import xml.etree.ElementTree as ET
from pathlib import Path

batch = Path(sys.argv[1])
want = sys.argv[2:]
d = batch / "ERC-CU-AK-12012020-V01" / "ERC-CU-AK-12012020-V01" / "RC-CU-AK-12012020-V01" / "RC-CU-AK-12012020-V01"
root = ET.parse(d / "FRC-CU-AK-12012020-V01.xml").getroot()
for dt in root.findall("DomainTable"):
    name = dt.findtext("Name")
    if name in want:
        vals = [e.findtext("DataValue") for e in dt.findall("DomainTableEntry")]
        print(name, len(vals), vals[:25])
