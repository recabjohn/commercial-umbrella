"""Build the CU Risk/Coverage screen as one standalone HTML file (Solartis style).

Shell (header, sidebar, step bar, Details strip, footer) is reused from ../lob-page/build_screen.py.
Body is rendered in the browser from the metadata JSON embedded below, following the GL runtime flow:
State (+) -> State picked -> Policy fields -> Save -> Additional Coverages + Risk Schedule ->
Underlying Insurance Information -> one table per risk group (+) -> in-row Detail -> Save.

usage: py -I build_risk_screen.py <metadata dir> <expand_panel.json> <logo.png> <out.html>
"""
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lob-page"))
import build_screen as shell  # noqa: E402

shell.ACTIVE_STEP = 3                        # Risk/Coverage
LOBS = {"Commercial Umbrella": "lob-cu", "Crime": "lob-crime"}        # tab label -> panel id
CRIME_JS = (Path(__file__).resolve().parent / "crime.js").read_text("utf-8")

CSS = """
.tabs{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:14px}.tabs .childtab{margin-bottom:0;border:0;cursor:pointer;font-family:inherit;color:#111}.tabs .childtab.on{box-shadow:0 2px 0 #1976d2,0 1px 6px rgba(0,0,0,.15);font-weight:700}
.rad{display:flex;gap:18px;height:40px;align-items:center;font-size:16px}.rad label{margin:0;font-size:16px;color:#111}.fld textarea{border:1px solid #b9b9b9;border-radius:7px;padding:8px 14px;font:inherit;font-size:16px}
.childtab{display:inline-flex;align-items:center;gap:10px;background:#fff;border-radius:8px;box-shadow:0 1px 6px rgba(0,0,0,.15);padding:18px 24px;margin-bottom:14px;font-size:16px;text-decoration:underline}
.childtab svg{width:22px;height:22px}
.card{background:#fff;border-radius:10px;box-shadow:0 1px 6px rgba(0,0,0,.15);padding:14px 30px 26px;margin-top:6px}
.acc{margin:6px 0}
.acc>.acc-h{display:flex;align-items:center;gap:8px;min-height:54px;cursor:pointer}
.acc-h h2{margin:0;font-size:22px;font-weight:700;text-transform:uppercase;color:#111}
.acc-h .chev{width:24px;height:24px;transition:transform .2s;color:#555}
.acc.closed>.acc-h .chev{transform:rotate(-90deg)}
.acc.closed>.acc-b{display:none}
.acc .acc{margin-left:20px}
.plus{border:0;background:none;padding:0;color:#1976d2;cursor:pointer}.plus svg{width:26px;height:26px}.plus.grey{color:#666}
.fld{margin:12px 0 4px;display:flex;flex-direction:column}
.fld label{font-size:11px;color:#444;margin:0 0 2px 6px}
.fld select,.fld input{height:40px;border:1px solid #b9b9b9;border-radius:7px;padding:0 14px;font:inherit;font-size:16px;background:#fff;min-width:0}
.fld select:focus,.fld input:focus{outline:2px solid #52779a;border-color:#52779a}
.fld.err select,.fld.err input{border-color:#f44336}.fld .msg{font-size:12px;color:#f44336;min-height:0}
.out{display:flex;margin:14px 0;font-size:14px;color:#222}.out span:first-child{width:51.5%}
.sub{margin:20px 0 0;font-size:20px;font-weight:500}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:0 24px}
.save{display:flex;justify-content:flex-end;margin-top:14px}
.tbl{margin:8px 0 6px 0;box-shadow:0 2px 6px rgba(0,0,0,.25);border-radius:6px;overflow:hidden}
.tbl table{width:100%;border-collapse:collapse;font-size:14px}
.tbl th{background:#e3eef5;font-weight:600;text-align:left;padding:11px 12px}
.tbl td{padding:10px 12px;border-top:1px solid #eee;vertical-align:top}
.tbl .none{text-align:center;font-weight:700;padding:10px}
.tbl td.exp{padding:6px 18px 18px;background:#fff}
.tbl .ex,.tbl .more{border:0;background:none;cursor:pointer;color:#444}
.tbl .ex .chev{width:24px;height:24px;transition:transform .2s}.tbl tr.open .ex .chev{transform:rotate(180deg)}
.tbl .more{position:relative}
.tbl .rows{display:flex;justify-content:flex-end;gap:22px;padding:12px 24px;font-size:13px;border-top:1px solid #eee}
.sec{font-size:20px;color:#555;margin:22px 0 0;display:flex;align-items:center;gap:8px}
.note{text-align:right;font-size:14px;color:#333;margin:34px 6px 24px}
.toast{position:fixed;top:80px;right:24px;background:#2e7d32;color:#fff;padding:12px 18px;border-radius:6px;z-index:60;box-shadow:0 2px 8px rgba(0,0,0,.3)}
.toast.bad{background:#c62828}
.hide{display:none!important}
.rule-err{color:#c62828;font-size:14px;margin:10px 0 0;text-align:right}
"""

JS = r"""
const M=JSON.parse(document.getElementById('meta').textContent);
const $=(s,e=document)=>e.querySelector(s),H=(h)=>{const t=document.createElement('template');t.innerHTML=h.trim();return t.content.firstChild};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const chev='<svg class="chev" viewBox="0 0 24 24"><path fill="currentColor" d="M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6z"/></svg>';
const plus='<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2m5 11h-4v4h-2v-4H7v-2h4V7h2v4h4z"/></svg>';
const PANELS=M.panels,NUM=['Decimal','Integer','Number'],state={policySaved:false,rows:0},CURV=new WeakMap();
function toast(t,bad){const e=H(`<div class="toast${bad?' bad':''}">${esc(t)}</div>`);document.body.append(e);setTimeout(()=>e.remove(),2200)}
function cond(c,v){if(!c)return true;
 if(!/^[\w\s.'=|&()\-,\/\[\]]+$/.test(c))return true;               // whitelist before evaluating FRC condition text
 const e=c.replace(/(\w+)\[((?:\.='[^']*'(?:\s+or\s+)?)+)\]/g,(m,n,b)=>'('+b.split(/\s+or\s+/).map(p=>`v.${n}==='${p.slice(3,-1)}'`).join('||')+')')
  .replace(/(\w+)\s*=\s*'([^']*)'/g,(m,n,s)=>`v.${n}==='${s}'`).replace(/\bor\b/g,'||').replace(/\band\b/g,'&&');
 try{return !!Function('v','return '+e)(v)}catch(x){return true}}
function accordion(title,body,extra='',closed=false){const a=H(`<section class="acc${closed?' closed':''}"><div class="acc-h">${chev}<h2>${esc(title)}</h2>${extra}</div><div class="acc-b"></div></section>`);
 $('.acc-b',a).append(body);$('.acc-h',a).addEventListener('click',e=>{if(!e.target.closest('button'))a.classList.toggle('closed')});return a}
function fieldEl(a,v,onchange){
 if(a.IsInvisible==='Y')return null;const lab=a.ComponentLabel+(a.IsRequired==='Y'?' *':'');
 if(a.ComponentType==='Subheading')return H(`<h3 class="sub" data-cond="${esc(a.Custom1)}">${esc(lab)}</h3>`);
 if(a.ComponentType==='outputText'||a.ComponentType==='OutputText')return H(`<div class="out" data-cond="${esc(a.Custom1)}"><span>${esc(lab)}</span><span>${esc(a.DefaultValue)}</span></div>`);
 const n=a.AttributeName,id='f_'+Math.random().toString(36).slice(2,8);
 const ctl=a.ComponentType.toUpperCase().startsWith('SELECT')
  ?`<select id="${id}">${(a.SubApplicationAttributeValueList.some(o=>o.Value==='')?'':'<option value="">Select</option>')+a.SubApplicationAttributeValueList.map(o=>`<option value="${esc(o.Value)}">${esc(o.DisplayValue)}</option>`).join('')}</select>`
  :`<input id="${id}" type="${a.ComponentType==='Date'?'date':NUM.includes(a.AttributeDataType)?'number':'text'}"${NUM.includes(a.AttributeDataType)?` step="${a.AttributeDataType==='Decimal'?1/10**(+a.Custom5||2):1}" min="${a.MinValue}"${a.MaxValue!=='0'?` max="${a.MaxValue}"`:''}`:a.MaxLength?` maxlength="${a.MaxLength}"`:''} placeholder="${esc(a.PlaceHolderText)}">`;
 const el=H(`<div class="fld" data-cond="${esc(a.Custom1)}" title="${esc(a.Tooltip)}"><label for="${id}">${esc(lab)}</label>${ctl}<div class="msg"></div></div>`);
 const c=$('select,input',el);c.value=v[n]??a.DefaultValue;v[n]=c.value;
 c.addEventListener('input',()=>{v[n]=c.value;el.classList.remove('err');$('.msg',el).textContent='';onchange&&onchange(n)});
 el._a=a;CURV.set(el,v);return el}
function ruleErr(rules,v,root){const n=k=>parseFloat(v[k])||0,out=[];
 for(const r of rules){
  if(r.t==='allZero'&&r.f.every(k=>!(n(k)>0)))out.push(r.msg);
  else if(r.t==='limitNeedsPremium'&&v[r.limit]&&v[r.limit]!=='Not Applicable'&&n(r.prem)===0)out.push(r.msg);
  else if(r.t==='premiumNeedsLimit'&&(!v[r.limit]||v[r.limit]==='Not Applicable')&&n(r.prem)!==0)out.push(r.msg);
  else if(r.t==='gt0'){const f=[...root.querySelectorAll('.fld')].find(e=>e._a&&e._a.AttributeName===r.f);if(f&&!f.classList.contains('hide')&&n(r.f)<=0)out.push(r.msg)}}
 return out}
function showRules(host,errs){let e=host.querySelector(':scope>.rule-err');if(!e){e=H('<div class="rule-err"></div>');host.querySelector('.save').before(e)}e.innerHTML=errs.map(m=>`<div>${esc(m)}</div>`).join('')}
function refresh(root,v){root.querySelectorAll('[data-cond]').forEach(e=>e.classList.toggle('hide',!cond(e.dataset.cond,v)))}
function validate(root){let ok=true;root.querySelectorAll('.fld').forEach(f=>{if(f.classList.contains('hide')||!f._a)return;
 const c=$('select,input',f);if(f._a.IsRequired==='Y'&&cond(f._a.Custom2,CURV.get(f))&&!c.value){ok=false;f.classList.add('err');$('.msg',f).textContent=f._a.RequiredMessage}});return ok}
function form(attrs,v,after){const w=H('<div></div>');attrs.filter(a=>a.ComponentType!=='SubmitV3').forEach(a=>{const e=fieldEl(a,v,()=>refresh(w,v));e&&w.append(e)});refresh(w,v);return w}
const sub=t=>M.groups.find(s=>s.TileName===t);
// ---- policy ----
const pol={},policyAttrs=M.policy.AttributeDetailList,stateAttr=policyAttrs[0];
const polBody=H('<div></div>'),polHost=H('<div></div>');
polBody.append(polHost);
const stateAcc=accordion('Policy',polBody,`<button type="button" class="plus" aria-label="Add Policy">${plus}</button>`);
let rest=null,after=null;
function openPolicy(){if(polHost.firstChild)return;
 const sf=fieldEl(stateAttr,pol,()=>{if(pol.State&&!rest)showRest();});polHost.append(sf);polHost._sf=sf}
function showRest(){rest=form(policyAttrs.slice(1),pol);polHost.append(rest);
 const b=H('<div class="save"><button type="button" class="btn">Save</button></div>');polHost.append(b);
 $('button',b).onclick=()=>{const sf=polHost._sf;if(!validate(polHost)){toast('Please complete the required fields',1);return}
  const pe=ruleErr(M.rules.policy,pol,polHost);showRules(polHost,pe);if(pe.length){toast(pe[0],1);return}
  toast('Policy Saved Successfully');state.policySaved=true;showAfter();sync()}}
$('.plus',stateAcc).onclick=openPolicy;
// ---- additional coverages + risk schedule ----
function table(cols,onadd,title,big){const t=H(`<div class="tbl"><table><thead><tr><th></th>${cols.map(c=>`<th>${esc(c)}</th>`).join('')}<th>Action</th></tr></thead><tbody></tbody></table></div>`);
 const none=()=>{if(!$('tr',$('tbody',t)))$('tbody',t).append(H(`<tr class="nr"><td class="none" colspan="${cols.length+2}">No Records To Display.</td></tr>`))};none();t._none=none;return t}
function section(title,onadd){const h=H(`<h3 class="sec">${esc(title)}<button type="button" class="plus grey" aria-label="Add">${plus}</button></h3>`);$('.plus',h).onclick=onadd;return h}
function underlying(g){const s=sub(g),d=sub(g+'Detail'),max=s.mAction.addRow.maxRows,cols=s.AttributeDetailList.map(a=>a.ComponentLabel),host=H('<div></div>');
 const t=table(cols);
 host.append(section(s.Description,()=>addRow()),t);
 function addRow(){$('.nr',t)?.remove();const v={},body=$('tbody',t),
   tr=H(`<tr data-row="1"><td><button type="button" class="ex" aria-label="Expand">${chev}</button></td>${cols.map(()=>'<td></td>').join('')}<td><button type="button" class="more" aria-label="Actions">&#8942;</button></td></tr>`),
   dr=H(`<tr><td class="exp" colspan="${cols.length+2}"></td></tr>`),f=form(d.AttributeDetailList,v);
  $('.exp',dr).append(f,H('<div class="save"><button type="button" class="btn">Save</button></div>'));
  $('.btn',dr).onclick=()=>{if(!validate(f)){toast('Please complete the required fields',1);return}
   const ge=ruleErr(M.rules.groups[s.Description]||[],v,f);showRules($('.exp',dr),ge);if(ge.length){toast(ge[0],1);return}
   [...tr.children].slice(1,-1).forEach((td,i)=>td.textContent=v[s.AttributeDetailList[i].AttributeName]||'');
   dr.classList.add('hide');tr.dataset.saved=1;toast('Saved Successfully');sync()};
  $('.ex',tr).onclick=()=>dr.classList.toggle('hide');
  $('.more',tr).onclick=()=>{if(confirm('Delete this record?')){tr.remove();dr.remove();t._none();$('.plus',host).classList.remove('hide');sync()}};
  body.append(tr,dr);if(body.querySelectorAll('tr[data-row]').length>=max)$('.plus',host).classList.add('hide')}
 return host}
function showAfter(){if(after)return;const ui=H('<div></div>');
 ui.append(...M.groupNames.map(underlying));
 after=H('<div></div>');
 const ac=H('<div></div>');ac.append(section('Additional Coverages',()=>toast('Additional coverage dialog is out of scope for this prototype')),table(['Coverage']));
 after.append(ac,accordion('Underlying Insurance Information',ui,'',true));$('#after').append(after)}
// ---- nav ----
const next=$('#next');
const LOBS=(()=>{try{const a=JSON.parse(sessionStorage.getItem('cuLobs'));if(Array.isArray(a))return a}catch(e){}return Object.keys(PANELS)})().filter(l=>PANELS[l]);
const lobOk={'Commercial Umbrella':()=>state.policySaved&&document.querySelector('#after tr[data-saved]'),'Crime':()=>crimeState.policySaved};
function sync(){next.disabled=!LOBS.every(l=>lobOk[l]())}
$('#state').append(stateAcc);
""" + CRIME_JS + r"""
sync();
$('#tabs').append(...LOBS.map(l=>{const b=H(`<button type="button" class="childtab">${esc(l)}</button>`);b.onclick=()=>show(l);b.dataset.l=l;return b}));
function show(l){Object.entries(PANELS).forEach(([k,id])=>document.getElementById(id).classList.toggle('hide',k!==l));document.querySelectorAll('#tabs .childtab').forEach(b=>b.classList.toggle('on',b.dataset.l===l))}
show(LOBS[0]);
"""


def screen(meta: dict, expand: dict, logo: str) -> str:
    sh = shell
    note = meta["page"]["ApplicationDetail"]["SubApplicationDetailList"][0]["AttributeDetailList"][0]["ComponentLabel"]
    body = (f'{sh.steps()}<div class="tabs" id="tabs"></div>{sh.details(expand)}'
            '<form class="card" onsubmit="return false"><div id="lob-cu"><div id="state"></div><div id="after"></div>'
            f'<div class="note">{note} *</div></div><div id="lob-crime" class="hide"><div id="crime-policy"></div><div id="crime-after"></div></div>'
            '<div class="lobnav" style="margin:0"><button class="btn" type="button">Previous</button>'
            '<button class="btn" type="button" id="next" disabled>Next</button></div></form>')
    foot = ('<footer class="footer"><span><a href="https://solartis.com" target="_blank" rel="noopener noreferrer">Solartis</a> &copy; 2026</span>'
            '<span>Powered by <a href="https://solartis.com" target="_blank" rel="noopener noreferrer">Solartis</a></span></footer>')
    payload = json.dumps(meta, separators=(",", ":")).replace("</", r"<\/")
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Risk/Coverage - Commercial Umbrella and Crime</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">'
            f'<style>{sh.CSS}{CSS}</style></head><body>{sh.header(logo)}{sh.sidebar()}<main class="main"><div class="page">{body}</div>{foot}</main>'
            f'<div class="code-tab" aria-label="Show request/response">{sh.svg("M8 6l-6 6 6 6M16 6l6 6-6 6").replace("<svg", "<svg fill=none stroke=currentColor stroke-width=2.2 width=20 height=20")}</div>'
            f'<button class="fab" aria-label="AI Assistant">{sh.svg(sh.ICON["chat"])}</button>'
            f'<script type="application/json" id="meta">{payload}</script><script>{JS}</script></body></html>')


def load(d: Path) -> dict:
    j = lambda n: json.loads((d / f"{n}_metadata.json").read_text("utf-8"))["ApplicationDetail"]["SubApplicationDetailList"]  # noqa: E731
    groups = j("cu_risk_groups")
    return {"page": json.loads((d / "cu_risk_page_metadata.json").read_text("utf-8")), "policy": j("cu_policy_detail")[0], "groups": groups,
            "groupNames": [s["TileName"] for s in groups if s["Type"] == "Summary"],
            "rules": json.loads((d / "cu_validation_rules.json").read_text("utf-8")),
            "crime": json.loads((d / "crime_metadata.json").read_text("utf-8")), "panels": LOBS}


if __name__ == "__main__":
    d, exp, logo, out = (Path(a) for a in sys.argv[1:5])
    uri = "data:image/png;base64," + base64.b64encode(logo.read_bytes()).decode("ascii")
    out.write_text(screen(load(d), json.loads(exp.read_text("utf-8")), uri), encoding="utf-8")
    print("wrote", out)
