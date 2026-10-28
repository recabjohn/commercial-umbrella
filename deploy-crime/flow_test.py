"""LOB -> Risk flow over local http. Run: py flow_test.py"""
import subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

srv = subprocess.Popen([sys.executable, "-m", "http.server", "8765", "-d", str(Path(__file__).parent / "site")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page()
        pg.goto("http://localhost:8765/")
        assert pg.locator("#programs label").all_inner_texts()[-1].strip() == "Crime"
        pg.check("input[name=Crime]"); pg.click("#lob-next")
        pg.wait_for_url("**/risk.html")
        assert pg.locator("#tabs .childtab").all_inner_texts() == ["Crime"] and pg.locator("#lob-crime").is_visible()
        assert pg.locator("#next").is_disabled()
        pg.reload(); pg.wait_for_url("http://localhost:8765/")            # refresh rule
        pg.check("input[name=CommercialUmbrella]"); pg.check("input[name=Crime]"); pg.click("#lob-next")
        pg.wait_for_url("**/risk.html")
        assert pg.locator("#tabs .childtab").all_inner_texts() == ["Commercial Umbrella", "Crime"] and pg.locator("#lob-cu").is_visible()
        print("ok: LOB Crime checkbox -> Risk tabs per selection")
        br.close()
finally:
    srv.kill()
