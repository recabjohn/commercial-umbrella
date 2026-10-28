"""One-off: remove the Multi-State Summary (and its proposal checks) from the multistate Risk screen."""
import re

p = "build_risk_screen.py"
s = open(p, encoding="utf-8").read()
m = re.search(r"function summary\(\)\{.*?</div></div>`\)\)\}\n", s, re.S)
assert m, "summary() not found"
s = s.replace(m.group(0), "", 1)
for a, b in (("fillPicker();summary()}", "fillPicker()}"), ("showPremium();summary()}", "showPremium()}"),
             ('<div id="after"></div><div id="summary"></div>', '<div id="after"></div>')):
    assert a in s, a
    s = s.replace(a, b, 1)
s = re.sub(r"const STATES=\[\],MONO=\['ND','OH','WA','WY'\];", "const STATES=[];", s, count=1)
s = re.sub(r"const MIN=\[\[.*?\]\];\n", "", s, count=1, flags=re.S)
assert "summary" not in s.replace("// ---- States", ""), [x for x in re.findall(r".{30}summary.{30}", s)]
open(p, "w", encoding="utf-8").write(s)
print("removed")
