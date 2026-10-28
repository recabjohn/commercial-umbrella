"""Headless multi-state flow. Run: py test_risk_screen.py"""
from pathlib import Path
from playwright.sync_api import sync_playwright

url = (Path(__file__).resolve().parent / "cu_risk_screen.html").as_uri()


def policy(pg, code, idx):
    pg.click("button[aria-label='Add Policy']")
    card = pg.locator("#states > .acc").nth(idx)
    card.locator(".fld select").first.select_option(code)
    card.locator(".fld:has-text('Accept Certified Acts of Terrorism') select").first.select_option("No")
    for lab in ("TRIP terminates", ):
        s = card.locator(f".fld:has-text('{lab}') select")
        if s.count() and s.first.is_visible():
            s.first.select_option("No")
    card.locator(".save .btn").first.click()
    return card


with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("dialog", lambda d: d.accept())
    pg.goto(url)
    assert pg.locator("h2:text-is('Policy')").count() == 1 and pg.locator("#states > .acc").count() == 0
    c0 = policy(pg, "AL", 0)
    assert "AL-Alabama (Primary State)" in pg.locator("#states > .acc >> nth=0").inner_text().upper().replace("ALABAMA", "Alabama") or "PRIMARY" in pg.locator("#states > .acc").nth(0).inner_text().upper()
    assert pg.locator("#states > .acc").nth(0).locator("h3.sec:has-text('Additional Coverages')").count() == 1      # saved -> per-state sections appear
    pg.click("button[aria-label='Add Policy']")                                                               # 2nd state; open (blank) one blocks a third
    pg.click("button[aria-label='Add Policy']"); assert pg.locator("#states > .acc").count() == 2
    c1 = pg.locator("#states > .acc").nth(1)
    c1.locator(".fld select").first.select_option("AL")                                                       # duplicate state
    assert c1.locator(".fld select").first.input_value() == "" and pg.locator("#states > .acc").nth(1).locator(".save").count() == 0
    c1.locator(".fld select").first.select_option("ND")                                                       # monopolistic state
    c1.locator(".fld:has-text('Accept Certified Acts of Terrorism') select").first.select_option("No")
    c1.locator(".save .btn").first.click()
    summ = pg.locator("#summary").inner_text()
    assert "AL-Alabama" in summ and "ND-North Dakota" in summ and "monopolistic" in summ and "No General Liability underlying scheduled" in summ, summ
    assert pg.locator("#next").is_disabled()
    pg.locator("#states > .acc").nth(0).locator("h2:text-is('Underlying Insurance Information')").click()
    pg.locator("#states > .acc").nth(0).locator("h3.sec:has-text('General Liability') .plus").click()
    ex = pg.locator("#states > .acc").nth(0).locator("td.exp")
    ex.locator(".fld:has-text('Underlying Each Occurrence Limit') select").select_option("50,000")
    ex.locator(".fld:has-text('Table 1 Premium') input").fill("100")
    ex.locator(".fld:has-text('Hired and Non-Owned Auto Limit') ~ .fld:has-text('Premium') input").fill("25")
    ex.locator(".fld:has-text('Carrier') input").fill("Test Carrier")
    ex.locator(".btn").click()
    assert pg.locator("#states tr[data-saved]").count() == 1, pg.locator(".toast").all_inner_texts()
    assert "GL each occurrence $50,000 is below the typical $1,000,000" in pg.locator("#summary").inner_text(), pg.locator("#summary").inner_text()
    assert "No General Liability underlying scheduled" not in pg.locator("#summary tr").nth(1).inner_text()
    assert pg.locator("#next").is_enabled()
    assert not errs, errs
    br.close()
print("ok: multi-state flow (add states, primary flag, duplicate check, summary checks, Next)")
