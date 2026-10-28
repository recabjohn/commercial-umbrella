"""Multistate v2 end-to-end on the assembled site: one Policy (no +), Additional States, underlying rows tagged by state,
Next -> Program Selection (one schedule row per state) -> Previous restores everything.
Needs deploy/make_site.py run first. usage: py test_flow.py"""
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

site = Path(__file__).resolve().parents[2] / "deploy" / "commercialumbrella3"
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8772", "--directory", str(site)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)


def gl_row(pg, states):
    pg.locator("h3.sec:has-text('General Liability') .plus").click()
    ex = pg.locator("td.exp").last
    ex.locator(".fld:has-text('Underlying Each Occurrence Limit') select").select_option("2,000,000")
    ex.locator(".fld:has-text('Table 1 Premium') input").fill("100")
    ex.locator(".fld:has-text('Hired and Non-Owned Auto Limit') ~ .fld:has-text('Premium') input").fill("25")
    ex.locator(".fld:has-text('Carrier') input").fill("Test Carrier")
    for c in states:                                              # default = all states ticked; untick the others
        pass
    return ex


try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1500, "height": 1600})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://localhost:8772/")
        pg.locator("#programs input").first.check()
        pg.click("#lob-next")
        assert pg.locator("button[aria-label='Add Policy']").count() == 0, "Policy must be a single record (no +)"
        assert pg.locator("#state label:text-is('Primary State *')").count() == 1
        pg.select_option("#state select >> nth=0", "KS")
        pg.select_option("#state .fld:has-text('Accept Certified Acts of Terrorism') select >> nth=0", "No")
        pg.click("#state .save .btn")
        row = pg.locator("#state section.acc.closed h2").first.inner_text().upper()
        assert row.startswith("KS - ") and "(PRIMARY STATE)" in row, row
        # one state only -> the State dropdown defaults to it
        pg.click("h2:text-is('Underlying Insurance Information')")
        ex = gl_row(pg, [])
        assert ex.locator(".tags select").input_value() == "KS", "single policy state must be the default"
        assert ex.locator(".tags select option").count() == 1
        ex.locator(".btn").click()
        assert pg.locator("tr[data-saved] td").nth(-2).inner_text() == "KS"
        # + on Policy adds a state row (State only; policy fields stay singleton)
        assert pg.locator("h3.sec:has-text('Additional States')").count() == 0, "no Additional States section"
        pg.click("button[aria-label='Add State']")
        blk = pg.locator("#state select").last
        assert pg.locator("button[aria-label='Add State']").count() == 1
        blk.select_option("ND")
        pg.locator("#state .btn.ok").last.click()
        assert pg.locator("#state section.acc.closed h2").nth(1).inner_text().upper().startswith("ND - "), pg.locator("#state section.acc h2").all_inner_texts()
        pg.click("button[aria-label='Add State']")
        pg.locator("#state select").last.select_option("MO")
        pg.locator("#state .btn.ok").last.click()
        pg.click("button[aria-label='Add State']")
        pg.click("button[aria-label='Add State']")
        assert "Save the open state first" in pg.locator(".toast").last.inner_text()
        pg.locator("#state .btn.cancel").last.click()
        assert pg.locator("#state section.acc.closed h2").count() >= 3
        # second GL row: dropdown lists only policy states + All States, must be chosen
        ex = gl_row(pg, [])
        assert ex.locator(".tags select option").all_inner_texts()[0] == "Select"
        assert [o for o in ex.locator(".tags select option").evaluate_all("e=>e.map(x=>x.value)")] == ["", "KS", "ND", "MO", "ALL"]
        ex.locator(".btn").click()
        assert pg.locator("tr[data-saved]").count() == 1 and ex.locator(".tags.err").count() == 1, "State is required"
        ex.locator(".tags select").select_option("ALL")
        ex.locator(".btn").click()
        assert pg.locator("tr[data-saved]").count() == 2
        assert pg.locator("tr[data-saved]").nth(0).locator("td").nth(-2).inner_text() == "KS" and pg.locator("tr[data-saved]").nth(1).locator("td").nth(-2).inner_text() == "KS,ND,MO"
        pg.click("#next")
        pg.wait_for_url("**/program.html")
        assert pg.locator("#st option").all_inner_texts() == ["KS", "ND", "MO"], pg.locator("#st option").all_inner_texts()
        assert pg.locator("#rs tbody tr").count() == 3
        pg.click("#prev")
        pg.wait_for_url("**/risk.html")
        pg.wait_for_timeout(600)
        assert pg.locator("tr[data-saved]").count() == 2 and pg.locator("tr[data-saved]").nth(1).locator("td").nth(-2).inner_text() == "KS,ND,MO"
        assert pg.locator("#next").is_enabled()
        assert not errs, errs
        b.close()
finally:
    srv.terminate()
print("ok: multistate v2 flow (single policy, additional states, state dropdown, program, restore)")
