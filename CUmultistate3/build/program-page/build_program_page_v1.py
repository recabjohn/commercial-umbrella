"""Build the CU Program Selection screen (step 5), modelled on the default Solartis Program Selection page.
Rate Indication (dates read-only, 1-year term) + Risk Schedule (CU: one row per state policy, read from sessionStorage 'cuRisk')
Save (spinner) -> Get Available Carriers -> skeleton -> carrier cards. Premium is not rated in this prototype.
usage: py -I build_program_page.py <expand_panel.json> <logo.png> <out.html>
"""
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "risk-page"))
import build_risk_screen as risk  # noqa: E402

sh = risk.shell
sh.ACTIVE_STEP = 4                           # Program Selection
EFF, EXP = "10/23/2026", "10/23/2027"        # from the default Program Selection metadata (1-year term)
CARRIERS = ("Prime Insurance", "Solartis Insurance")  # from the default page's Available Carriers response

CSS = risk.CSS + """
.card h1,.rs h1{margin:0 0 6px;font-size:28px;font-weight:600;color:#555}
.ro select,.ro input{background:#f3f3f3;color:#777}
.rs{margin-top:34px}
.acts{display:flex;justify-content:flex-end;gap:70px;margin:26px 24px}
.btn.load{background:#adb5bd;opacity:1;cursor:wait}
.spin{display:inline-block;width:14px;height:14px;border:2px solid #fff;border-top-color:transparent;border-radius:50%;animation:sp .7s linear infinite;margin-left:8px;vertical-align:-2px}
@keyframes sp{to{transform:rotate(360deg)}}
.skel{height:20px;width:60%;background:#e0e0e0;border-radius:2px;margin:30px 0 0 30px}
.carrier{display:flex;align-items:center;gap:30px;background:#fff;border-radius:8px;box-shadow:0 1px 6px rgba(0,0,0,.15);padding:18px 22px;margin:14px 4px}
.carrier .tp{font-size:14px;line-height:1.5;width:110px}.carrier .nm{width:200px;font-size:15px}
.carrier .lnk{color:#1f9bd7;font-size:17px;min-width:140px;text-align:center;cursor:pointer}
.carrier .btn{margin-left:auto}.carrier .btn~.btn{margin-left:30px}
"""

JS = r"""
const $=(s,e=document)=>e.querySelector(s),esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let R=[];try{R=JSON.parse(sessionStorage.getItem('cuRisk')||'[]')}catch(e){}
$('#st').innerHTML=(R.length?R:[{state:''}]).map(r=>`<option>${esc(r.state)}</option>`).join('');
$('#rs tbody').innerHTML=R.length?R.map(r=>`<tr><td>CU</td><td>${esc(r.state)}</td><td>${esc(r.form)}</td><td>${esc(r.limit)}</td><td>${esc(r.sir)}</td><td>${esc(r.underlying)}</td></tr>`).join(''):'<tr><td class="none" colspan="6">No Records To Display.</td></tr>';
$('#rc').textContent=R.length?`1-${R.length} of ${R.length}`:'0-0 of 0';
const toast=t=>{const e=document.createElement('div');e.className='toast';e.textContent=t;document.body.append(e);setTimeout(()=>e.remove(),2200)};
const busy=(b,on)=>{b.disabled=on;b.classList.toggle('load',on);$('.spin',b)?.remove();if(on)b.insertAdjacentHTML('beforeend','<i class="spin"></i>')};
const sv=$('#sv'),gac=$('#gac'),cars=$('#cars');
sv.onclick=()=>{busy(sv,true);setTimeout(()=>{busy(sv,false);gac.classList.remove('hide');toast('Saved Successfully')},1000)};
gac.onclick=()=>{busy(gac,true);cars.innerHTML='<div class="skel"></div>';
 setTimeout(()=>{busy(gac,false);cars.innerHTML=CARRIERS.map(c=>`<div class="carrier"><div class="tp">Total Premium<br>&mdash;</div><div class="nm">${esc(c)}</div>
  <span class="lnk">Subjectivities</span><span class="lnk">Forms</span><button class="btn" type="button">Preview Rating Worksheet</button>
  <button class="btn" type="button">Preview Quote</button><button class="btn" type="button">Create Quote</button></div>`).join('');
  cars.querySelectorAll('.btn,.lnk').forEach(b=>b.onclick=()=>toast('Prototype: not wired'))},1200)};
"""


def fld(label: str, val: str, ident: str = "", kind: str = "input", opts: tuple = ()) -> str:
    """kind: input (read-only) or select (editable)."""
    if kind == "select":
        o = "".join(f"<option{' selected' if x == val else ''}>{x}</option>" for x in opts)
        return f'<div class="fld"><label>{label}</label><select id="{ident}">{o}</select></div>'
    return f'<div class="fld ro"><label>{label}</label><input value="{val}" disabled></div>'


def screen(expand: dict, logo: str) -> str:
    body = (f'{sh.steps()}{sh.details(expand)}'
            '<form class="card" onsubmit="return false"><h1>Rate Indication</h1><div class="grid2">'
            f'{fld("Subline *", "CU", "sl", "select", ("CU",))}{fld("State *", "", "st", "select")}'
            f'{fld("Effective Date", EFF)}{fld("Expiration Date", EXP)}'
            f'{fld("Billing Type", "Agency Bill", "bt", "select", ("Agency Bill", "Direct Bill"))}{fld("Quote Type", "New Business")}</div></form>'
            '<div class="rs"><h1>Risk Schedule</h1>'
            '<div class="tbl" id="rs"><table><thead><tr><th>Subline</th><th>State</th><th>Policy Coverage Form</th><th>Umbrella / Excess Limit</th>'
            '<th>Self Insured Retention</th><th>Underlying Insurance</th></tr></thead><tbody></tbody></table>'
            '<div class="rows"><span>Rows per page: 5</span><span id="rc"></span></div></div></div>'
            '<div class="acts"><button class="btn" type="button" id="sv">Save</button>'
            '<button class="btn hide" type="button" id="gac">Get Available Carriers</button></div><div id="cars"></div>'
            '<div class="lobnav" style="margin:24px 0 0"><button class="btn" type="button" id="prev">Previous</button></div>')
    foot = ('<footer class="footer"><span><a href="https://solartis.com" target="_blank" rel="noopener noreferrer">Solartis</a> &copy; 2026</span>'
            '<span>Powered by <a href="https://solartis.com" target="_blank" rel="noopener noreferrer">Solartis</a></span></footer>')
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Program Selection - Commercial Umbrella</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">'
            f'<style>{sh.CSS}{CSS}</style></head><body>{sh.header(logo)}{sh.sidebar()}<main class="main"><div class="page">{body}</div>{foot}</main>'
            f'<button class="fab" aria-label="AI Assistant">{sh.svg(sh.ICON["chat"])}</button>'
            f'<script>const CARRIERS={json.dumps(CARRIERS)};{JS}</script></body></html>')


if __name__ == "__main__":
    exp, logo, out = (Path(a) for a in sys.argv[1:4])
    uri = "data:image/png;base64," + base64.b64encode(logo.read_bytes()).decode("ascii")
    out.write_text(screen(json.loads(exp.read_text("utf-8")), uri), encoding="utf-8")
    print("wrote", out)
