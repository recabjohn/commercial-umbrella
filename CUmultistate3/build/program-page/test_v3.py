"""v3 (commercialumbrella3): + on Policy adds a full policy block per state (prefilled from the primary), rating runs per block,
worksheet shows each state, Previous restores every block. Needs deploy/make_site.py run first. usage: py test_v3.py"""
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

site = Path(__file__).resolve().parents[2] / "deploy" / "commercialumbrella3"
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8773", "--directory", str(site)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)


def gl_row(pg, state, table1):
    pg.locator("h3.sec:has-text('General Liability') .plus").click()
    ex = pg.locator("td.exp").last
    ex.locator(".tags select").select_option(state)
    ex.locator(".fld:has-text('Underlying Each Occurrence Limit') select").select_option("2,000,000")
    ex.locator(".fld:has-text('Table 1 Premium') input").fill(str(table1))
    ex.locator(".fld:has-text('Hired and Non-Owned Auto Limit') ~ .fld:has-text('Premium') input").fill("25")
    ex.locator(".fld:has-text('Carrier') input").fill("Test Carrier")
    ex.locator(".btn").click()


try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1500, "height": 1600})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://localhost:8773/")
        pg.locator("#programs input").first.check()
        pg.click("#lob-next")
        pg.select_option("#state select >> nth=0", "KS")
        pg.select_option("#state .fld:has-text('Accept Certified Acts of Terrorism') select >> nth=0", "No")
        pg.click("#state .save .btn")
        pg.click("h2:text-is('Underlying Insurance Information')")
        gl_row(pg, "KS", 100)                                           # 100 + 25 = 125 rated on KS
        # + on Policy: full policy block for the 2nd state
        pg.click("button[aria-label='Add State']")
        blk = pg.locator("#state .btn.cancel").last.locator("xpath=../..")
        assert blk.locator(".btn.ok").is_hidden() and blk.locator(".btn.cancel").is_visible()
        blk.locator("select").first.select_option("ND")
        assert blk.locator(".btn.ok").is_visible()
        assert blk.locator(".fld:has-text('Policy Coverage Form') select").input_value() == "Commercial Umbrella Coverage Form", "prefilled from primary"
        assert blk.locator(".fld:has-text('Umbrella Limit') select").input_value() == "1,000,000"
        blk.locator(".fld:has-text('Umbrella Limit') select").select_option("2,000,000")   # a state may differ
        blk.locator(".btn.ok").click()
        assert pg.locator("#state section.acc.closed h2").nth(1).inner_text().upper().startswith("ND - ")
        gl_row(pg, "ND", 200)                                           # 200 + 25 = 225 rated on ND
        pg.click("#next")
        pg.wait_for_url("**/program.html")
        assert pg.locator("#rs tbody tr").count() == 2
        assert pg.locator("#rs tbody tr").nth(1).inner_text().find("2,000,000") >= 0, "ND row shows its own limit"
        pg.click("#sv"); pg.wait_for_timeout(1300); pg.click("#gac"); pg.wait_for_timeout(1500)
        assert "$ 350.00" in pg.locator(".carrier").first.inner_text(), pg.locator(".carrier").first.inner_text()
        pg.locator(".carrier").first.locator("text=Preview Rating Worksheet").click()
        ws = pg.locator(".mod").inner_text()
        assert "State KS" in ws and "State ND" in ws and "$ 125.00" in ws and "$ 225.00" in ws and "Policy Term Premium: $ 350.00" in ws, ws
        pg.locator(".mod .cl").click()
        pg.click("#prev")
        pg.wait_for_url("**/risk.html")
        pg.wait_for_timeout(700)
        assert pg.locator("tr[data-saved]").count() == 2
        nd = pg.locator("#state section.acc:has(> .acc-h h2:text-matches('^ND - ', 'i'))")
        nd.locator("h2").click()
        assert nd.locator(".fld:has-text('Umbrella Limit') select").input_value() == "2,000,000", "ND policy block restored"
        assert not errs, errs
        b.close()
finally:
    srv.terminate()
print("ok: v3 policy block per state, per-block rating, worksheet per state, restore")
