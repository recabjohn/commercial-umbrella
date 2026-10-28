// ---- policy: multi-state (one Policy card per state; first = primary) ----
const policyAttrs=M.policy.AttributeDetailList,stateAttr=policyAttrs[0],cards=[];
const polBody=H('<div id="states"></div>');
const stateAcc=accordion('Policy',polBody,`<button type="button" class="plus" aria-label="Add Policy">${plus}</button>`);
const stateName=c=>(stateAttr.SubApplicationAttributeValueList.find(o=>o.Value===c)||{}).DisplayValue||c;
$('.plus',stateAcc).onclick=()=>{if(cards.some(c=>!c.pol.State)){toast('Select a state for the open Policy first',1);return}addCard();stateAcc.classList.remove('closed')};
const rowLbl=(c,i)=>`${c.pol.State} - ${c.pol.PolicyCoverageForm}${i===0?' (Primary State)':''}`;
function relabel(){cards.forEach((c,i)=>{c.pol.SolartisIsPrimaryState=i===0?'Yes':'No';if(c.stRow)$('h2',c.stRow).textContent=rowLbl(c,i);
 $('h2',c.acc).textContent=c.pol.State?`${c.pol.State}-${stateName(c.pol.State)}${i===0?' (Primary State)':''}`:'New Policy'})}
function addCard(){const c={pol:{},saved:false,rest:null,after:null};
 c.host=H('<div></div>');c.body=H('<div></div>');c.body.append(c.host);
 c.acc=accordion('New Policy',c.body,`<button type="button" class="plus grey" aria-label="Remove Policy" title="Remove this state">&#10005;</button>`);
 $('.acc-h .plus',c.acc).onclick=e=>{e.stopPropagation();if(!confirm('Remove this state and everything under it?'))return;
  cards.splice(cards.indexOf(c),1);c.acc.remove();relabel();summary();sync()};
 c.sf=fieldEl(stateAttr,c.pol,()=>onState(c));c.host.append(c.sf);
 c.host.addEventListener('input',()=>summary());
 cards.push(c);polBody.append(c.acc);relabel();return c}
function onState(c){const s=c.pol.State;if(!s){relabel();summary();return}
 if(cards.some(o=>o!==c&&o.pol.State===s)){toast('Selected State already exist',1);$('select',c.sf).value='';c.pol.State='';relabel();return}
 relabel();if(!c.rest)showRest(c);summary()}
function showRest(c){c.rest=form(policyAttrs.slice(1),c.pol);c.host.append(c.rest);
 const b=H('<div class="save"><button type="button" class="btn">Save</button></div>');c.host.append(b);
 $('button',b).onclick=()=>{if(!validate(c.host)){toast('Please complete the required fields',1);return}
  const pe=ruleErr(M.rules.policy,c.pol,c.host);showRules(c.host,pe);if(pe.length){toast(pe[0],1);return}
  toast('Policy Saved Successfully');c.saved=true;showAfter(c);
  if(!c.stRow){c.stRow=accordion('',c.host,'',true);c.body.prepend(c.stRow)}   // state row appears only after Save
  relabel();c.stRow.classList.add('closed');summary();sync()}}
// ---- per state: Additional Coverages + Underlying Insurance ----
function table(cols){const t=H(`<div class="tbl"><table><thead><tr><th></th>${cols.map(c=>`<th>${esc(c)}</th>`).join('')}<th>Action</th></tr></thead><tbody></tbody></table></div>`);
 const none=()=>{if(!$('tr',$('tbody',t)))$('tbody',t).append(H(`<tr class="nr"><td class="none" colspan="${cols.length+2}">No Records To Display.</td></tr>`))};none();t._none=none;return t}
function section(title,onadd){const h=H(`<h3 class="sec">${esc(title)}<button type="button" class="plus grey" aria-label="Add">${plus}</button></h3>`);$('.plus',h).onclick=onadd;return h}
function underlying(g,c){const s=sub(g),d=sub(g+'Detail'),max=s.mAction.addRow.maxRows,cols=s.AttributeDetailList.map(a=>a.ComponentLabel),host=H('<div></div>');
 const t=table(cols);
 host.append(section(s.Description,()=>addRow()),t);
 function addRow(){$('.nr',t)?.remove();const v={},body=$('tbody',t),
   tr=H(`<tr data-row="1"><td><button type="button" class="ex" aria-label="Expand">${chev}</button></td>${cols.map(()=>'<td></td>').join('')}<td><button type="button" class="more" aria-label="Actions">&#8942;</button></td></tr>`),
   dr=H(`<tr><td class="exp" colspan="${cols.length+2}"></td></tr>`),f=form(d.AttributeDetailList,v);tr._v=v;tr._g=s.Description;
  $('.exp',dr).append(f,H('<div class="save"><button type="button" class="btn">Save</button></div>'));
  $('.btn',dr).onclick=()=>{if(!validate(f)){toast('Please complete the required fields',1);return}
   const ge=ruleErr(M.rules.groups[s.Description]||[],v,f);showRules($('.exp',dr),ge);if(ge.length){toast(ge[0],1);return}
   [...tr.children].slice(1,-1).forEach((td,i)=>td.textContent=v[s.AttributeDetailList[i].AttributeName]||'');
   dr.classList.add('hide');$('.ex',tr).classList.remove('open');tr.dataset.saved=1;toast('Saved Successfully');summary();sync()};
  $('.ex',tr).onclick=e=>{dr.classList.toggle('hide');e.currentTarget.classList.toggle('open',!dr.classList.contains('hide'))};
  $('.more',tr).onclick=e=>{e.stopPropagation();document.querySelectorAll('.menu').forEach(m=>m.remove());
   const m=H('<div class="menu"><button type="button">Delete</button></div>');e.currentTarget.parentNode.append(m);
   $('button',m).onclick=()=>{tr.remove();dr.remove();t._none();$('.plus',host).classList.remove('hide');summary();sync()}};
  body.append(tr,dr);if(body.querySelectorAll('tr[data-row]').length>=max)$('.plus',host).classList.add('hide');
  $('.ex',tr).classList.add('open');return{tr,dr,f}}
 host._add=addRow;c.groups[s.Description]=host;return host}
document.addEventListener('click',()=>document.querySelectorAll('.menu').forEach(m=>m.remove()));
function showAfter(c){if(c.after)return;const ui=H('<div></div>');c.groups={};
 ui.append(...M.groupNames.map(g=>underlying(g,c)));
 c.after=H('<div></div>');
 const ac=H('<div></div>');ac.append(section('Additional Coverages',()=>toast('Additional coverage dialog is out of scope for this prototype')),table(['Coverage']));
 c.after.append(ac,accordion('Underlying Insurance Information',ui,'',true));c.body.append(c.after)}
// ---- multi-state summary + real-time checks (BA proposals from research, NOT in FRC; minimums are typical market practice, configurable) ----
const MIN=[['General Liability','UnderlyingEachOccurrenceLimit',1000000,'GL each occurrence'],['Commercial Auto','UnderlyingLiabilityLimit',1000000,'Auto liability'],['Employers Liability','UnderlyingBIByAccidentEachAccidentLimit',500000,'EL bodily injury by accident']],MONOPOLISTIC=['ND','OH','WA','WY'],REQ_GROUPS=['General Liability','Commercial Auto','Employers Liability'];
const num=x=>parseFloat(String(x||'').replace(/[^0-9.]/g,''))||0,money=n=>'$'+n.toLocaleString('en-US');
function checks(c){const rows=[...c.acc.querySelectorAll('tr[data-saved]')],w=[],have=new Set(rows.map(r=>r._g));
 MIN.forEach(([g,k,m,l])=>rows.filter(r=>r._g===g).forEach(r=>{const x=num(r._v[k]);if(x&&x<m)w.push(`${l} ${money(x)} is below the typical ${money(m)}; the insured absorbs the gap`)}));
 if(c.saved)REQ_GROUPS.filter(g=>!have.has(g)).forEach(g=>w.push(`No ${g} underlying scheduled`));
 rows.forEach(r=>{const e=r._v.UnderlyingEffectiveDate,x=r._v.UnderlyingExpirationDate;if(e&&x&&x<=e)w.push(`${r._g}: expiration is not after effective date`)});
 const ex=[...new Set(rows.map(r=>r._v.UnderlyingExpirationDate).filter(Boolean))];if(ex.length>1)w.push('Underlying expiration dates differ: '+ex.join(', '));
 if(MONOPOLISTIC.includes(c.pol.State))w.push(c.pol.State+' is a monopolistic workers comp state: schedule stop-gap Employers Liability');
 return w}
function summary(){const el=$('#summary'),rows=cards.filter(c=>c.pol.State);el.innerHTML='';if(!rows.length)return;
 const g=(c,k)=>c.pol[k]||'';
 const body=rows.map(c=>{const ex=g(c,'PolicyCoverageForm')==='Commercial Excess Liability',n=c.acc.querySelectorAll('tr[data-saved]').length,i=cards.indexOf(c),w=checks(c);
  return `<tr><td>${esc(c.pol.State+'-'+stateName(c.pol.State))}${i===0?' <b>(Primary)</b>':''}</td><td>${esc(g(c,'PolicyCoverageForm'))}</td><td>${esc(ex?g(c,'ExcessLiabilityLimit'):g(c,'Limit'))}</td><td>${esc(ex?g(c,'ExcessLiabilitySelfInsuredRetention'):g(c,'SelfInsuredRetention'))}</td><td>${n?n+' saved':'0'}</td><td>${c.saved?'Policy saved':'Policy open'}</td><td class="warn">${w.length?w.map(x=>'&#9888; '+esc(x)).join('<br>'):'&#10003; No issues'}</td></tr>`}).join('');
 el.append(H(`<div><h3 class="sec">Multi-State Summary</h3><div class="tbl"><table><thead><tr><th>State</th><th>Policy Coverage Form</th><th>Umbrella / Excess Limit</th><th>Self Insured Retention</th><th>Underlying Rows</th><th>Status</th><th>Real-time Checks</th></tr></thead><tbody>${body}</tbody></table></div></div>`))}
// ---- nav ----
const next=$('#next');
function sync(){next.disabled=!(cards.length&&cards.every(c=>c.saved)&&document.querySelector('#states tr[data-saved]'))}
$('#state').append(stateAcc);sync();
// ---- restore: Program Selection -> Previous replays every saved state and underlying row through the same UI ----
function fill(root,v){root.querySelectorAll('.fld').forEach(f=>{if(!f._a)return;const k=f._a.AttributeName;if(v[k]===undefined)return;
 const c=$('select,input',f);c.value=v[k];c.dispatchEvent(new Event('input'))})}
function restore(){let s=null;try{s=JSON.parse(sessionStorage.getItem('cuRiskState')||'null')}catch(e){}
 if(!s||!sessionStorage.getItem('cuRestore'))return;sessionStorage.removeItem('cuRestore');
 s.cards.forEach(sc=>{$('.plus',stateAcc).click();const c=cards[cards.length-1];fill(c.host,{State:sc.pol.State});fill(c.host,sc.pol);$('.save .btn',c.host).click();
  sc.rows.forEach(r=>{const x=c.groups[r.g]._add();fill(x.f,r.v);$('.btn',x.dr).click()})})}
restore();
