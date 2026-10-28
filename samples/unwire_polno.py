"""Revert wire_polno.py: remove the sample policy number row from all four sites."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
NO = ("(sessionStorage.getItem('cuPolNo')||(()=>{const n='POL-'+String(Math.floor(Math.random()*1e7)).padStart(7,'0');"
      "sessionStorage.setItem('cuPolNo',n);return n})())")
ROW = "H('<div class=\"out\"><span>Policy Number</span><span>'+" + NO + "+'</span></div>')"

for base in (root, root / "CUmultistate", root / "CUmultistate3"):
    p = base / "build/risk-page/build_risk_screen.py"
    s = p.read_text("utf-8")
    a = "polBody.append(" + ROW + ");polBody.append(polHost);"
    assert a in s, p
    p.write_text(s.replace(a, "polBody.append(polHost);", 1), "utf-8")

p = root / "CUmultistate4/build/risk-page/build_risk_screen.py"
s = p.read_text("utf-8")
a = " polBody.prepend(" + ROW + ");   // sample policy number (random placeholder)\n"
assert a in s
p.write_text(s.replace(a, "", 1), "utf-8")
for base in (root, root / "CUmultistate", root / "CUmultistate3", root / "CUmultistate4"):
    assert "Policy Number" not in (base / "build/risk-page/build_risk_screen.py").read_text("utf-8"), base
print("reverted")
