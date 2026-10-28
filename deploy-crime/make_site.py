"""Assemble Crime-enabled site (index.html = LOB, risk.html = Risk) into deploy-crime/site. Run: py -I make_site.py
Same refresh rule as CU site. LOB Next stores ticked programs in sessionStorage 'cuLobs' -> Risk page shows one tab per ticked LOB (CU, Crime).
"""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / "deploy-crime" / "site"
out.mkdir(exist_ok=True)
lob = (root / "build-crime/lob-page/cu_lob_screen.html").read_text("utf-8").replace(
    "</body>", "<script>document.getElementById('lob-next').addEventListener('click',()=>{sessionStorage.setItem('cuFlow','1');"
    "sessionStorage.setItem('cuLobs',JSON.stringify([...document.querySelectorAll('#programs input:checked')].map(b=>b.value)));location.href='risk.html'})</script></body>")
risk = (root / "build-crime/risk-page/cu_risk_screen.html").read_text("utf-8").replace(
    "<head>", "<head><script>if(!sessionStorage.getItem('cuFlow'))location.replace('./');else sessionStorage.removeItem('cuFlow')</script>", 1).replace(
    "</body>", "<script>document.querySelector('.card .btn').addEventListener('click',()=>{location.href='./'})</script></body>")
assert "cuLobs" in lob and "cuFlow" in risk
(out / "index.html").write_text(lob, "utf-8")
(out / "risk.html").write_text(risk, "utf-8")
print("site ready", out)
