"""Every FRC condition evaluates; Included/Limit range rule; keyed cascade. Run: py test_crime_rules.py"""
from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page()
    pg.goto((Path(__file__).resolve().parent / "cu_risk_screen.html").as_uri())
    n = pg.evaluate("""()=>{let n=0;const fs=[...CR.policy,...CR.groups.flatMap(g=>[...g.summary,...g.detail])];
      for(const f of fs)for(const c of [f.cond,f.reqCond]){if(c){ccond(c,{});ccond(c,new Proxy({},{get:()=>'Yes'}));n++}}return n}""")
    assert n > 300, n
    g = "Commercial Crime"
    r = pg.evaluate("""g=>{const G=CR.groups.find(x=>x.name===g),v={},w=cform(G.detail,v),F=G.detail;
      const inc=F.find(f=>f.n==='InsidePremTheftOfMoneyIncluded'),lim=F.find(f=>/InsideThePremisesTheftOfMoneyAndSecuritiesCoverage\.Limit$/.test(f.n));
      const e=n=>w.querySelector('[data-f="'+n+'"]');
      const out={noRange:crange(lim,v,F)};v[inc.n]='Yes';crefresh(w,v,F);out.yesRange=crange(lim,v,F);
      e(lim.n).querySelector('input').value='0';v[lim.n]='0';out.valid0=cvalid(w,v,F);out.msg=e(lim.n).querySelector('.msg').textContent;return out}""", g)
    assert r["noRange"] == {"min": 0, "max": 0} and r["yesRange"] == {"min": 1, "max": 999999999}, r
    assert r["valid0"] is False and "between 1 and 999999999" in r["msg"], r
    c = pg.evaluate("""()=>{const v={EntityType:'Government'},o=copts(CR.policy.find(f=>f.n==='MonolinePolicyType'),v,CR.policy).map(x=>x.v);return o}""")
    assert c == ["Government Crime", "Government Fidelity", "Government Crime And Fidelity", "Government Fidelity And Forgery", "Kidnap/Ransom And Extortion"], c
    pa = pg.evaluate("""()=>{const v={MajorIndustryGroup:CR.domains.PredominantActivity.items[0].k};return [copts(CR.policy.find(f=>f.n==='PredominantActivity'),v,CR.policy).length]}""")
    assert pa[0] > 0, pa
    cc = pg.evaluate("""()=>{const v={PredominantActivity:CR.domains.ClassCode.items[0].k};return copts(CR.policy.find(f=>f.n==='ClassCode'),v,CR.policy).length}""")
    assert cc > 0, cc
    print("ok:", n, "conditions evaluate; limit range, Government cascade, Class Code cascade")
    br.close()
