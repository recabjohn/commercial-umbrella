"""v4 (commercialumbrella4): Policy container (single instance, no +, no State field) with the FRC policy fields, then PARTICIPATING STATES
(repeatable, + here). Each state holds its own Underlying Insurance Information. Proposal structure from the Gemini sketch the user chose;
FRC field sets are unchanged. Premium is rated per state, policy-level terms (limit, SIR, excess manual premium) apply once."""
p = "build_risk_screen.py"
s = open(p, encoding="utf-8").read()
a = s.index("// ---- policy ----")
b = s.index("restore();\n", a) + len("restore();\n")

NEW = r"""// ---- policy: single container (no +, no State field; states live in Participating States) ----
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
const stBody=H('<div></div>'),statesAcc=accordion('Participating States',stBody,`<button type="button" class="plus" aria-label="Add State" title="Add State">${plus}</button>`);
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
function restore(){let s=null;try{s=JSON.parse(sessionStorage.getItem('cuRiskState')||'null')}catch(e){}
 if(!s||!sessionStorage.getItem('cuRestore'))return;sessionStorage.removeItem('cuRestore');window.EXTRA_FORMS=s.forms||[];
 openPolicy();fill(polHost,s.pol);$('.save .btn',polHost).click();
 (s.states||[]).forEach(st=>{const row=addStateRow(st.code);st.rows.forEach(r=>{const x=row.groups[r.g]._add();fill(x.f,r.v);$('.btn',x.dr).click()})})}
restore();
"""
s = s[:a] + NEW + s[b:]
open(p, "w", encoding="utf-8").write(s)

# program page: v4 worksheet note
q = "../program-page/build_program_page.py"
t = open(q, encoding="utf-8").read()
old = " Each state is rated on its own policy block; underlying rows set to All States are rated on the primary state (assumption, not in the files)."
assert old in t
t = t.replace(old, " Underlying rows are rated under the state they are scheduled in; the policy limit, SIR and excess manual premium apply once.")
open(q, "w", encoding="utf-8").write(t)

# site wiring: state payload
m = "../../deploy/make_site.py"
w = open(m, encoding="utf-8").read()
old = "states:ST_ROWS.filter(r=>r.acc).map(r=>({code:r.code,pol:r.pol})),rows:[...document.querySelectorAll('#after tr[data-saved]')].map(r=>({g:r._g,v:r._v}))}"
assert old in w
w = w.replace(old, "states:SROWS.filter(r=>r.acc).map(r=>({code:r.code,rows:[...document.querySelectorAll('#after tr[data-saved]')].filter(t=>t._code===r.code).map(t=>({g:t._g,v:t._v}))}))}")
open(m, "w", encoding="utf-8").write(w)
print("v4 patched")
