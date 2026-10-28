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
TAB = "Commercial Umbrella"

CSS = """
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
.tbl .more{position:relative}
.tbl .rows{display:flex;justify-content:flex-end;gap:22px;padding:12px 24px;font-size:13px;border-top:1px solid #eee}
.sec{font-size:20px;color:#555;margin:22px 0 0;display:flex;align-items:center;gap:8px}
.note{text-align:right;font-size:14px;color:#333;margin:34px 6px 24px}
.toast{position:fixed;top:80px;right:24px;background:#2e7d32;color:#fff;padding:12px 18px;border-radius:6px;z-index:60;box-shadow:0 2px 8px rgba(0,0,0,.3)}
.toast.bad{background:#c62828}
.hide{display:none!important}.warn{color:#8a5a00;font-size:13px}.prop{font-style:normal;color:#8a5a00;font-size:11px;font-weight:400}
.tags .chips{display:flex;flex-wrap:wrap;gap:6px 18px;padding:6px 6px}.tags .chips label{display:flex;gap:6px;align-items:center;font-size:14px;color:#222;margin:0}
.fld.tags.err .chips{outline:1px solid #f44336;border-radius:6px}
.tbl .ex .chev{width:22px;height:22px;transition:transform .2s}.tbl .ex.open .chev{transform:rotate(180deg)}
.tbl td:last-child{position:relative}
.menu{position:absolute;right:14px;top:4px;background:#fff;border-radius:6px;box-shadow:0 2px 10px rgba(0,0,0,.3);z-index:30}
.menu button{border:0;background:none;padding:12px 20px;font:inherit;font-size:15px;cursor:pointer}
.acc-h .chev{flex:none}
.rule-err{color:#c62828;font-size:14px;margin:10px 0 0;text-align:right}
"""

JS = r"""
const M=JSON.parse(document.getElementById('meta').textContent);
const $=(s,e=document)=>e.querySelector(s),H=(h)=>{const t=document.createElement('template');t.innerHTML=h.trim();return t.content.firstChild};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const chev='<svg class="chev" viewBox="0 0 24 24"><path fill="currentColor" d="M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6z"/></svg>';
const plus='<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2m5 11h-4v4h-2v-4H7v-2h4V7h2v4h4z"/></svg>';
const NUM=['Decimal','Integer','Number'],state={policySaved:false,rows:0},CURV=new WeakMap();
function toast(t,bad){if(window.QUIET)return;const e=H(`<div class="toast${bad?' bad':''}">${esc(t)}</div>`);document.body.append(e);setTimeout(()=>e.remove(),2200)}
function cond(c,v){if(!c)return true;
 if(!/^[\w\s.'=|&()\-,\/\[\]]+$/.test(c))return true;               // whitelist before evaluating FRC condition text
 const e=c.replace(/(\w+)\[((?:\.='[^']*'(?:\s+or\s+)?)+)\]/g,(m,n,b)=>'('+b.split(/\s+or\s+/).map(p=>`v.${n}==='${p.slice(3,-1)}'`).join('||')+')')
  .replace(/(\w+)\s*=\s*'([^']*)'/g,(m,n,s)=>`v.${n}==='${s}'`).split(/('[^']*')/).map((t,i)=>i%2?t:t.replace(/\bor\b/g,'||').replace(/\band\b/g,'&&')).join('');   // keep 'and'/'or' inside quoted values
 try{return !!Function('v','return '+e)(v)}catch(x){return true}}
function accordion(title,body,extra='',closed=false){const a=H(`<section class="acc${closed?' closed':''}"><div class="acc-h">${chev}<h2>${esc(title)}</h2>${extra}</div><div class="acc-b"></div></section>`);
 $('.acc-b',a).append(body);$('.acc-h',a).addEventListener('click',e=>{if(!e.target.closest('button'))a.classList.toggle('closed')});return a}
function fieldEl(a,v,onchange){
 if(a.IsInvisible==='Y')return null;const lab=a.ComponentLabel+(a.IsRequired==='Y'?' *':'');
 if(a.ComponentType==='Subheading')return H(`<h3 class="sub" data-cond="${esc(a.Custom1)}">${esc(lab)}</h3>`);
 if(a.ComponentType==='outputText'||a.ComponentType==='OutputText'){const o=H(`<div class="out" data-cond="${esc(a.Custom1)}"><span>${esc(lab)}</span><span>${esc(a.DefaultValue)}</span></div>`);o._a=a;return o}
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
// ---- policy: single container (no +, no State field; states live in States) ----
const pol={},policyAttrs=M.policy.AttributeDetailList,stateAttr=policyAttrs[0],polFields=policyAttrs.slice(1);
const polBody=H('<div></div>'),polHost=H('<div></div>');
const stateAcc=accordion('Policy',polBody);
let rest=null,after=null,stAcc=null;
function openPolicy(){if(polHost.firstChild)return;polBody.append(polHost);polHost.addEventListener('input',()=>showPremium());
 rest=form(polFields,pol);polHost.append(rest);
 const b=H('<div class="save"><button type="button" class="btn">Save</button></div>');polHost.append(b);
 $('button',b).onclick=()=>{if(!validate(polHost)){toast('Please complete the required fields',1);return}
  const pe=ruleErr(M.rules.policy,pol,polHost);showRules(polHost,pe);if(pe.length){toast(pe[0],1);return}
  toast('Policy Saved Successfully');state.policySaved=true;showAfter();sync();
  if(!stAcc){stAcc=accordion(pol.PolicyCoverageForm,polHost,'',true);polBody.append(stAcc)}else $('h2',stAcc).textContent=pol.PolicyCoverageForm;
  stAcc.classList.add('closed')}}
// ---- helpers ----
function table(cols,onadd,title,big){const t=H(`<div class="tbl"><table><thead><tr><th></th>${cols.map(c=>`<th>${esc(c)}</th>`).join('')}<th>Action</th></tr></thead><tbody></tbody></table></div>`);
 const none=()=>{if(!$('tr',$('tbody',t)))$('tbody',t).append(H(`<tr class="nr"><td class="none" colspan="${cols.length+2}">No Records To Display.</td></tr>`))};none();t._none=none;return t}
function section(title,onadd){const h=H(`<h3 class="sec">${esc(title)}<button type="button" class="plus grey" aria-label="Add">${plus}</button></h3>`);$('.plus',h).onclick=onadd;return h}
// ---- Participating States (proposal, not in FRC): repeatable; each state owns its underlying insurance ----
const SROWS=[],stName=c=>(stateAttr.SubApplicationAttributeValueList.find(o=>o.Value===c)||{}).DisplayValue||c,allStates=()=>SROWS.filter(r=>r.acc).map(r=>r.code);
const stBody=H('<div></div>'),statesAcc=accordion('States',stBody,`<button type="button" class="plus" aria-label="Add State" title="Add State">${plus}</button>`);
const rowLbl=r=>`${r.code} - ${stName(r.code)}${SROWS.filter(x=>x.acc).indexOf(r)===0?' (Primary State)':''}`;
const relabelStates=()=>SROWS.forEach(r=>{if(r.acc)$('h2',r.acc).textContent=rowLbl(r)});
function dropRow(r){SROWS.splice(SROWS.indexOf(r),1);(r.acc||r.host).remove();relabelStates();sync()}
function addStateRow(code){const row={code:code||'',groups:{},acc:null},host=H('<div></div>');row.host=host;
 const tmp={State:code||''},attr={...stateAttr,ComponentLabel:'State',SubApplicationAttributeValueList:stateAttr.SubApplicationAttributeValueList.filter(o=>!o.Value||!allStates().includes(o.Value))};
 function make(){row.code=tmp.State;row.acc=accordion(rowLbl(row),H('<div></div>'),`<button type="button" class="plus grey" aria-label="Remove State" title="Remove this state">&#10005;</button>`);
  const ui=H('<div></div>');ui.append(...M.groupNames.map(g=>underlying(g,row)));
  $('.acc-b',row.acc).append(accordion('Underlying Insurance Information',ui,'',true));
  $('.acc-h .plus',row.acc).onclick=e=>{e.stopPropagation();dropRow(row)};
  host.replaceWith(row.acc);relabelStates();sync()}
 SROWS.push(row);stBody.append(host);
 if(code){make();return row}
 const sf=fieldEl(attr,tmp);host.append(sf);
 const b=H('<div class="save" style="gap:10px"><button type="button" class="btn cancel">Cancel</button><button type="button" class="btn ok">Add State</button></div>');host.append(b);
 $('.cancel',b).onclick=()=>dropRow(row);
 $('.ok',b).onclick=()=>{if(!tmp.State){sf.classList.add('err');$('.msg',sf).textContent=stateAttr.RequiredMessage||'State is required';return}make();toast('State added')};
 return row}
$('.plus',statesAcc).onclick=e=>{e.stopPropagation();
 if(!state.policySaved){toast('Save the policy first',1);return}
 if(SROWS.some(r=>!r.acc)){toast('Save the open state first',1);return}
 statesAcc.classList.remove('closed');addStateRow('')};
function riskRows(){const R=[...document.querySelectorAll('#after tr[data-saved]')],ex=pol.PolicyCoverageForm==='Commercial Excess Liability Coverage Form';
 return SROWS.filter(r=>r.acc).map((r,i)=>({state:r.code,role:i?'Additional':'Primary',form:pol.PolicyCoverageForm||'',limit:(ex?pol.ExcessLiabilityLimit:pol.Limit)||'',
  sir:(ex?pol.ExcessLiabilitySelfInsuredRetention:pol.SelfInsuredRetention)||'',underlying:R.filter(t=>t._code===r.code).length+' saved'}))}
// ---- underlying rows (per state) ----
function underlying(g,row){const s=sub(g),d=sub(g+'Detail'),max=s.mAction.addRow.maxRows,cols=s.AttributeDetailList.map(a=>a.ComponentLabel),host=H('<div></div>');
 const t=table(cols);
 host.append(section(s.Description,()=>addRow()),t);
 function addRow(){$('.nr',t)?.remove();const v={},body=$('tbody',t),
   tr=H(`<tr data-row="1"><td><button type="button" class="ex" aria-label="Expand">${chev}</button></td>${cols.map(()=>'<td></td>').join('')}<td><button type="button" class="more" aria-label="Actions">&#8942;</button></td></tr>`),
   dr=H(`<tr><td class="exp" colspan="${cols.length+2}"></td></tr>`),f=form(d.AttributeDetailList,v);
  tr._v=v;tr._g=s.Description;tr._code=row.code;
  $('.exp',dr).append(f,H('<div class="save"><button type="button" class="btn">Save</button></div>'));
  $('.btn',dr).onclick=()=>{if(!validate(f)){toast('Please complete the required fields',1);return}
   const ge=ruleErr(M.rules.groups[s.Description]||[],v,f);showRules($('.exp',dr),ge);if(ge.length){toast(ge[0],1);return}
   [...tr.children].slice(1,-1).forEach((td,i)=>td.textContent=v[s.AttributeDetailList[i].AttributeName]||'');
   dr.classList.add('hide');$('.ex',tr).classList.remove('open');tr.dataset.saved=1;toast('Saved Successfully');sync()};
  $('.ex',tr).onclick=e=>{dr.classList.toggle('hide');e.currentTarget.classList.toggle('open',!dr.classList.contains('hide'))};
  $('.more',tr).onclick=e=>{e.stopPropagation();document.querySelectorAll('.menu').forEach(m=>m.remove());
   const m=H('<div class="menu"><button type="button">Delete</button></div>');e.currentTarget.parentNode.append(m);
   $('button',m).onclick=()=>{tr.remove();dr.remove();t._none();$('.plus',host).classList.remove('hide');sync()}};
  body.append(tr,dr);if(body.querySelectorAll('tr[data-row]').length>=max)$('.plus',host).classList.add('hide');
  $('.ex',tr).classList.add('open');return{tr,dr,f}}
 host._add=addRow;row.groups[s.Description]=host;return host}
document.addEventListener('click',()=>document.querySelectorAll('.menu').forEach(m=>m.remove()));
function showAfter(){if(after)return;after=H('<div></div>');
 const ac=H('<div></div>');ac.append(section('Additional Coverages',()=>toast('Additional coverage dialog is out of scope for this prototype')),table(['Coverage']));
 after.append(ac);$('#after').prepend(after)}
// ---- nav ----
const next=$('#next');
function sync(){next.disabled=!(state.policySaved&&document.querySelector('#after tr[data-saved]'));showPremium()}
// ---- rating: reproduces the TC 'Calculations' sheet (underlying premium x policy type factor; factor is 1 in the TC) ----
const FACTOR=1,num=x=>parseFloat(String(x||'').replace(/[^0-9.\-]/g,''))||0,money=n=>'$ '+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const HNO='UnderlyingHiredAndNonOwnedAutoPremium',MANUAL='CommercialUmbrellaExcessLiabilityCoverage.ManualPremium';
function groupsFor(rows){const groups=[];
 M.groupNames.forEach(g=>{const s=sub(g),d=sub(g+'Detail'),lines=[];
  rows.filter(r=>r._g===s.Description).forEach(r=>d.AttributeDetailList.forEach(a=>{
   if(a.AttributeDataType!=='Decimal'||!/Premium/.test(a.ComponentLabel))return;const b=num(r._v[a.AttributeName]);
   if(b)lines.push({label:a.AttributeName===HNO?'Hired And Non Owned Auto':a.ComponentLabel.replace(/ - Liability Premium| Premium$/,'').replace(/^Underlying Liability$/,'Liability'),base:b,factor:FACTOR,amt:b*FACTOR})}));
  if(lines.length)groups.push({name:s.Description,lines,total:lines.reduce((t,l)=>t+l.amt,0)})});return groups}
function rate(){const forms=window.EXTRA_FORMS||[],saved=[...document.querySelectorAll('#after tr[data-saved]')],f=pol.PolicyCoverageForm||'',umb=/Umbrella/.test(f),exc=/Excess/.test(f);
 const sts=SROWS.filter(r=>r.acc).map(r=>r.code);if(!sts.length)sts.push('');
 const blocks=sts.map((c,i)=>{const groups=groupsFor(saved.filter(t=>t._code===c));return{state:c,groups,umb,exc:exc&&i===0,first:umb?groups.reduce((t,g)=>t+g.total,0):0,excess:(exc&&i===0)?num(pol[MANUAL]):0}});
 const first=blocks.reduce((t,b)=>t+b.first,0),excess=blocks.reduce((t,b)=>t+b.excess,0),fsum=forms.reduce((t,x)=>t+x.premium,0);
 return{blocks,groups:blocks.flatMap(b=>b.groups),first,excess,forms,formsTotal:fsum,term:first+excess+fsum,umb,exc}}
function showPremium(){if(!rest)return;const r=rate(),set=(n,v)=>polHost.querySelectorAll('.out').forEach(o=>{if(o._a&&o._a.AttributeName===n)o.lastChild.textContent=v});
 set('CommercialUmbrella1stMillionCoverage.PolicyTermPremium',money(r.first));
 ['2nd','3rd','4th','5th'].forEach(m=>set(`CommercialUmbrella${m}MillionCoverage.PolicyTermPremium`,money(0)));
 set('CommercialUmbrellaExcessLiabilityCoverage.PolicyTermPremium',money(r.excess))}
$('#state').append(stateAcc);$('#after').append(statesAcc);openPolicy();sync();
// ---- restore: Program Selection -> Previous replays the saved policy, states and underlying rows through the same UI ----
function fill(root,v){root.querySelectorAll('.fld').forEach(f=>{if(!f._a)return;const k=f._a.AttributeName;if(v[k]===undefined)return;
 const c=$('select,input',f);c.value=v[k];c.dispatchEvent(new Event('input'))})}
function restore(){window.QUIET=true;try{restore0()}finally{window.QUIET=false}}
function restore0(){let s=null;try{s=JSON.parse(sessionStorage.getItem('cuRiskState')||'null')}catch(e){}
 if(!s||!sessionStorage.getItem('cuRestore'))return;sessionStorage.removeItem('cuRestore');window.EXTRA_FORMS=s.forms||[];
 openPolicy();fill(polHost,s.pol);$('.save .btn',polHost).click();
 (s.states||[]).forEach(st=>{const row=addStateRow(st.code);st.rows.forEach(r=>{const x=row.groups[r.g]._add();fill(x.f,r.v);$('.btn',x.dr).click()})})}
restore();
"""


def screen(meta: dict, expand: dict, logo: str) -> str:
    sh = shell
    note = meta["page"]["ApplicationDetail"]["SubApplicationDetailList"][0]["AttributeDetailList"][0]["ComponentLabel"]
    body = (f'{sh.steps()}<div class="childtab"><svg viewBox="0 0 24 24" fill="currentColor">'
            f'<path d="{sh.ICON["more"]}"/></svg><span>{TAB}</span></div>{sh.details(expand)}'
            '<form class="card" onsubmit="return false"><div id="state"></div><div id="after"></div>'
            f'<div class="note">{note} *</div><div class="lobnav" style="margin:0"><button class="btn" type="button">Previous</button>'
            '<button class="btn" type="button" id="next" disabled>Next</button></div></form>')
    foot = ('<footer class="footer"><span><a href="https://solartis.com" target="_blank" rel="noopener noreferrer">Solartis</a> &copy; 2026</span>'
            '<span>Powered by <a href="https://solartis.com" target="_blank" rel="noopener noreferrer">Solartis</a></span></footer>')
    payload = json.dumps(meta, separators=(",", ":")).replace("</", r"<\/")
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Risk/Coverage - Commercial Umbrella</title>'
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
            "rules": json.loads((d / "cu_validation_rules.json").read_text("utf-8"))}


if __name__ == "__main__":
    d, exp, logo, out = (Path(a) for a in sys.argv[1:5])
    uri = "data:image/png;base64," + base64.b64encode(logo.read_bytes()).decode("ascii")
    out.write_text(screen(load(d), json.loads(exp.read_text("utf-8")), uri), encoding="utf-8")
    print("wrote", out)
