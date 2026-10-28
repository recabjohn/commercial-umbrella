"""AK TC preview: 9 groups restored via the real UI, premium = TC 'Policy Term Premium' $976,000. usage: py test_tc_preview.py"""
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

d = Path(__file__).resolve().parent / "preview"
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8770", "--directory", str(d)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1500, "height": 1400})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://localhost:8770/start.html")
        pg.wait_for_url("**/risk.html")
        pg.wait_for_timeout(800)
        toasts = pg.locator(".toast").all_inner_texts()
        n = pg.locator("tr[data-saved]").count()
        print("saved rows:", n, "toasts:", toasts[:3], "errs:", errs)
        assert n == 9, "all 9 groups must save through the real validation"
        pg.click("#state section.acc.closed h2")
        txt = pg.locator("#state").inner_text()
        assert "$ 856,000.00" in txt and "$ 100,000.00" in txt, txt[-600:]
        assert pg.locator("#next").is_enabled()
        pg.screenshot(path=str(d / "risk.png"), full_page=True)
        pg.click("#next")
        pg.wait_for_url("**/program.html")
        pg.click("#sv"); pg.wait_for_timeout(1300); pg.click("#gac"); pg.wait_for_timeout(1500)
        assert "$ 976,000.00" in pg.locator(".carrier").first.inner_text()
        pg.locator(".carrier").first.locator("text=Preview Rating Worksheet").click()
        ws = pg.locator(".mod").inner_text()
        assert "Policy Term Premium: $ 976,000.00" in ws and "$ 500,000.00" in ws and "$ 16,000.00" in ws, ws[-400:]
        pg.screenshot(path=str(d / "worksheet.png"), full_page=True)
        assert not errs, errs
        b.close()
finally:
    srv.terminate()
print("ok: AK TC fill reproduces 1st million $856,000 and Policy Term Premium $976,000")
