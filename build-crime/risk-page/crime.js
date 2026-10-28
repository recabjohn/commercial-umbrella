// ---- Crime tab (FRC-CR-CW): Policy -> group (0..1) -> Detail. Appended to the Risk page script; reuses H,$,esc,chev,plus,toast,accordion,table,section.
document.head.append(H(`<style id="crime-radio-css">.fld.rfld{display:grid;grid-template-columns:33.33% 1fr;align-items:center;margin:14px 0 6px}.fld.rfld>label{font-size:16px;color:#333;margin:0 0 0 6px}.fld.rfld .rad{display:flex;height:auto;gap:0}.fld.rfld .rad label{flex:0 0 33.33%;display:flex;align-items:center;gap:10px;font-size:14px;color:#111;margin:0;cursor:pointer}.fld.rfld .rad input{padding:0;min-width:20px;flex:none;appearance:none;-webkit-appearance:none;width:20px;height:20px;border:2px solid #0d1e37;border-radius:50%;margin:0;display:grid;place-content:center;background:#fff;cursor:pointer}.fld.rfld .rad input::before{content:"";width:10px;height:10px;border-radius:50%;background:#0d1e37;transform:scale(0)}.fld.rfld .rad input:checked::before{transform:scale(1)}.fld.rfld .msg{grid-column:2}</style>`));
const CR=M.crime,DOM=CR.domains,cp={},cgroups={};
const cnorm=p=>p.replace(/\//g,'.');
function ccond(c,v){if(!c)return true;
 c=c.replace(/count\([^)]*\)\s*>\s*0/g,'(1=0)');          // 'a form schedule already has rows': form schedules are out of scope -> false
 if(!/^[\w\s.'"=!()+\-\/\[\]]+$/.test(c))throw new Error('unsupported condition: '+c);
 const lit=s=>s.replace(/^['"]|['"]$/g,''),val=p=>`String(v[${JSON.stringify(cnorm(p))}]??'')`,
  e=c.replace(/([\w.\/]+)\[([^\]]+)\]|([\w.\/]+)\s*(!?=)\s*('[^']*'|"[^"]*"|\d+)|\b(and|or)\b|([\w.\/]+)/g,(m,bp,bb,ep,eo,ev,op,bare)=>
   bp?`(${/!=/.test(bb)?'!':''}${JSON.stringify(bb.split(/\s+or\s+/).map(t=>lit(t.replace(/^[\w.]*\s*!?=\s*/,''))))}.includes(${val(bp)}))`
   :ep?`(${val(ep)}${eo==='='?'===':'!=='}${JSON.stringify(lit(ev))})`:op?(op==='and'?'&&':'||'):`(${val(bare)}==='Yes')`);
 return !!Function('v','return '+e)(v)}
function copts(f,v,fields){const d=DOM[f.dom];if(!d||d.range)return[];
 return d.items.filter(i=>!d.key||i.k===String(v[d.key]??'')).map(i=>({v:i.v,d:i.d}))}
function crange(f,v,fields){const d=DOM[f.dom];if(!d||!d.range)return null;
 const i=fields.indexOf(f);let inc=d.key;
 if(inc==='Included'){for(let j=i-1;j>=0;j--)if(/Included$/.test(fields[j].n)&&fields[j].dom==='YesNo'){inc=fields[j].n;break}}
 const r=d.items.find(x=>x.k===String(v[inc]??''));return r?{min:+r.min,max:+r.max}:null}
function cfield(f,v,fields,onchange){
 if(f.t==='Hidden'||f.t==='Button'){v[f.n]=f.def;return null}
 if(f.t==='Subheading')return H(`<h3 class="sub" data-f="${esc(f.n)}">${esc(f.l)}</h3>`);
 const id='c_'+Math.random().toString(36).slice(2,8),lab=esc(f.l)+(f.req&&!f.ro?' *':'');
 v[f.n]=v[f.n]??f.def;
 if(f.ro)return H(`<div class="out" data-f="${esc(f.n)}"><span>${lab}</span><span class="val">${esc(v[f.n])}</span></div>`);
 let ctl;
 if(f.t==='Select')ctl=`<select id="${id}"></select>`;
 else if(f.t==='Radio'||f.t==='RADIO_STACKED')ctl=`<div class="rad">${DOM[f.dom].items.map(i=>`<label><input type="radio" name="${id}" value="${esc(i.v)}"${v[f.n]===i.v?' checked':''}> ${esc(i.d)}</label>`).join('')}</div>`;
 else if(f.t==='Textarea')ctl=`<textarea id="${id}" rows="3"></textarea>`;
 else if(f.t==='Checkbox')ctl=`<input id="${id}" type="checkbox">`;
 else ctl=`<input id="${id}" type="${DOM[f.dom]?.range?'number':'text'}">`;
 const el=H(`<div class="fld${f.t==='Radio'||f.t==='RADIO_STACKED'?' rfld':''}" data-f="${esc(f.n)}" title="${esc(f.help)}"><label for="${id}">${lab}</label>${ctl}<div class="msg"></div></div>`);
 el._f=f;
 const set=()=>{v[f.n]=f.t==='Radio'||f.t==='RADIO_STACKED'?($('input:checked',el)?.value??''):f.t==='Checkbox'?($('input',el).checked?'Yes':'No'):$('select,input,textarea',el).value;
  el.classList.remove('err');$('.msg',el).textContent='';onchange()};
 el.addEventListener('input',set);el.addEventListener('change',set);
 const c=$('select,input[type=text],input[type=number],textarea',el);if(c&&f.t!=='Select')c.value=v[f.n];
 if(f.t==='Checkbox')$('input',el).checked=v[f.n]==='Yes';
 return el}
function crefresh(root,v,fields){
 root.querySelectorAll('[data-f]').forEach(e=>{const f=fields.find(x=>x.n===e.dataset.f);
  e.classList.toggle('hide',!ccond(f.cond,v));
  if(f.t==='Select'){const s=$('select',e),o=copts(f,v,fields),key=o.map(x=>x.v).join('\u0001');
   if(s._key!==key){const cur=v[f.n];s._key=key;s.innerHTML='<option value="">Select</option>'+o.map(x=>`<option value="${esc(x.v)}">${esc(x.d)}</option>`).join('');
    s.value=o.some(x=>x.v===cur)?cur:'';v[f.n]=s.value}}
  const r=crange(f,v,fields),inp=$('input[type=number]',e);
  if(inp&&r){inp.min=r.min;inp.max=r.max;if(+inp.value<r.min||+inp.value>r.max){inp.value=r.min;v[f.n]=inp.value}}
  if(f.ro&&$('.val',e))$('.val',e).textContent=v[f.n]??''})}
function cvalid(root,v,fields){let ok=true;
 root.querySelectorAll('.fld').forEach(e=>{if(e.classList.contains('hide')||!e._f)return;const f=e._f;let m='';const val=v[f.n]??'';
  if(f.req&&ccond(f.reqCond,v)&&val==='')m=`${f.l} is required.`;
  else if(val!==''){const r=crange(f,v,fields);if(r&&(isNaN(+val)||+val<r.min||+val>r.max))m=`${f.l} must be between ${r.min} and ${r.max}.`}
  if(m){ok=false;e.classList.add('err');$('.msg',e).textContent=m}});return ok}
function cform(fields,v){const w=H('<div class="cform"></div>'),r=()=>crefresh(w,v,fields);
 fields.forEach(f=>{const e=cfield(f,v,fields,r);e&&w.append(e)});r();return w}
// policy
const cpHost=H('<div></div>'),cpBody=H('<div></div>');cpBody.append(cpHost);
const cpAcc=accordion('Policy',cpBody,`<button type="button" class="plus" aria-label="Add Crime Policy">${plus}</button>`);
const crimeState={policySaved:false};let cAfter=null,cPolForm=null;
$('.plus',cpAcc).onclick=()=>{if(cPolForm)return;cPolForm=cform(CR.policy,cp);cpHost.append(cPolForm,H('<div class="save"><button type="button" class="btn">Save</button></div>'));
 $('.btn',cpHost).onclick=()=>{if(!cvalid(cPolForm,cp,CR.policy)){toast('Please complete the required fields',1);return}
  toast('Policy Saved Successfully');crimeState.policySaved=true;showGroups();sync()}};
// Additional Coverages = Policy Form Summary (AL TC): Mandatory forms listed, Optional forms added by the user (package: AL when State=AL, else CW)
const addl={chosen:new Set(),render:()=>{}};
function addlCoverages(){
 if(!document.getElementById('crime-modal-css'))document.head.append(H(`<style id="crime-modal-css">.mback{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:70;display:flex;align-items:center;justify-content:center}.mcard{background:#fff;border-radius:12px;width:min(1100px,92vw);padding:30px 30px 24px}.mcard h2{margin:0 0 50px;font-size:24px;font-weight:500;color:#222}.mcard .srch{position:relative}.mcard .srch input{width:100%;height:40px;border:1px solid #b9b9b9;border-radius:20px;padding:0 44px 0 16px;font:inherit;font-size:15px}.mcard .srch svg{position:absolute;right:12px;top:8px;width:24px;height:24px;color:#555}.mcard .mb{display:flex;justify-content:space-between;margin-top:44px}.mcard input::-webkit-calendar-picker-indicator{display:none!important}.mcard .msg{color:#f44336;font-size:12px;margin:4px 0 0 14px}</style>`));
 const t=table(['Coverage']),host=H('<div id="crime-addl"></div>'),pkg=()=>CR.forms[cp.State==='AL'?'AL':'CW'];
 const label=f=>`${f.number} - ${f.name}`,avail=()=>pkg().filter(f=>f.type==='Optional'&&!addl.chosen.has(f.number)&&ccond(f.cond,cp));
 addl.render=()=>{const tb=$('tbody',t);[...addl.chosen].forEach(n=>{const f=pkg().find(x=>x.number===n);if(!f||!ccond(f.cond,cp))addl.chosen.delete(n)});
  tb.innerHTML='';const rows=[...pkg().filter(f=>f.type==='Mandatory'),...pkg().filter(f=>addl.chosen.has(f.number))];
  rows.forEach(f=>{const tr=H(`<tr data-form="${esc(f.number)}"><td></td><td>${esc(label(f))} <b style="color:${f.type==='Mandatory'?'#c62828':'#444'}">(${f.type==='Mandatory'?'m':'o'})</b></td><td>${f.type==='Optional'?'<button type="button" class="more" aria-label="Remove">&#10005;</button>':''}</td></tr>`);
   $('.more',tr)&&($('.more',tr).onclick=()=>{addl.chosen.delete(f.number);addl.render()});tb.append(tr)});
  if(!rows.length)t._none()};
 function dialog(){const a=avail();if(!a.length){toast('No more forms available');return}
  const m=H(`<div class="mback"><div class="mcard" role="dialog" aria-label="Policy Additional Coverage"><h2>Policy Additional Coverage</h2><div class="srch"><input list="covlist" placeholder="Coverage *" aria-label="Coverage"><datalist id="covlist">${a.map(f=>`<option value="${esc(label(f))}">`).join('')}</datalist><svg viewBox="0 0 24 24"><path fill="currentColor" d="M15.5 14h-.79l-.28-.27A6.47 6.47 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14"/></svg></div><div class="msg"></div><div class="mb"><button type="button" class="btn" id="cov-save">Save Coverage</button><button type="button" class="btn" id="cov-cancel">Cancel</button></div></div></div>`);
  document.body.append(m);$('input',m).focus();$('#cov-cancel',m).onclick=()=>m.remove();
  $('#cov-save',m).onclick=()=>{const f=a.find(x=>label(x)===$('input',m).value.trim());if(!f){$('.msg',m).textContent='Coverage is required.';return}
   addl.chosen.add(f.number);m.remove();addl.render();toast('Saved Successfully')}}
 host.append(section('Additional Coverages',dialog),t);return host}
function groupVisible(g){const t=cp.PackagePolicy==='Yes'?cp.PackagePolicyType:cp.MonolinePolicyType;return g.showWhen.includes(t)}
function showGroups(){if(!cAfter){cAfter=H('<div></div>');$('#crime-after').append(cAfter);cAfter.append(addlCoverages())}
 addl.render();
 CR.groups.forEach(g=>{const st=cgroups[g.name]||(cgroups[g.name]={v:{},host:null});
  if(!groupVisible(g)){st.host?.remove();st.host=null;return}
  if(st.host)return;
  const cols=g.summary.map(f=>f.l),t=table(cols),body=H('<div></div>');body.append(t);
  const host=accordion(g.name,body,`<button type="button" class="plus grey" aria-label="Add ${esc(g.name)}">${plus}</button>`,true);
  $('.plus',host).onclick=()=>{addRow();host.classList.remove('closed')};
  const sumVal=f=>({TotNumPrem:cp.TotalNumPrem,NumRatableEmps:cp.NumRatableEmps1})[f.n]??st.v[f.n]??'';
  function addRow(){if($('tr[data-row]',t))return;$('.nr',t)?.remove();
   const tr=H(`<tr data-row="1"><td></td>${cols.map(()=>'<td></td>').join('')}<td><button type="button" class="ex" aria-label="Expand">${chev}</button></td></tr>`),
    dr=H(`<tr><td class="exp" colspan="${cols.length+2}"></td></tr>`),f=cform(g.detail,st.v);
   $('.exp',dr).append(f,H('<div class="save"><button type="button" class="btn">Save</button></div>'));
   $('.btn',dr).onclick=()=>{if(!cvalid(f,st.v,g.detail)){toast('Please complete the required fields',1);return}
    [...tr.children].slice(1,-1).forEach((td,i)=>td.textContent=sumVal(g.summary[i]));dr.classList.add('hide');tr.dataset.saved=1;toast('Saved Successfully');sync()};
   $('.ex',tr).onclick=()=>{dr.classList.toggle('hide');tr.classList.toggle('open')};$('tbody',t).append(tr,dr);$('.plus',host).classList.add('hide')}
  st.host=host;cAfter.append(...CR.groups.map(x=>cgroups[x.name]?.host).filter(Boolean))})}
$('#crime-policy').append(cpAcc);
