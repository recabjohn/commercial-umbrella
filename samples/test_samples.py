"""All four sites open pre-filled from the Test Case workbooks; premium reproduces the TC totals. usage: py test_samples.py"""
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
SITES = [  # name, deploy dir, port, expected saved rows (default sample), expected Total Premium
    ("commercialumbrella (AK)", root / "deploy/commercialumbrella", 8781, 9, "$ 976,000.00"),
    ("commercialumbrella2 (AK+KY+AR)", root / "CUmultistate/deploy/commercialumbrella2", 8782, 19, "$ 2,398,712.00"),
    ("commercialumbrella3 (AK+KY+AR)", root / "CUmultistate3/deploy/commercialumbrella3", 8783, 19, "$ 2,418,712.00"),
    ("commercialumbrella4 (AK+KY+AR)", root / "CUmultistate4/deploy/commercialumbrella4", 8784, 19, "$ 2,398,712.00"),
]
procs = [subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--directory", str(d)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
         for _, d, port, _, _ in SITES]
time.sleep(2)
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, _, port, rows, total in SITES:
            pg = b.new_page(viewport={"width": 1500, "height": 1600})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(f"http://localhost:{port}/")
            pg.locator("#programs input").first.check()
            pg.click("#lob-next")
            pg.wait_for_timeout(1200)
            n = pg.locator("tr[data-saved]").count()
            assert n == rows, f"{name}: {n} saved rows, expected {rows}; errs={errs}"
            assert pg.locator("#next").is_enabled(), name
            pg.click("#next")
            pg.wait_for_url("**/program.html")
            pg.click("#sv"); pg.wait_for_timeout(1300); pg.click("#gac"); pg.wait_for_timeout(1500)
            got = pg.locator(".carrier").first.inner_text()
            assert total in got, f"{name}: expected {total}, got {got!r}"
            pg.click("#prev")
            pg.wait_for_url("**/risk.html")
            pg.wait_for_timeout(1200)
            assert pg.locator("tr[data-saved]").count() == rows, f"{name}: restore lost rows"
            assert not errs, (name, errs)
            print("ok:", name, rows, "rows,", total)
            pg.close()
        b.close()
finally:
    for pr in procs:
        pr.terminate()
