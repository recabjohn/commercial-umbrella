"""One-off: show a random sample policy number (POL- + 7 digits, kept for the browser session) at the top of the Policy section on all four sites."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
NO = ("(sessionStorage.getItem('cuPolNo')||(()=>{const n='POL-'+String(Math.floor(Math.random()*1e7)).padStart(7,'0');"
      "sessionStorage.setItem('cuPolNo',n);return n})())")
ROW = "H('<div class=\"out\"><span>Policy Number</span><span>'+" + NO + "+'</span></div>')"

for base in (root, root / "CUmultistate", root / "CUmultistate3"):
    p = base / "build/risk-page/build_risk_screen.py"
    s = p.read_text("utf-8")
    a = "function openPolicy(){if(polHost.firstChild)return;polBody.append(polHost);"
    assert a in s, p
    s = s.replace(a, "function openPolicy(){if(polHost.firstChild)return;polBody.append(" + ROW + ");polBody.append(polHost);", 1)
    p.write_text(s, "utf-8")

p = root / "CUmultistate4/build/risk-page/build_risk_screen.py"
s = p.read_text("utf-8")
a = "polHost.append(H('<div class=\"out\"><span>Policy Number</span><span>POL-0000000</span></div>'));   // sample policy number (placeholder)"
assert a in s
s = s.replace(a, "polHost.append(" + ROW + ");   // sample policy number (random placeholder)", 1)
p.write_text(s, "utf-8")
print("ok")
