"""One-off: derive the multistate v2 Risk screen from the main screen builder (copied here as build_risk_screen.py).
Design (proposal, not FRC): one Policy record, 'Additional States' list, underlying rows tagged with the states they cover,
multi-state summary with real-time checks. FRC field sets for Policy and the 9 underlying groups are unchanged."""
p = "build_risk_screen.py"
s = open(p, encoding="utf-8").read()


def rep(a: str, b: str) -> None:
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# 1 singleton Policy: no +, opens at load, State = Primary State
rep("const stateAcc=accordion('Policy',polBody,`<button type=\"button\" class=\"plus\" aria-label=\"Add Policy\">${plus}</button>`);",
    "stateAttr.ComponentLabel='Primary State';   // proposal: policy is one record; extra states live in the States section\nconst stateAcc=accordion('Policy',polBody);")
rep("$('.plus',stateAcc).onclick=openPolicy;\n", "")
rep("$('#state').append(stateAcc);sync();", "$('#state').append(stateAcc);openPolicy();sync();")

NEW = r"""// ---- States (proposal, not in FRC): one Policy, many states; underlying rows are tagged with the states they cover ----
const STATES=[],MONO=['ND','OH','WA','WY'];
const stName=c=>(stateAttr.SubApplicationAttributeValueList.find(o=>o.Value===c)||{}).DisplayValue||c,allStates=()=>[pol.State,...STATES].filter(Boolean);
const MIN=[['General Liability','UnderlyingEachOccurrenceLimit',1000000,'GL each occurrence'],['Commercial Auto','UnderlyingLiabilityLimit',1000000,'Auto liability'],['Employers Liability','UnderlyingBIByAccidentEachAccidentLimit',500000,'EL bodily injury by accident']];
function tagWidget(init){const el=H('<div class="fld tags"><label>States Covered * <i class="prop">(proposal, not in FRC)</i></label><div class="chips"></div><div class="msg"></div></div>');
 let sel=new Set(init||allStates());
 const render=()=>{sel=new Set([...sel].filter(c=>allStates().includes(c)));const ch=$('.chips',el);
  ch.innerHTML=allStates().map(c=>`<label><input type="checkbox" value="${c}"${sel.has(c)?' checked':''}> ${esc(c)}</label>`).join('');
  ch.querySelectorAll('input').forEach(i=>i.onchange=()=>{i.checked?sel.add(i.value):sel.delete(i.value);el.classList.remove('err');$('.msg',el).textContent=''})};
 render();return{el,render,get:()=>allStates().filter(c=>sel.has(c)),set:a=>{sel=new Set(a);render()},fail:()=>{el.classList.add('err');$('.msg',el).textContent='Select at least one state'}}}
function retag(){document.querySelectorAll('#after tr[data-row]').forEach(tr=>{const sc=tr._sc;if(!sc)return;sc.render();
 if(tr.dataset.saved){if(!sc.get().length)sc.set([pol.State]);tr._v.States=sc.get().join(',');const td=[...tr.children];td[td.length-2].textContent=tr._v.States}})}
const statesTbl=table(['State','Role']),picker=H('<div class="fld stpick hide"><select></select><button type="button" class="btn">Add State</button></div>');
function fillPicker(){$('select',picker).innerHTML='<option value="">Select State</option>'+stateAttr.SubApplicationAttributeValueList.filter(o=>o.Value&&!allStates().includes(o.Value)).map(o=>`<option value="${esc(o.Value)}">${esc(o.Value)} - ${esc(o.DisplayValue)}</option>`).join('')}
function renderStates(){const b=$('tbody',statesTbl);b.innerHTML='';
 allStates().forEach((c,i)=>{const tr=H(`<tr><td></td><td>${esc(c)} - ${esc(stName(c))}</td><td>${i?'Additional State':'Primary State'}</td><td>${i?'<button type="button" class="more" aria-label="Actions">&#8942;</button>':''}</td></tr>`);
  if(i)$('.more',tr).onclick=e=>{e.stopPropagation();document.querySelectorAll('.menu').forEach(m=>m.remove());const m=H('<div class="menu"><button type="button">Delete</button></div>');
   e.currentTarget.parentNode.append(m);$('button',m).onclick=()=>{STATES.splice(STATES.indexOf(c),1);renderStates()}};
  b.append(tr)});retag();fillPicker();summary()}
function addState(c){if(!c||allStates().includes(c))return false;STATES.push(c);renderStates();return true}
$('.btn',picker).onclick=()=>{const c=$('select',picker).value;if(!c){toast('Select a state',1);return}addState(c);toast('State added')};
function riskRows(){const R=[...document.querySelectorAll('#after tr[data-saved]')],ex=pol.PolicyCoverageForm==='Commercial Excess Liability Coverage Form';
 return allStates().map((c,i)=>({state:c,role:i?'Additional':'Primary',form:pol.PolicyCoverageForm||'',limit:(ex?pol.ExcessLiabilityLimit:pol.Limit)||'',
  sir:(ex?pol.ExcessLiabilitySelfInsuredRetention:pol.SelfInsuredRetention)||'',underlying:R.filter(r=>(r._v.States||'').split(',').includes(c)).length+' saved'}))}
function summary(){const el=$('#summary');if(!el)return;el.innerHTML='';if(!state.policySaved)return;
 const R=[...document.querySelectorAll('#after tr[data-saved]')],g=n=>R.filter(r=>r._g===n),w=[];
 if(!g('General Liability').length&&!g('BOP').length)w.push('No General Liability or BOP underlying scheduled');
 if(!g('Commercial Auto').length)w.push('No Commercial Auto underlying scheduled');
 if(!g('Employers Liability').length)w.push('No Employers Liability underlying scheduled');
 MIN.forEach(([n,k,m,l])=>g(n).forEach(r=>{const x=num(r._v[k]);if(x&&x<m)w.push(`${l} $${x.toLocaleString('en-US')} is below the typical $${m.toLocaleString('en-US')}; the insured absorbs the gap`)}));
 R.forEach(r=>{const e=r._v.UnderlyingEffectiveDate,x=r._v.UnderlyingExpirationDate;if(e&&x&&x<=e)w.push(`${r._g}: expiration is not after effective date`)});
 const ex=[...new Set(R.map(r=>r._v.UnderlyingExpirationDate).filter(Boolean))];if(ex.length>1)w.push('Underlying expiration dates differ: '+ex.join(', '));
 const cell=ws=>ws.length?ws.map(x=>'&#9888; '+esc(x)).join('<br>'):'&#10003; No issues',excess=/Excess/.test(pol.PolicyCoverageForm||''),umb=/Umbrella/.test(pol.PolicyCoverageForm||'');
 const lim=[umb?`Umbrella ${pol.Limit||''} / SIR ${pol.SelfInsuredRetention||''}`:'',excess?`Excess ${pol.ExcessLiabilityLimit||''} / SIR ${pol.ExcessLiabilitySelfInsuredRetention||''}`:''].filter(Boolean).join('<br>');
 const rows=allStates().map((c,i)=>{const t=R.filter(r=>(r._v.States||'').split(',').includes(c)),ws=[];
  if(!t.length)ws.push('No underlying insurance tagged to this state');
  if(MONO.includes(c)&&!t.some(r=>r._g==='Employers Liability'))ws.push(`${c} is a monopolistic workers comp state: schedule stop-gap Employers Liability`);
  return `<tr><td>${esc(c)} - ${esc(stName(c))}</td><td>${i?'Additional':'Primary'}</td><td>${t.length}</td><td class="warn">${cell(ws)}</td></tr>`}).join('');
 el.append(H(`<div><h3 class="sec">Multi-State Summary <i class="prop">(real-time checks are proposals, not FRC)</i></h3><div class="tbl"><table><thead><tr><th>Scope</th><th>Limits</th><th>Underlying Policies</th><th>Real-time Checks</th></tr></thead>
  <tbody><tr><td>Policy (all states)</td><td>${lim}</td><td>${R.length}</td><td class="warn">${cell(w)}</td></tr></tbody></table></div>
  <div class="tbl"><table><thead><tr><th>State</th><th>Role</th><th>Underlying Tagged</th><th>Real-time Checks</th></tr></thead><tbody>${rows}</tbody></table></div></div>`))}
"""
rep("const GROUPS={};\n", "const GROUPS={};\n" + NEW)

# 3 underlying: extra States column + tag widget
rep("cols=s.AttributeDetailList.map(a=>a.ComponentLabel),host=H('<div></div>');", "cols=[...s.AttributeDetailList.map(a=>a.ComponentLabel),'States'],host=H('<div></div>');")
rep("  tr._v=v;tr._g=s.Description;\n", "  tr._v=v;tr._g=s.Description;const sc=tagWidget();tr._sc=sc;f.prepend(sc.el);\n")
rep("  $('.btn',dr).onclick=()=>{if(!validate(f)){toast('Please complete the required fields',1);return}\n   const ge=",
    "  $('.btn',dr).onclick=()=>{if(!validate(f)){toast('Please complete the required fields',1);return}\n"
    "   const st=sc.get();if(!st.length){sc.fail();toast('Please complete the required fields',1);return}v.States=st.join(',');\n   const ge=")
rep("   [...tr.children].slice(1,-1).forEach((td,i)=>td.textContent=v[s.AttributeDetailList[i].AttributeName]||'');",
    "   const tds=[...tr.children].slice(1,-1);tds.forEach((td,i)=>td.textContent=i<tds.length-1?(v[s.AttributeDetailList[i].AttributeName]||''):v.States);")
rep("return{tr,dr,f}}", "return{tr,dr,f,sc}}")

# 4 showAfter: States section first; primary re-save
rep("after.append(ac,accordion('Underlying Insurance Information',ui,'',true));$('#after').append(after)}",
    "const stSec=H('<div></div>');stSec.append(section('Additional States',()=>{fillPicker();picker.classList.toggle('hide')}),picker,statesTbl);\n"
    " after.append(stSec,ac,accordion('Underlying Insurance Information',ui,'',true));$('#after').append(after);renderStates()}")
rep("toast('Policy Saved Successfully');state.policySaved=true;showAfter();sync();",
    "toast('Policy Saved Successfully');state.policySaved=true;showAfter();{const i=STATES.indexOf(pol.State);if(i>=0)STATES.splice(i,1)}renderStates();sync();")

# 5 summary on sync, body div, restore
rep("showPremium()}\n// ---- rating", "showPremium();summary()}\n// ---- rating")
rep("""'<form class="card" onsubmit="return false"><div id="state"></div><div id="after"></div>'""",
    """'<form class="card" onsubmit="return false"><div id="state"></div><div id="after"></div><div id="summary"></div>'""")
rep("$('.save .btn',polHost).click();\n s.rows.forEach(r=>{const x=GROUPS[r.g]._add();fill(x.f,r.v);$('.btn',x.dr).click()})}",
    "$('.save .btn',polHost).click();(s.states||[]).forEach(addState);\n"
    " s.rows.forEach(r=>{const x=GROUPS[r.g]._add();fill(x.f,r.v);x.sc.set((r.v.States||'').split(',').filter(Boolean));$('.btn',x.dr).click()})}")

# 6 CSS
rep(".hide{display:none!important}", """.hide{display:none!important}.warn{color:#8a5a00;font-size:13px}.prop{font-style:normal;color:#8a5a00;font-size:11px;font-weight:400}
.tags .chips{display:flex;flex-wrap:wrap;gap:6px 18px;padding:6px 6px}.tags .chips label{display:flex;gap:6px;align-items:center;font-size:14px;color:#222;margin:0}
.fld.tags.err .chips{outline:1px solid #f44336;border-radius:6px}.stpick{flex-direction:row;gap:10px;align-items:flex-end}.stpick select{min-width:260px}""")
open(p, "w", encoding="utf-8").write(s)
print("patched")
