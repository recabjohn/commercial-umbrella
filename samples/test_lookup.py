"""Main site: Carrier / Underlying Policy Number are dropdowns (click to pick, type to filter or enter your own) for every LOB;
picking a known policy number fills carrier + dates. usage: py test_lookup.py"""
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

d = Path(__file__).resolve().parents[1] / "deploy/commercialumbrella"
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8792", "--directory", str(d)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1500, "height": 1700})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://localhost:8792/")
        pg.evaluate("sessionStorage.setItem('cuSample','NONE')")
        pg.locator("#programs input").first.check()
        pg.click("#lob-next")
        pg.click("button[aria-label='Add Policy']")
        pg.select_option("#state select >> nth=0", "KY")
        pg.select_option("#state .fld:has-text('Accept Certified Acts of Terrorism') select >> nth=0", "No")
        pg.click("#state .save .btn")
        pg.click("h2:text-is('Underlying Insurance Information')")
        for grp in ("General Liability", "Aircraft Liability", "Auto Dealers", "Liquor"):          # every LOB gets the dropdowns
            pg.locator(f"h3.sec:has-text('{grp}') .plus").click()
            ex = pg.locator("td.exp").last
            assert ex.locator(".fld:has-text('Carrier') .combo").count() == 1, grp
            assert ex.locator(".fld:has-text('Underlying Policy Number') .combo").count() == 1, grp
        ex = pg.locator("td.exp").nth(2)                                                          # General Liability row (DOM order: Aircraft, Auto Dealers, GL, Liquor)
        car = ex.locator(".fld:has-text('Carrier') input")
        num = ex.locator(".fld:has-text('Underlying Policy Number') input")
        car.click()
        assert ex.locator(".fld:has-text('Carrier') .combo-list").is_visible()
        carriers = ex.locator(".fld:has-text('Carrier') .combo-list .opt b").all_inner_texts()
        assert "AQS" in carriers and "Prime Insurance" in carriers, carriers
        ex.locator(".fld:has-text('Carrier') .combo-list .opt:has(b:text-is('Prime Insurance'))").click()
        assert car.input_value() == "Prime Insurance"
        num.click()
        nums = ex.locator(".fld:has-text('Underlying Policy Number') .combo-list .opt b").all_inner_texts()
        assert nums and all(n.startswith("GL-") for n in nums), nums                              # filtered to the chosen carrier
        car.fill("")
        car.press("Tab")                                                                          # Tab moves on; the number list opens
        ex.locator(".fld:has-text('Underlying Policy Number') .combo-list .opt:has(b:text-is('123456'))").click()
        assert car.input_value() == "AQS" and num.input_value() == "123456"
        assert ex.locator(".fld:has-text('Underlying Policy Effective Date') input").input_value() == "2013-10-01"
        car.fill("My Own Carrier")                                                                # typing a value that is not in the list
        assert "No matches" in ex.locator(".fld:has-text('Carrier') .combo-list").inner_text()
        num.fill("ZZ-999")
        pg.mouse.click(5, 5)
        assert car.input_value() == "My Own Carrier" and num.input_value() == "ZZ-999"
        assert not errs, errs
        pg.screenshot(path=str(Path(__file__).resolve().parent / "lookup.png"), full_page=False)
        b.close()
finally:
    srv.terminate()
print("ok: Carrier / Underlying Policy Number dropdowns (pick or type) on every LOB")
