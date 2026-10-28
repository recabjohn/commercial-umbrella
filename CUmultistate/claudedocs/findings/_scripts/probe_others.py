"""Probe other systems for entity hierarchy: Entity Hierarchy xlsx sheet names + savesubmission JSON structure.

usage: py -I probe_others.py <CF template dir>
"""
import json
import re
import sys
import zipfile
from pathlib import Path

d = Path(sys.argv[1])

# 1. Entity Hierarchy workbook: list sheets without openpyxl (style bug), via workbook.xml
x = next(d.glob("SWP_1_Entity Hierarchy*.xlsx"))
with zipfile.ZipFile(x) as z:
    wb = z.read("xl/workbook.xml").decode("utf-8")
    print("SHEETS:", re.findall(r'<sheet [^>]*name="([^"]+)"', wb))


# 2. savesubmission JSON: print key tree to depth 5, collapsing lists to first element
def tree(node, depth, max_depth, name="$"):
    pad = "  " * depth
    if isinstance(node, dict):
        print(f"{pad}{name} {{{len(node)} keys}}")
        if depth < max_depth:
            for k, v in node.items():
                if isinstance(v, (dict, list)):
                    tree(v, depth + 1, max_depth, k)
    elif isinstance(node, list):
        print(f"{pad}{name} [list x{len(node)}]")
        if node and depth < max_depth:
            tree(node[0], depth + 1, max_depth, name + "[0]")


for fn in ("Gl savesubmission.json", "AU savesubmission.json", "CF submission 1.json"):
    print("\n=====", fn)
    data = json.loads((d / fn).read_text(encoding="utf-8"))
    tree(data, 0, 6)
