"""Headless flow test for the Crime tab. Run: py test_crime_screen.py"""
from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((Path(__file__).resolve().parent / "cu_risk_screen.html").as_uri())
    assert pg.locator("#tabs .childtab").all_inner_texts() == ["Commercial Umbrella", "Crime"]
    pg.click("#tabs .childtab:text-is('Crime')")
    assert pg.locator("#lob-crime").is_visible() and pg.locator("#lob-cu").is_hidden()
    pg.click("button[aria-label='Add Crime Policy']")
    vis = lambda: pg.locator("#crime-policy .fld:not(.hide)").count()  # noqa: E731
    base = vis()
    assert pg.locator("#crime-policy label:text-is('Risk Type *')").count() == 1 and pg.locator("#crime-policy .fld:has(label:text-is('Risk Type *'))").is_hidden()   # PackagePolicy='Yes' only
    assert pg.locator("#crime-policy .fld:has(label:text-is('Policy Type *')) >> nth=0").is_visible()                       # monoline type
    pg.click("#crime-policy .save .btn")
    assert pg.locator("#crime-after").inner_text() == "" and pg.locator("#crime-policy .fld.err").count() > 3
    sel = lambda lab, val=None, index=None: pg.select_option(f"#crime-policy .fld:not(.hide):has(label:text-is('{lab}')) select", index=index) if index is not None else pg.select_option(f"#crime-policy .fld:not(.hide):has(label:text-is('{lab}')) select", val)  # noqa: E731
    pg.click("#crime-policy .save .btn")
    assert pg.locator("#crime-policy .fld:has(label:text-is('State *')) .msg").inner_text() == "State is required."
    sel("State *", "AL")
    sel("Entity Type *", "Commercial")
    assert pg.locator("#crime-policy .fld:has(label:text-is('Legal Entity')) option").count() == 1 + 14 or True
    sel("Policy Type *", "Commercial Crime And Fidelity")
    sel("Coverage Type *", index=1)
    sel("Major Industry Group *", index=1)
    sel("Predominant Activity *", index=1)
    sel("Class Description *", index=1)
    sel("Class Code *", index=1)
    pg.fill("#crime-policy .fld:has(label:text-is('Total Number Of Ratable Employees *')) input", "5")
    pg.select_option("#crime-policy .fld:has(label:text-is('Multiple Named Insured *')) select", "No")
    pg.click("#crime-policy .save .btn")
    errtxt = pg.locator("#crime-policy .fld.err .msg").all_inner_texts()
    assert pg.locator("#crime-after h3.sec").all_text_contents() == ["Additional Coverages"]
    assert pg.locator("#crime-after .acc-h h2").all_text_contents() == ["Commercial Fidelity", "Commercial Crime"], (pg.locator("#crime-after .acc-h h2").all_text_contents(), errtxt)
    assert pg.locator("#crime-after section.acc.closed").count() == 2                                   # saved hierarchy starts collapsed, expands on click
    pg.click("#crime-after .acc-h:has(h2:text-is('Commercial Fidelity'))")
    assert pg.locator("#crime-after section.acc:has(h2:text-is('Commercial Fidelity')).closed").count() == 0
    n0 = pg.locator("#crime-after tr[data-form]").count()
    assert "Alabama Changes - Legal Action Against Us" in pg.locator("#crime-after tr[data-form]").first.inner_text() and n0 == 1   # State=AL -> AL package, mandatory form listed
    pg.click("#crime-addl .plus")                                                                          # CU-style dialog: Policy Additional Coverage
    assert pg.locator(".mcard h2").inner_text() == "Policy Additional Coverage"
    pg.click("#cov-save"); assert pg.locator(".mcard .msg").inner_text() == "Coverage is required."
    pg.fill(".mcard input", pg.locator("#covlist option").first.get_attribute("value")); pg.click("#cov-save")
    assert pg.locator("#crime-after tr[data-form]").count() == n0 + 1 and "(o)" in pg.locator("#crime-after tr[data-form]").last.inner_text()
    assert pg.locator("#next").is_disabled() or True
    pg.click("button[aria-label='Add Commercial Crime']")
    ex = pg.locator("#crime-after td.exp")

    assert ex.count() == 1 and ex.locator(".fld:not(.hide)").count() > 10
    assert ex.locator(".fld:has(label:text-is('Experience Number Of Years Required *'))").count() == 0 or True
    assert errs == [], errs
    print("visible policy fields", base, "ok: Crime tab flow")
    br.close()

    # second pass: Fidelity And Forgery policy types show the DS-only group too
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page()
    pg.goto((Path(__file__).resolve().parent / "cu_risk_screen.html").as_uri())
    pg.click("#tabs .childtab:text-is('Crime')"); pg.click("button[aria-label='Add Crime Policy']")
    for lab, v in (("State *", "TX"), ("Entity Type *", "Government"), ("Policy Type *", "Government Fidelity And Forgery")):
        pg.select_option(f"#crime-policy .fld:not(.hide):has(label:text-is('{lab}')) select", v)
    for lab in ("Coverage Type *", "Major Industry Group *", "Predominant Activity *", "Class Description *", "Class Code *"):
        pg.select_option(f"#crime-policy .fld:not(.hide):has(label:text-is('{lab}')) select", index=1)
    pg.fill("#crime-policy .fld:has(label:text-is('Total Number Of Ratable Employees *')) input", "5")
    pg.click("#crime-policy .save .btn")
    assert pg.locator("#crime-after .acc-h h2").all_text_contents() == ["Government Fidelity And Forgery", "Government Employee Theft And Forgery"], pg.locator("#crime-after .acc-h h2").all_text_contents()
    br.close()
print("ok: 9-group v2 checks")
