"""One-off: 'States Covered' tick-list -> 'State' dropdown limited to the policy's states (default = the only state; 'All States' when several)."""
import re

p = "build_risk_screen.py"
s = open(p, encoding="utf-8").read()
m = re.search(r"function tagWidget\(init\)\{.*?\n render\(\);return\{[^\n]*\n", s, re.S)
assert m, "tagWidget not found"
NEW = r"""function tagWidget(init){const el=H('<div class="fld tags"><label>State * <i class="prop">(proposal, not in FRC)</i></label><select></select><div class="msg"></div></div>'),sel=$('select',el);
 const render=()=>{const cur=sel.value,all=allStates();
  sel.innerHTML=(all.length>1?'<option value="">Select</option>':'')+all.map(c=>`<option value="${c}">${esc(c)} - ${esc(stName(c))}</option>`).join('')+(all.length>1?'<option value="ALL">All States (multistate underlying policy)</option>':'');
  sel.value=all.length===1?all[0]:([...sel.options].some(o=>o.value===cur)?cur:'')};
 sel.onchange=()=>{el.classList.remove('err');$('.msg',el).textContent=''};
 render();if(init)sel.value=init.length>1?'ALL':init[0]||'';
 return{el,render,get:()=>sel.value==='ALL'?allStates():sel.value?[sel.value]:[],set:a=>{sel.value=a.length>1?'ALL':(a[0]||'')},fail:()=>{el.classList.add('err');$('.msg',el).textContent='State is required'}}}
"""
s = s.replace(m.group(0), NEW, 1)
open(p, "w", encoding="utf-8").write(s)
print("patched")
