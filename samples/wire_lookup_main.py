"""One-off (main site only): Carrier + Underlying Policy Number become lookups (datalist) per selected LOB: pick or type.
Picking a known policy number fills the carrier and the effective/expiration dates when they are empty."""
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "build/risk-page/build_risk_screen.py"
s = p.read_text("utf-8")


def rep(a: str, b: str) -> None:
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


LK = r"""// ---- Underlying policy lookup per LOB (pick from the list or type) ----
function lookupize(f,g){const L=(M.lookup||{})[g]||[];if(!L.length)return;
 const by=n=>[...f.querySelectorAll('.fld')].find(x=>x._a&&x._a.AttributeName===n),car=by('NameID'),num=by('UnderlyingPolicyNumber');if(!car||!num)return;
 const ci=$('input',car),ni=$('input',num),id='lk'+Math.random().toString(36).slice(2,7),dc=H(`<datalist id="${id}c"></datalist>`),dn=H(`<datalist id="${id}n"></datalist>`);
 ci.setAttribute('list',id+'c');ni.setAttribute('list',id+'n');car.append(dc);num.append(dn);
 dc.innerHTML=[...new Set(L.map(x=>x.carrier))].map(c=>`<option value="${esc(c)}">`).join('');
 const fillN=()=>{const c=ci.value.trim().toLowerCase(),m=L.filter(x=>!c||x.carrier.toLowerCase()===c);dn.innerHTML=(m.length?m:L).map(x=>`<option value="${esc(x.number)}">${esc(x.carrier)}</option>`).join('')};
 fillN();ci.addEventListener('input',fillN);
 ni.addEventListener('change',()=>{const n=ni.value.trim(),c=ci.value.trim().toLowerCase(),hit=L.find(x=>x.number===n&&c&&x.carrier.toLowerCase()===c)||(c?null:L.find(x=>x.number===n));
  if(!hit)return;const put=(el,val)=>{if(el&&val&&!el.value){el.value=val;el.dispatchEvent(new Event('input'))}};
  put(ci,hit.carrier);put($('input',by('UnderlyingEffectiveDate')),hit.eff);put($('input',by('UnderlyingExpirationDate')),hit.exp)})}
"""
rep("const GROUPS={};\n", "const GROUPS={};\n" + LK)
rep("  tr._v=v;tr._g=s.Description;\n", "  tr._v=v;tr._g=s.Description;lookupize(f,s.Description);\n")
rep('''    return {"page": json.loads((d / "cu_risk_page_metadata.json").read_text("utf-8")),''',
    '''    lk = Path(__file__).resolve().parents[2] / "samples" / "lookup.json"
    return {"lookup": json.loads(lk.read_text("utf-8")), "page": json.loads((d / "cu_risk_page_metadata.json").read_text("utf-8")),''')
p.write_text(s, "utf-8")
print("wired")
