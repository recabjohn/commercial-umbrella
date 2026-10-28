"""v3 (commercialumbrella3): the + on POLICY adds a full policy block for the new state, started as a copy of the primary policy terms.
Rating runs per block: an underlying row tagged to one state is rated on that state's block; 'All States' rows are rated on the primary
(assumption - how the Solartis ERC splits them is not in the files). Forms premiums are added once."""
import re

p = "build_risk_screen.py"
s = open(p, encoding="utf-8").read()


def sub1(pattern: str, new: str) -> None:
    global s
    m = re.search(pattern, s, re.S)
    assert m, pattern[:60]
    s = s[:m.start()] + new + s[m.end():]


def rep(a: str, b: str) -> None:
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


rep("const rowLbl=c=>`${c} - ${pol.PolicyCoverageForm||''}`;", "const rowLbl=r=>`${r.code} - ${(r.pol&&r.pol.PolicyCoverageForm)||''}`;")
rep("$('h2',r.acc).textContent=rowLbl(r.code)})}", "$('h2',r.acc).textContent=rowLbl(r)})}")

STATE_ROW = r"""function stateRow(code,saved){const host=H('<div></div>'),tmp={},row={code:code||'',host,acc:null,pol:tmp,rest:null};
 if(saved)Object.assign(tmp,saved);else Object.keys(pol).forEach(k=>{if(!/Premium|^State$|^SolartisIsPrimaryState$/.test(k))tmp[k]=pol[k]});   // a new state starts as a copy of the primary policy terms
 tmp.State=code||'';tmp.SolartisIsPrimaryState='No';
 const attr={...stateAttr,ComponentLabel:'State',SubApplicationAttributeValueList:stateAttr.SubApplicationAttributeValueList.filter(o=>!o.Value||o.Value===tmp.State||!allStates().includes(o.Value))};
 const sf=fieldEl(attr,tmp,()=>{if(tmp.State&&!row.rest)showRest()});host.append(sf);
 let b=null;
 function showRest(){row.rest=form(policyAttrs.slice(1),tmp);host.append(row.rest);
  b=H('<div class="save" style="gap:10px"><button type="button" class="btn cancel">Cancel</button><button type="button" class="btn ok">Save</button></div>');host.append(b);
  $('.ok',b).onclick=()=>{if(save())toast('State saved successfully')};$('.cancel',b).onclick=()=>dropRow(row);showPremium()}
 host.addEventListener('input',()=>showPremium());
 function save(){if(!tmp.State){sf.classList.add('err');$('.msg',sf).textContent=stateAttr.RequiredMessage||'State is required';return false}
  if(!validate(host)){toast('Please complete the required fields',1);return false}
  const pe=ruleErr(M.rules.policy,tmp,host);showRules(host,pe);if(pe.length){toast(pe[0],1);return false}
  if(row.code){const i=STATES.indexOf(row.code);if(i>=0)STATES.splice(i,1)}
  STATES.push(tmp.State);row.code=tmp.State;
  if(!row.acc){row.acc=accordion(rowLbl(row),host,`<button type="button" class="plus grey" aria-label="Remove State" title="Remove this state">&#10005;</button>`,true);polBody.append(row.acc);
   $('.acc-h .plus',row.acc).onclick=e=>{e.stopPropagation();dropRow(row)};$('.cancel',b).classList.add('hide')}
  else $('h2',row.acc).textContent=rowLbl(row);
  row.acc.classList.add('closed');retag();sync();return true}
 ST_ROWS.push(row);polBody.append(host);
 if(saved){showRest();save()}
 return row}
"""
sub1(r"function stateRow\(code\)\{.*? return row\}\n", STATE_ROW)
sub1(r"function addState\(c\)\{[^\n]*\n", "")
sub1(r"function riskRows\(\)\{.*?\}\)\)\}\n", r"""function riskRows(){const R=[...document.querySelectorAll('#after tr[data-saved]')],polOf=c=>c===pol.State?pol:((ST_ROWS.find(r=>r.code===c)||{}).pol||pol);
 return allStates().map((c,i)=>{const p=polOf(c),ex=p.PolicyCoverageForm==='Commercial Excess Liability Coverage Form';
  return{state:c,role:i?'Additional':'Primary',form:p.PolicyCoverageForm||'',limit:(ex?p.ExcessLiabilityLimit:p.Limit)||'',
   sir:(ex?p.ExcessLiabilitySelfInsuredRetention:p.SelfInsuredRetention)||'',underlying:R.filter(r=>(r._v.States||'').split(',').includes(c)).length+' saved'}})}
""")
RATE = r"""const MANUAL='CommercialUmbrellaExcessLiabilityCoverage.ManualPremium';
function groupsFor(rows){const groups=[];
 M.groupNames.forEach(g=>{const s=sub(g),d=sub(g+'Detail'),lines=[];
  rows.filter(r=>r._g===s.Description).forEach(r=>d.AttributeDetailList.forEach(a=>{
   if(a.AttributeDataType!=='Decimal'||!/Premium/.test(a.ComponentLabel))return;const b=num(r._v[a.AttributeName]);
   if(b)lines.push({label:a.AttributeName===HNO?'Hired And Non Owned Auto':a.ComponentLabel.replace(/ - Liability Premium| Premium$/,'').replace(/^Underlying Liability$/,'Liability'),base:b,factor:FACTOR,amt:b*FACTOR})}));
  if(lines.length)groups.push({name:s.Description,lines,total:lines.reduce((t,l)=>t+l.amt,0)})});return groups}
const owner=tr=>{const st=(tr._v.States||'').split(',').filter(Boolean);return st.length===1?st[0]:pol.State};   // 'All States' rows are rated on the primary state (assumption)
function rate(){const forms=window.EXTRA_FORMS||[],saved=[...document.querySelectorAll('#after tr[data-saved]')];
 const blocks=[{state:pol.State,p:pol,host:polHost},...ST_ROWS.filter(r=>r.acc).map(r=>({state:r.code,p:r.pol,host:r.host}))];
 blocks.forEach(b=>{const f=b.p.PolicyCoverageForm||'';b.umb=/Umbrella/.test(f);b.exc=/Excess/.test(f);b.groups=groupsFor(saved.filter(r=>owner(r)===b.state));
  b.first=b.umb?b.groups.reduce((t,g)=>t+g.total,0):0;b.excess=b.exc?num(b.p[MANUAL]):0});
 const first=blocks.reduce((t,b)=>t+b.first,0),excess=blocks.reduce((t,b)=>t+b.excess,0),fsum=forms.reduce((t,f)=>t+f.premium,0);
 return{blocks,groups:blocks.flatMap(b=>b.groups),first,excess,forms,formsTotal:fsum,term:first+excess+fsum,umb:blocks.some(b=>b.umb),exc:blocks.some(b=>b.exc)}}
function showPremium(){if(!rest)return;rate().blocks.forEach(b=>{const set=(n,v)=>b.host.querySelectorAll('.out').forEach(o=>{if(o._a&&o._a.AttributeName===n)o.lastChild.textContent=v});
 set('CommercialUmbrella1stMillionCoverage.PolicyTermPremium',money(b.first));
 ['2nd','3rd','4th','5th'].forEach(m=>set(`CommercialUmbrella${m}MillionCoverage.PolicyTermPremium`,money(0)));
 set('CommercialUmbrellaExcessLiabilityCoverage.PolicyTermPremium',money(b.excess))})}
"""
sub1(r"function rate\(\)\{.*?(?=\$\('#state'\)\.append\(stateAcc\))", RATE)
rep("(s.states||[]).forEach(addState)", "(s.states||[]).forEach(x=>stateRow(x.code,x.pol))")
assert "addState" not in s
open(p, "w", encoding="utf-8").write(s)
print("risk patched")

# program page: worksheet per state block
q = "../program-page/build_program_page.py"
t = open(q, encoding="utf-8").read()
WS = r"""function worksheet(){const r=RT,t=(h,rows)=>`<table><thead><tr>${h.map((x,i)=>`<th class="${i?'r':''}">${x}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table>`;
 const blk=b=>{const g=b.groups.map(x=>`<h3>${esc(x.name)}</h3>`+t(['Premium Type','Underlying Premium','Policy Type Factor','Premium'],
   x.lines.map(l=>`<tr><td>${esc(l.label)}</td><td class="r">${mny(l.base)}</td><td class="r">${l.factor}</td><td class="r">${mny(l.amt)}</td></tr>`).join('')+`<tr class="t"><td colspan="3">Premium ${esc(x.name)}</td><td class="r">${mny(x.total)}</td></tr>`)).join('');
  const first=t(['1st Million Premium','','','Premium'],b.groups.map(x=>`<tr><td colspan="3">${esc(x.name)}</td><td class="r">${mny(x.total)}</td></tr>`).join('')+`<tr class="t"><td colspan="3">Premium:</td><td class="r">${mny(b.first)}</td></tr>`);
  return(b.umb?g+'<h3>1st Million Premium</h3>'+first:'')+(b.exc?'<h3>Excess Liability Coverage</h3>'+t(['Manual Premium','','','Premium'],`<tr><td colspan="3">Manual Premium</td><td class="r">${mny(b.excess)}</td></tr>`):'')};
 const fm=r.forms.map(f=>`<tr><td colspan="3">${esc(f.name)}</td><td class="r">${mny(f.premium)}</td></tr>`).join(''),multi=r.blocks.length>1;
 return `<h2>Rating Worksheet <button class="btn cl" type="button">Close</button></h2><p class="nt">Reproduces the Test Case "Calculations" sheet: underlying liability premium × policy type factor. The factor is 1 in the TC; the real factor comes from rate tables that are not in the TC. 2nd–5th million premium is $0.00 in the TC (1,000,000 limit).${multi?' Each state is rated on its own policy block; underlying rows set to All States are rated on the primary state (assumption, not in the files).':''}</p>`
  +(multi?r.blocks.map(b=>`<h2 style="font-size:20px;margin-top:22px">State ${esc(b.state)}</h2>`+blk(b)).join(''):blk(r.blocks[0]))
  +(fm?'<h3>Policy Level Forms</h3>'+t(['Form','','','Premium'],fm):'')+`<h3>Policy Term Premium: ${mny(r.term)}</h3>`}
"""
m = re.search(r"function worksheet\(\)\{.*?(?=function showWs\()", t, re.S)
assert m, "worksheet not found"
t = t[:m.start()] + WS + t[m.end():]
open(q, "w", encoding="utf-8").write(t)
print("program patched")
