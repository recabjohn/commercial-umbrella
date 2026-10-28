"""Drive the generated screen headless and assert the State -> Policy -> Underlying flow. Run: py -I test_risk_screen.py"""
from pathlib import Path
from playwright.sync_api import sync_playwright

page_url = (Path(__file__).resolve().parent / "cu_risk_screen.html").as_uri()
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(page_url)
    assert pg.locator("h2:text-is('Policy')").count() == 1 and pg.locator("#after").inner_text() == ""   # nothing below State yet
    assert pg.locator("#state .fld").count() == 1                                                      # only State shown
    pg.select_option("#state select", "AL")
    n_fields = pg.locator("#state .fld:not(.hide)").count()
    assert n_fields == 7, n_fields                                                                    # policy fields appear after State
    assert pg.locator("#state label:text-is('Risk Type')").count() == 0                                 # PackagePolicy-only field stays hidden
    assert pg.locator(".fld:has-text('Excess Liability Limit')").first.is_hidden()                      # form-conditional (default = Umbrella form)
    pg.click("#state .save .btn")                                                                       # TerrorismCoverage required -> blocked
    assert pg.locator("#after").inner_text() == ""
    pg.select_option("#state .fld:has-text('Accept Certified Acts of Terrorism') select >> nth=0", "No")
    pg.click("#state .save .btn")
    assert pg.locator("h2:text-is('Underlying Insurance Information')").count() == 1 and pg.locator("h2:text-is('Risk Schedule')").count() == 0 and pg.locator("#next").is_disabled()
    assert pg.locator("h3.sec").count() == 1 + 9, pg.locator("h3.sec").count()                          # Additional Coverages + 9 risk groups
    assert pg.locator("section.acc.closed h2:text-is('Underlying Insurance Information')").count() == 1   # closed after Policy Save
    assert pg.locator(".btn:text-is('Action')").count() == 0
    pg.click("h2:text-is('Underlying Insurance Information')")                                          # opens only on toggle
    pg.locator("h3.sec:has-text('General Liability') .plus").click()
    assert pg.locator(".tbl td.exp .fld").count() == 17                                                # GL detail: 20 FRC fields - 3 non-input (type, 2 headings)
    pg.select_option(".tbl td.exp .fld:has-text('Underlying Each Occurrence Limit') select", "")        # required limit emptied -> blocked
    pg.click(".tbl td.exp .btn")
    assert pg.locator("tr[data-saved]").count() == 0 and pg.locator(".tbl td.exp .fld.err").count() == 1
    pg.select_option(".tbl td.exp .fld:has-text('Underlying Each Occurrence Limit') select", "2,000,000")
    pg.click(".tbl td.exp .btn")                                                                        # ALG rules: all premiums 0 + H&NO limit w/o premium
    msgs = pg.locator(".tbl .rule-err").inner_text()
    assert "At Least One Underlying Liability Premium Must Be Greater Than 0" in msgs, msgs
    assert "Underlying Hired And Non Owned Premium Must Be Greater Than 0" in msgs, msgs
    assert pg.locator("tr[data-saved]").count() == 0
    pg.fill(".tbl td.exp .fld:has-text('Table 1 Premium') input", "100.50")
    pg.fill(".tbl td.exp .fld:has-text('Hired and Non-Owned Auto Limit') ~ .fld:has-text('Premium') input", "25")
    pg.fill(".tbl td.exp .fld:has-text('Carrier') input", "Test Carrier")
    pg.click(".tbl td.exp .btn")
    assert pg.locator("tr[data-saved]").count() == 1 and pg.locator("#next").is_enabled()
    assert pg.locator("tr[data-saved] td:nth-child(2)").inner_text() == "Test Carrier"
    assert not errs, errs
    br.close()
print("ok: screen flow State -> Policy Save -> Underlying row -> Next enabled")
