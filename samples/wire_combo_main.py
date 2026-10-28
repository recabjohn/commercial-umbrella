"""One-off (main site only): replace the native datalist with a dropdown (like the State select) that is also typable.
Carrier and Underlying Policy Number: click/focus opens a styled list for the selected LOB; typing filters it; any typed value is kept."""
import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "build/risk-page/build_risk_screen.py"
s = p.read_text("utf-8")

NEW = r"""function lookupize(f,g){const L=(M.lookup||{})[g]||[];if(!L.length)return;
 const by=n=>[...f.querySelectorAll('.fld')].find(x=>x._a&&x._a.AttributeName===n),car=by('NameID'),num=by('UnderlyingPolicyNumber');if(!car||!num)return;
 const ci=$('input',car),ni=$('input',num),norm=x=>x.trim().toLowerCase();
 function combo(inp,opts,pick){const w=H('<div class="combo"></div>'),list=H('<div class="combo-list hide"></div>'),ar=H(`<span class="ca">${chev}</span>`);
  inp.replaceWith(w);w.append(inp,ar,list);inp.setAttribute('autocomplete','off');
  const render=()=>{const all=opts(),q=norm(inp.value),exact=all.some(o=>norm(o.value)===q),m=q&&!exact?all.filter(o=>norm(o.value).includes(q)||norm(o.sub||'').includes(q)):all;
   list.innerHTML=m.length?m.map((o,i)=>`<div class="opt" data-i="${i}"><b>${esc(o.value)}</b>${o.sub?`<small>${esc(o.sub)}</small>`:''}</div>`).join(''):'<div class="opt none">No matches: your typed value will be kept</div>';
   list.querySelectorAll('.opt[data-i]').forEach(e=>e.onmousedown=ev=>{ev.preventDefault();pick(m[+e.dataset.i]);close()})};
  const open=()=>{render();list.classList.remove('hide')},close=()=>list.classList.add('hide');
  inp.addEventListener('focus',open);inp.addEventListener('click',open);inp.addEventListener('input',open);inp.addEventListener('blur',close);
  inp.addEventListener('keydown',e=>{if(e.key==='Escape')close();if(e.key==='ArrowDown')open()});
  ar.onmousedown=e=>{e.preventDefault();list.classList.contains('hide')?(inp.focus(),open()):close()}}
 combo(ci,()=>[...new Set(L.map(x=>x.carrier))].map(c=>({value:c})),o=>{ci.value=o.value;ci.dispatchEvent(new Event('input'))});
 combo(ni,()=>{const c=norm(ci.value),m=L.filter(x=>!c||norm(x.carrier)===c);return(m.length?m:L).map(x=>({value:x.number,sub:x.carrier}))},o=>{
  const hit=L.find(x=>x.number===o.value&&x.carrier===o.sub)||L.find(x=>x.number===o.value);ni.value=o.value;ni.dispatchEvent(new Event('input'));
  const put=(el,val,force)=>{if(el&&val&&(force||!el.value)){el.value=val;el.dispatchEvent(new Event('input'))}};
  put(ci,hit.carrier,true);put($('input',by('UnderlyingEffectiveDate')),hit.eff);put($('input',by('UnderlyingExpirationDate')),hit.exp)})}
"""
m = re.search(r"function lookupize\(f,g\)\{.*?hit\.exp\)\}\)\}\n", s, re.S)
assert m, "lookupize not found"
s = s[:m.start()] + NEW + s[m.end():]
a = ".hide{display:none!important}"
assert a in s
s = s.replace(a, a + """
.combo{position:relative}.combo input{width:100%;padding-right:36px}
.combo .ca{position:absolute;right:10px;top:9px;width:22px;height:22px;color:#555;cursor:pointer}.combo .ca svg{width:22px;height:22px;transform:none}
.combo-list{position:absolute;left:0;right:0;top:100%;margin-top:2px;max-height:240px;overflow:auto;background:#fff;border:1px solid #b9b9b9;border-radius:7px;box-shadow:0 4px 14px rgba(0,0,0,.25);z-index:40}
.combo-list .opt{padding:9px 14px;cursor:pointer;font-size:15px;display:flex;justify-content:space-between;gap:16px}.combo-list .opt small{color:#666;font-size:13px}
.combo-list .opt:hover{background:#e3eef5}.combo-list .opt.none{color:#777;cursor:default;font-size:13px}""", 1)
p.write_text(s, "utf-8")
print("wired")
