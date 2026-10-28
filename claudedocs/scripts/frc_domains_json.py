"""Export full picklist values for chosen FRC domain tables to JSON.
usage: py -I frc_domains_json.py <batch dir> <out.json> <domain>...
"""
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

batch, out, want = Path(sys.argv[1]), Path(sys.argv[2]), set(sys.argv[3:])
d = batch / "ERC-CU-AK-12012020-V01" / "ERC-CU-AK-12012020-V01" / "RC-CU-AK-12012020-V01" / "RC-CU-AK-12012020-V01"
root = ET.parse(d / "FRC-CU-AK-12012020-V01.xml").getroot()
res = {dt.findtext("Name"): [e.findtext("DataValue") for e in dt.findall("DomainTableEntry")]
       for dt in root.findall("DomainTable") if dt.findtext("Name") in want}
missing = want - set(res)
assert not missing, missing
out.write_text(json.dumps(res, indent=1), encoding="utf-8")
print({k: len(v) for k, v in res.items()})
