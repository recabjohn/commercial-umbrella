"""v3: the pending state block always has Cancel; Save appears once a state is chosen."""
p = "build_risk_screen.py"
s = open(p, encoding="utf-8").read()


def rep(a: str, b: str) -> None:
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


rep(" let b=null;\n function showRest(){row.rest=form(policyAttrs.slice(1),tmp);host.append(row.rest);\n"
    "  b=H('<div class=\"save\" style=\"gap:10px\"><button type=\"button\" class=\"btn cancel\">Cancel</button><button type=\"button\" class=\"btn ok\">Save</button></div>');host.append(b);\n"
    "  $('.ok',b).onclick=()=>{if(save())toast('State saved successfully')};$('.cancel',b).onclick=()=>dropRow(row);showPremium()}",
    " const b=H('<div class=\"save\" style=\"gap:10px\"><button type=\"button\" class=\"btn cancel\">Cancel</button><button type=\"button\" class=\"btn ok hide\">Save</button></div>');host.append(b);\n"
    " $('.ok',b).onclick=()=>{if(save())toast('State saved successfully')};$('.cancel',b).onclick=()=>dropRow(row);\n"
    " function showRest(){row.rest=form(policyAttrs.slice(1),tmp);b.before(row.rest);$('.ok',b).classList.remove('hide');showPremium()}")
open(p, "w", encoding="utf-8").write(s)
print("ok")
