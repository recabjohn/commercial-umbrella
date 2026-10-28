"""v4 (commercialumbrella4): Policy container (no +, no State) -> PARTICIPATING STATES (+) -> underlying per state.
Rating per state, worksheet per state, Previous restores. Needs deploy/make_site.py run first. usage: py test_v4.py"""
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

site = Path(__file__).resolve().parents[2] / "deploy" / "commercialumbrella4"
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8774", "--directory", str(site)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)


def gl_row(pg, st, table1):
    st.locator("h2:text-is('Underlying Insurance Information')").first.click()
    st.locator("h3.sec:has-text('General Liability') .plus").click()
    ex = st.locator("td.exp").last
    ex.locator(".fld:has-text('Underlying Each Occurrence Limit') select").select_option("2,000,000")
    ex.locator(".fld:has-text('Table 1 Premium') input").fill(str(table1))
    ex.locator(".fld:has-text('Hired and Non-Owned Auto Limit') ~ .fld:has-text('Premium') input").fill("25")
    ex.locator(".fld:has-text('Carrier') input").fill("Test Carrier")
    ex.locator(".btn").click()


def state_section(pg, code):
    return pg.locator(f"section.acc:has(> .acc-h h2:text-matches('^{code} - ', 'i'))")


try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1500, "height": 1700})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://localhost:8774/")
        pg.evaluate("sessionStorage.setItem('cuSample','NONE')")
        pg.locator("#programs input").first.check()
        pg.click("#lob-next")
        assert pg.locator("#state .plus").count() == 0, "Policy container has no +"
        assert pg.locator("#state .fld:has(label:text-matches('^(Primary )?State', 'i'))").count() == 0, "no State field in Policy"
        assert pg.locator("h2:text-is('States')").count() == 1
        pg.click("button[aria-label='Add State']")
        assert "Save the policy first" in pg.locator(".toast").last.inner_text()
        pg.select_option("#state .fld:has-text('Accept Certified Acts of Terrorism') select >> nth=0", "No")
        pg.click("#state .save .btn")
        assert pg.locator("#state section.acc.closed h2").first.inner_text().upper().startswith("COMMERCIAL UMBRELLA")
        # + under States
        pg.click("button[aria-label='Add State']")
        pg.click("button[aria-label='Add State']")
        assert "Save the open state first" in pg.locator(".toast").last.inner_text()
        pg.locator("#after .stpick select, #after .fld select").last.select_option("KS")
        pg.locator(".btn.ok:has-text('Add State')").click()
        ks = state_section(pg, "KS")
        assert "(PRIMARY STATE)" in ks.locator("> .acc-h h2").inner_text().upper()
        gl_row(pg, ks, 100)                                              # 125 on KS
        pg.click("button[aria-label='Add State']")
        pg.locator("#after .fld select").last.select_option("MO")
        pg.locator(".btn.ok:has-text('Add State')").click()
        mo = state_section(pg, "MO")
        assert "(PRIMARY STATE)" not in mo.locator("> .acc-h h2").inner_text().upper()
        gl_row(pg, mo, 200)                                              # 225 on MO
        assert pg.locator("tr[data-saved]").count() == 2
        pg.click("#next")
        pg.wait_for_url("**/program.html")
        assert pg.locator("#rs tbody tr").count() == 2 and pg.locator("#st option").all_inner_texts() == ["KS", "MO"]
        pg.click("#sv"); pg.wait_for_timeout(1300); pg.click("#gac"); pg.wait_for_timeout(1500)
        assert "$ 350.00" in pg.locator(".carrier").first.inner_text()
        pg.locator(".carrier").first.locator("text=Preview Rating Worksheet").click()
        ws = pg.locator(".mod").inner_text()
        assert "State KS" in ws and "State MO" in ws and "$ 125.00" in ws and "$ 225.00" in ws and "Policy Term Premium: $ 350.00" in ws, ws
        pg.locator(".mod .cl").click()
        pg.click("#prev")
        pg.wait_for_url("**/risk.html")
        pg.wait_for_timeout(700)
        assert pg.locator("tr[data-saved]").count() == 2 and state_section(pg, "KS").count() == 1 and state_section(pg, "MO").count() == 1
        assert pg.locator("#next").is_enabled() and not errs, errs
        b.close()
finally:
    srv.terminate()
print("ok: v4 policy container + participating states, per-state underlying, rating, worksheet, restore")
