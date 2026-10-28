"""Check: dates read-only, Save -> spinner -> Get Available Carriers -> skeleton -> carrier cards. usage: py test_program_page.py"""
from pathlib import Path

from playwright.sync_api import sync_playwright

d = Path(__file__).resolve().parent
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1500, "height": 1500})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((d / "preview_seeded.html").as_uri())
    assert pg.is_hidden("#gac"), "GAC must be hidden before Save"
    assert pg.is_disabled('input[value="10/23/2027"]') and pg.is_disabled('input[value="10/23/2026"]'), "dates read-only"
    assert pg.input_value("#st") == "IL"
    pg.click("#sv")
    pg.wait_for_timeout(300)
    assert pg.is_disabled("#sv") and pg.is_visible("#sv .spin"), "Save spinner"
    pg.wait_for_timeout(1000)
    assert pg.is_visible("#gac") and pg.locator(".carrier").count() == 0
    pg.click("#gac")
    pg.wait_for_timeout(300)
    assert pg.is_visible(".skel")
    pg.wait_for_timeout(1500)
    assert pg.locator(".carrier").count() == 2 and not errs, errs
    pg.screenshot(path=str(d / "preview.png"), full_page=True)
    b.close()
print("ok: program page flow")
