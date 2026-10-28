"""Assemble the static site: index.html (LOB) + risk.html, with flow wiring. Run: py -I make_site.py
Refresh rule: risk.html only opens when reached via LOB Next (one-shot sessionStorage flag); any reload or direct hit goes to the LOB page.
"""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / "deploy" / "commercialumbrella"
out.mkdir(exist_ok=True)

lob = (root / "build/lob-page/cu_lob_screen.html").read_text("utf-8").replace(
    "</body>", "<script>document.getElementById('lob-next').addEventListener('click',()=>{sessionStorage.setItem('cuFlow','1');location.href='risk.html'})</script></body>")
risk = (root / "build/risk-page/cu_risk_screen.html").read_text("utf-8").replace(
    "<head>", "<head><script>if(!sessionStorage.getItem('cuFlow'))location.replace('./');else sessionStorage.removeItem('cuFlow')</script>", 1).replace(
    "</body>", "<script>document.querySelector('.lobnav .btn').addEventListener('click',()=>{location.href='./'})</script></body>")
risk = risk.replace("</body>", """<script>document.getElementById('next').addEventListener('click',()=>{
const nm=c=>{const o=stateAttr.SubApplicationAttributeValueList.find(x=>x.Value===c);return o?o.DisplayValue:c};
sessionStorage.setItem('cuRisk',JSON.stringify([{state:pol.State,form:pol.PolicyCoverageForm||'',
 limit:(pol.PolicyCoverageForm==='Commercial Excess Liability'?pol.ExcessLiabilityLimit:pol.Limit)||'',
 sir:(pol.PolicyCoverageForm==='Commercial Excess Liability'?pol.ExcessLiabilitySelfInsuredRetention:pol.SelfInsuredRetention)||'',
 underlying:document.querySelectorAll('#after tr[data-saved]').length+' saved'}]));
sessionStorage.setItem('cuRate',JSON.stringify(rate()));
sessionStorage.setItem('cuRiskState',JSON.stringify({forms:window.EXTRA_FORMS||[],pol:pol,rows:[...document.querySelectorAll('#after tr[data-saved]')].map(r=>({g:r._g,v:r._v}))}));
sessionStorage.setItem('cuFlow','1');location.href='program.html'})</script></body>""")
prog = (root / "build/program-page/cu_program_screen.html").read_text("utf-8").replace(
    "<head>", "<head><script>if(!sessionStorage.getItem('cuFlow'))location.replace('./');else sessionStorage.removeItem('cuFlow')</script>", 1).replace(
    "</body>", "<script>document.getElementById('prev').addEventListener('click',()=>{sessionStorage.setItem('cuFlow','1');sessionStorage.setItem('cuRestore','1');location.href='risk.html'})</script></body>")
(out / "program.html").write_text(prog, "utf-8")
SAMP = next(p / 'samples' for p in Path(__file__).resolve().parents if (p / 'samples').exists())
risk = risk.replace('</head>', (SAMP / 'seed_single.html').read_text('utf-8') + '</head>', 1).replace(
    '</body>', (SAMP / 'bar_single.html').read_text('utf-8') + '</body>', 1)
assert "cuFlow" in lob and "cuFlow" in risk
(out / "index.html").write_text(lob, "utf-8")
(out / "risk.html").write_text(risk, "utf-8")
print("site ready")
