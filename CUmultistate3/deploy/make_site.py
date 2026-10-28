"""Assemble the multistate static site: index.html (LOB) + risk.html + program.html, with flow wiring. Run: py -I make_site.py
Refresh rule: risk/program only open when reached through the flow (one-shot sessionStorage flag); any reload or direct hit goes to the LOB page.
Risk Next stores: cuRisk (one schedule row per state), cuRate (TC-style rating worksheet), cuRiskState (so Previous can replay the page).
"""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / "deploy" / "commercialumbrella3"
out.mkdir(exist_ok=True)
GUARD = "<script>if(!sessionStorage.getItem('cuFlow'))location.replace('./');else sessionStorage.removeItem('cuFlow')</script>"

lob = (root / "build/lob-page/cu_lob_screen.html").read_text("utf-8").replace(
    "</body>", "<script>document.getElementById('lob-next').addEventListener('click',()=>{sessionStorage.setItem('cuFlow','1');location.href='risk.html'})</script></body>")
risk = (root / "build/risk-page/cu_risk_screen.html").read_text("utf-8").replace("<head>", "<head>" + GUARD, 1).replace(
    "</body>", """<script>document.querySelector('.lobnav .btn').addEventListener('click',()=>{location.href='./'});
document.getElementById('next').addEventListener('click',()=>{
sessionStorage.setItem('cuRisk',JSON.stringify(riskRows()));
sessionStorage.setItem('cuRate',JSON.stringify(rate()));
sessionStorage.setItem('cuRiskState',JSON.stringify({forms:window.EXTRA_FORMS||[],pol:pol,states:ST_ROWS.filter(r=>r.acc).map(r=>({code:r.code,pol:r.pol})),rows:[...document.querySelectorAll('#after tr[data-saved]')].map(r=>({g:r._g,v:r._v}))}));
sessionStorage.setItem('cuFlow','1');location.href='program.html'})</script></body>""")
prog = (root / "build/program-page/cu_program_screen.html").read_text("utf-8").replace("<head>", "<head>" + GUARD, 1).replace(
    "</body>", "<script>document.getElementById('prev').addEventListener('click',()=>{sessionStorage.setItem('cuFlow','1');sessionStorage.setItem('cuRestore','1');location.href='risk.html'})</script></body>")
SAMP = next(p / 'samples' for p in Path(__file__).resolve().parents if (p / 'samples').exists())
risk = risk.replace('</head>', (SAMP / 'seed_v3.html').read_text('utf-8') + '</head>', 1).replace(
    '</body>', (SAMP / 'bar_v3.html').read_text('utf-8') + '</body>', 1)
assert "cuFlow" in lob and "cuFlow" in risk and "cuFlow" in prog
(out / "index.html").write_text(lob, "utf-8")
(out / "risk.html").write_text(risk, "utf-8")
(out / "program.html").write_text(prog, "utf-8")
print("site ready")
