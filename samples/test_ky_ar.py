"""Main site with the KY and AR samples picked from the selector: TC totals $1,381,000 (KY) and $61,712 (AR). usage: py test_ky_ar.py"""
import subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
d = Path(__file__).resolve().parents[1] / "deploy/commercialumbrella"
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8791", "--directory", str(d)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.5)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1500, "height": 1600}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        for pick, rows, total in (("KY", 9, "$ 1,381,000.00"), ("AR", 1, "$ 61,712.00")):
            pg.goto("http://localhost:8791/"); pg.evaluate(f"sessionStorage.clear();sessionStorage.setItem('cuSample','{pick}')")
            pg.locator("#programs input").first.check(); pg.click("#lob-next"); pg.wait_for_timeout(1200)
            assert pg.locator("tr[data-saved]").count() == rows, (pick, pg.locator("tr[data-saved]").count())
            pg.click("#next"); pg.wait_for_url("**/program.html")
            pg.click("#sv"); pg.wait_for_timeout(1300); pg.click("#gac"); pg.wait_for_timeout(1500)
            assert total in pg.locator(".carrier").first.inner_text(), (pick, pg.locator(".carrier").first.inner_text())
            print("ok:", pick, rows, "rows,", total)
        assert not errs, errs
        b.close()
finally:
    srv.terminate()
