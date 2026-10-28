"""End-to-end on the assembled site: LOB -> Risk (policy + GL row) -> Next -> Program Selection -> Previous -> Risk restored.
Needs deploy/make_site.py run first. usage: py test_flow.py"""
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

site = Path(__file__).resolve().parents[2] / "deploy" / "commercialumbrella"
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8766", "--directory", str(site)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1500, "height": 1400})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://localhost:8766/")
        pg.evaluate("sessionStorage.setItem('cuSample','NONE')")
        pg.locator("#programs input").first.check()
        pg.click("#lob-next")
        pg.select_option("#state select", "AL")
        pg.select_option("#state .fld:has-text('Accept Certified Acts of Terrorism') select >> nth=0", "No")
        pg.click("#state .save .btn")
        title = pg.locator("#state section.acc section.acc h2").first.inner_text()
        assert "(PRIMARY STATE)" in title.upper() and title.upper().startswith("AL - "), title
        assert pg.locator("#state section.acc.closed h2").first.inner_text().upper().startswith("AL - ")   # state row collapsed after Save
        pg.click("h2:text-is('Underlying Insurance Information')")
        pg.locator("h3.sec:has-text('General Liability') .plus").click()
        pg.select_option(".tbl td.exp .fld:has-text('Underlying Each Occurrence Limit') select", "2,000,000")
        pg.fill(".tbl td.exp .fld:has-text('Table 1 Premium') input", "100.50")
        pg.fill(".tbl td.exp .fld:has-text('Hired and Non-Owned Auto Limit') ~ .fld:has-text('Premium') input", "25")
        pg.fill(".tbl td.exp .fld:has-text('Carrier') input", "Test Carrier")
        pg.click(".tbl td.exp .btn")
        assert pg.locator("tr[data-saved]").count() == 1
        box = pg.locator("tr[data-saved] .ex .chev").bounding_box()
        assert box and box["width"] > 10, box                                                       # chevron visible
        pg.click("tr[data-saved] .more")
        assert pg.locator(".menu button:text-is('Delete')").is_visible()                            # Action menu
        pg.mouse.click(5, 5)
        assert pg.locator(".menu").count() == 0
        pg.click("#next")
        pg.wait_for_url("**/program.html")
        assert pg.input_value("#st") == "AL"
        pg.click("#prev")
        pg.wait_for_url("**/risk.html")
        pg.wait_for_timeout(300)
        assert pg.locator("tr[data-saved]").count() == 1, "underlying row restored"
        assert pg.locator("tr[data-saved] td:nth-child(2)").inner_text() == "Test Carrier"
        assert pg.locator("#next").is_enabled()
        assert pg.locator("#state section.acc.closed h2").first.inner_text().upper().startswith("AL - ")
        assert not errs, errs
        b.close()
finally:
    srv.terminate()
print("ok: LOB -> Risk -> Program -> Previous restores Risk")
