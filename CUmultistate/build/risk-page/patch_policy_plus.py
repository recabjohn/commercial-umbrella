"""One-off: states are added with the + on the POLICY header (state rows under Policy); remove the 'Additional States' section.
Extra state rows carry only the State: Policy Coverage Form, limits, SIR and terrorism answers stay singleton on the primary policy."""
import re

p = "build_risk_screen.py"
s = open(p, encoding="utf-8").read()


def rep(a: str, b: str) -> None:
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# Policy header gets the + (adds a state row)
rep("const stateAcc=accordion('Policy',polBody);",
    "const stateAcc=accordion('Policy',polBody,`<button type=\"button\" class=\"plus\" aria-label=\"Add State\" title=\"Add State\">${plus}</button>`);")
# primary re-save: drop a duplicate state row, relabel rows
rep("showAfter();{const i=STATES.indexOf(pol.State);if(i>=0)STATES.splice(i,1)}renderStates();sync();",
    "showAfter();{const r=ST_ROWS.find(x=>x.code===pol.State);if(r)dropRow(r)}relabelStates();retag();sync();")

# remove the Additional States table/picker, add state rows
a = s.index("const statesTbl=table(")
b = s.index("function riskRows()")
NEW = r"""const ST_ROWS=[];
const rowLbl=c=>`${c} - ${pol.PolicyCoverageForm||''}`;
function relabelStates(){ST_ROWS.forEach(r=>{if(r.acc)$('h2',r.acc).textContent=rowLbl(r.code)})}
function dropRow(r){const i=STATES.indexOf(r.code);if(i>=0)STATES.splice(i,1);ST_ROWS.splice(ST_ROWS.indexOf(r),1);(r.acc||r.host).remove();retag()}
function stateRow(code){const host=H('<div></div>'),tmp={State:code||''},row={code:code||'',host,acc:null};
 const attr={...stateAttr,ComponentLabel:'State',SubApplicationAttributeValueList:stateAttr.SubApplicationAttributeValueList.filter(o=>!o.Value||o.Value===tmp.State||!allStates().includes(o.Value))};
 const sf=fieldEl(attr,tmp);host.append(sf);
 const b=H('<div class="save" style="gap:10px"><button type="button" class="btn cancel">Cancel</button><button type="button" class="btn ok">Save</button></div>');host.append(b);
 const save=()=>{if(!tmp.State){sf.classList.add('err');$('.msg',sf).textContent=stateAttr.RequiredMessage||'State is required';return false}
  if(row.code){const i=STATES.indexOf(row.code);if(i>=0)STATES.splice(i,1)}
  STATES.push(tmp.State);row.code=tmp.State;
  if(!row.acc){row.acc=accordion(rowLbl(row.code),host,`<button type="button" class="plus grey" aria-label="Remove State" title="Remove this state">&#10005;</button>`,true);polBody.append(row.acc);
   $('.acc-h .plus',row.acc).onclick=e=>{e.stopPropagation();dropRow(row)};$('.cancel',b).classList.add('hide')}
  else $('h2',row.acc).textContent=rowLbl(row.code);
  row.acc.classList.add('closed');retag();return true};
 $('.ok',b).onclick=()=>{if(save())toast('State saved successfully')};
 $('.cancel',b).onclick=()=>dropRow(row);
 ST_ROWS.push(row);polBody.append(host);
 if(code){STATES.length&&0;save()}
 return row}
function addState(c){if(!c||allStates().includes(c))return false;stateRow(c);return true}
$('.plus',stateAcc).onclick=e=>{e.stopPropagation();
 if(!state.policySaved){toast('Save the policy first',1);return}
 if(ST_ROWS.some(r=>!r.acc)){toast('Save the open state first',1);return}
 stateAcc.classList.remove('closed');stateRow('')};
"""
s = s[:a] + NEW + s[b:]
# showAfter: no states section
rep(" const stSec=H('<div></div>');stSec.append(section('Additional States',()=>{fillPicker();picker.classList.toggle('hide')}),picker,statesTbl);\n", "")
rep(" after.append(stSec,ac,accordion('Underlying Insurance Information',ui,'',true));$('#after').append(after);renderStates()}",
    " after.append(ac,accordion('Underlying Insurance Information',ui,'',true));$('#after').append(after)}")
# stray no-op I left in stateRow
s = s.replace("if(code){STATES.length&&0;save()}", "if(code)save()")
# unused CSS
s = s.replace(".stpick{flex-direction:row;gap:10px;align-items:flex-end}.stpick select{min-width:260px}", "")
assert "renderStates" not in s and "picker" not in s and "statesTbl" not in s
open(p, "w", encoding="utf-8").write(s)
print("patched")
