"""Build the CU Line Of Business screen as one standalone HTML file.

Shell CSS and markup are reused from the endo-nav prototype (endo-nav/site/index.html):
header, hover-expand sidebar, step bar, Details box, Program Information card, Previous/Next,
footer, code tab, chat button. Those files are read-only here; the CSS below is a trimmed copy.
Generated from metadata: Details (ExpandPanel), ProgramInformation checkboxes, Previous/Next.
Logo is embedded from the supplied PNG so the output is standalone.

usage: py -I build_screen.py <lob_page.json> <expand_panel.json> <logo.png> <out.html>
"""
import base64
import html
import json
import sys
from pathlib import Path

STEPS = ("Agency & Agent", "Insured Details", "Line Of Business", "Risk/Coverage", "Program Selection")
ACTIVE_STEP = 2

CHECK = '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2m-2 15-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8z"/>'
DOC = '<path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8zm2 16H8v-2h8zm0-4H8v-2h8zm-3-5V3.5L18.5 9z"/>'
ICON = {
    "note": "M19 5v9h-5v5H5V5zm0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h10l6-6V5c0-1.1-.9-2-2-2m-7 11H7v-2h5zm5-4H7V8h10z",
    "bell": "M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2m6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1zm-2 1H8v-6c0-2.48 1.51-4.5 4-4.5s4 2.02 4 4.5z",
    "tune": "M3 17v2h6v-2zM3 5v2h10V5zm10 16v-2h8v-2h-8v-2h-2v6zM7 9v2H3v2h4v2h2V9zm14 4v-2H11v2zm-6-4h2V7h4V5h-4V3h-2z",
    "home": "M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z",
    "find": "M7 9H2V7h5zm0 3H2v2h5zm13.59 7-3.83-3.83c-.8.52-1.74.83-2.76.83-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5c0 1.02-.31 1.96-.83 2.75L22 17.59zM17 11c0-1.65-1.35-3-3-3s-3 1.35-3 3 1.35 3 3 3 3-1.35 3-3M2 19h10v-2H2z",
    "sub": "M19 3h-4.18C14.4 1.84 13.3 1 12 1s-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM8 17l.6-2.4 6-6 1.8 1.8-6 6zM15.2 8l.9-.9a.6.6 0 0 1 .85 0l.95.95a.6.6 0 0 1 0 .85l-.9.9z",
    "gear": "M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6",
    "more": "M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6z",
    "chat": "M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2M6 9h12v2H6zm8 5H6v-2h8zm4-6H6V6h12z",
}

# trimmed from endo-nav/site/index.html (shell, steps, Details box, program card, buttons, footer)
CSS = """
:root{--navy:#0d2a4f;--btn-grad:linear-gradient(90deg,#112b50,#4c6c8f);--side-grad:linear-gradient(180deg,#13284d 0%,#4b7191 100%);--header-h:69px;--side-w:81px;--side-w-open:300px}
*{box-sizing:border-box}
body{margin:0;font-family:"Noto Sans",Arial,sans-serif;color:#111;background:#f5f5f5;min-height:100vh}
svg{fill:currentColor;display:block}
.header{position:fixed;inset:0 0 auto 0;height:var(--header-h);background:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 0 0 20px;z-index:30}
.header::after{content:"";position:absolute;left:374px;right:0;bottom:0;height:1px;box-shadow:0 2px 4px rgba(0,0,0,.55)}
.logo{display:block}
.tools{display:flex;align-items:center}
.tools button{background:none;border:0;padding:0;width:65px;display:flex;justify-content:center;color:#444;cursor:pointer}
.tools svg{width:26px;height:26px}
.tools .avatar{width:37px;height:37px;border-radius:50%;background:#6a3fb5;color:#fff;font-weight:700;font-size:17px;display:flex;align-items:center;justify-content:center}
.sidebar{position:fixed;top:var(--header-h);bottom:0;left:0;width:var(--side-w);z-index:20;background:var(--side-grad);color:#fff;overflow:hidden;padding-top:19px;transition:width .2s ease}
.sidebar:hover{width:var(--side-w-open)}
.item{display:flex;align-items:center;height:50px;margin:0 14px 0 20px;padding:0 12px;border-radius:6px;white-space:nowrap;font-size:20px;cursor:pointer;color:#fff;text-decoration:none}
.item svg{width:26px;height:26px;flex:none}
.item .label{margin-left:19px;opacity:0;transition:opacity .15s}
.sidebar:hover .item .label{opacity:1}
.item:hover,.item.active{background:rgba(255,255,255,.12)}
.item.find{margin-top:20px}
.children{display:none;margin-top:10px}
.sidebar:hover .children{display:block}
.children .item{padding-left:35px;border-radius:0}
.item.manage{margin-top:20px}
.sidebar:hover .item.manage{margin-top:10px}
.main{margin-left:var(--side-w);padding-top:var(--header-h);min-height:100vh;display:flex;flex-direction:column}
.main>.page{flex:1;padding:31px 32px 40px 33px}
.crumbs{display:flex;justify-content:space-between;align-items:center;height:72px;padding:0 22px 0 8px;background:#fff;border-radius:10px;box-shadow:0 1px 6px rgba(0,0,0,.15);margin-bottom:14px}
.crumb{display:flex;align-items:center;gap:14px;border:0;background:none;padding:0 8px;font:inherit;font-size:18px;color:#222;cursor:default}
.crumb svg{width:26px;height:26px}
.crumb.done,.crumb.done span{color:#1b7f3b}
.crumb.active span{font-size:16px;font-weight:500;text-decoration:underline;text-underline-offset:5px}
.isum{background:#fff;border-radius:10px;box-shadow:0 1px 6px rgba(0,0,0,.15);overflow:hidden;margin-bottom:14px}
.isum-head{display:flex;align-items:center;height:44px;padding:0 22px 0 20px;background:#52779a;color:#fff;text-transform:uppercase;font-size:17px;font-weight:600;letter-spacing:.3px}
.isum-head .tog{margin-left:auto;border:0;background:none;padding:0;color:#fff;cursor:pointer}
.isum-head .tog svg{width:26px;height:26px;transition:transform .2s}
.isum.collapsed .isum-head .tog svg{transform:rotate(180deg)}
.isum.collapsed .isum-body{display:none}
.isum-body{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:22px 28px;padding:24px 32px 28px;margin:0}
.isum-body div{display:block;font-size:15px}
.isum-body dt{font-weight:700;color:#333;margin-bottom:6px}
.isum-body dd{margin:0;font-weight:700;color:#111;overflow-wrap:anywhere}
.progcard{background:#fff;border-radius:10px;box-shadow:0 1px 6px rgba(0,0,0,.15);padding:22px 24px 26px}
.progcard h2{margin:0;font-size:28px;font-weight:600;color:#555}
.progcard h3{margin:18px 0 14px;font-size:18px;font-weight:400;color:#222}
.progcard label{display:flex;align-items:center;gap:14px;padding:14px;font-size:15px;color:#333;cursor:pointer;width:fit-content}
.progcard input[type=checkbox]{width:20px;height:20px;accent-color:var(--navy);cursor:pointer}
.lobnav{display:flex;justify-content:space-between;margin:24px 24px 0}
.btn{height:40px;padding:0 16px;min-width:88px;border:0;border-radius:5px;background:var(--btn-grad);color:#fff;font:inherit;font-size:15.6px;font-weight:500;cursor:pointer}
.btn:hover{filter:brightness(1.12)}
.btn:disabled{opacity:.45;cursor:not-allowed;filter:none}
.footer{height:63px;background:#d9d9d9;border-top:1px solid #cfcfcf;display:flex;align-items:center;justify-content:space-between;padding:0 20px;font-size:16px;color:#222}
.footer a{color:#1f9bd7;text-decoration:none}
.code-tab{position:fixed;right:0;top:261px;width:70px;height:57px;background:#c6cbd3;z-index:15;border-radius:28px 0 0 28px;display:flex;align-items:center;justify-content:center;color:#222;cursor:pointer}
.fab{position:fixed;right:22px;bottom:24px;width:65px;height:65px;border-radius:50%;border:0;background:#13284d;color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 8px rgba(0,0,0,.3);cursor:pointer;z-index:40}
.fab svg{width:20px;height:20px}
"""

# Next stays locked until a program is ticked (mirrors Action.UIReadOnlyConditions in the metadata).
JS = """
const boxes=[...document.querySelectorAll('#programs input')],next=document.getElementById('lob-next');
const sync=()=>{next.disabled=!boxes.some(b=>b.checked)};boxes.forEach(b=>b.addEventListener('change',sync));sync();
"""


def svg(path: str) -> str:
    return f'<svg viewBox="0 0 24 24"><path d="{path}"/></svg>'


def tiles(page: dict) -> dict:
    return {s["TileName"]: s for s in page["ApplicationDetail"]["SubApplicationDetailList"]}


def header(logo: str) -> str:
    tools = "".join(f'<button aria-label="{n}">{svg(ICON[k])}</button>' for k, n in (("note", "Sticky notes"), ("bell", "Notifications"), ("tune", "Settings")))
    return (f'<header class="header"><img class="logo" src="{logo}" alt="Solartis" width="100" height="45">'
            f'<div class="tools">{tools}<button aria-label="Account"><span class="avatar">U</span></button></div></header>')


def sidebar() -> str:
    def item(cls, key, label):
        return f'<a class="item {cls}" href="#">{svg(ICON[key])}<span class="label">{label}</span></a>'
    kids = "".join(f'<a class="item" href="#"><span class="label" style="opacity:1;margin-left:0">{k}</span></a>'
                   for k in ("Insured", "Submission", "Quote", "Policy", "General Agency", "Agency", "Agent", "User Account"))
    return ('<nav class="sidebar" aria-label="Main">' + item("home", "home", "Home") + item("active", "sub", "Submission")
            + item("find", "find", "Find") + f'<div class="children">{kids}</div>' + item("manage", "gear", "Manage") + "</nav>")


def steps() -> str:
    parts = []
    for i, name in enumerate(STEPS):
        state = "done" if i < ACTIVE_STEP else "active" if i == ACTIVE_STEP else ""
        parts.append(f'<span class="crumb {state}"><svg viewBox="0 0 24 24">{CHECK if i < ACTIVE_STEP else DOC}</svg><span>{html.escape(name)}</span></span>')
    return f'<nav class="crumbs steps" aria-label="Submission steps">{"".join(parts)}</nav>'


def details(expand: dict) -> str:
    sub = tiles(expand)["ExpandPanel"]
    cells = "".join(f'<div><dt>{html.escape(a["ComponentLabel"])}</dt><dd>{html.escape(a["DefaultValue"])}</dd></div>'
                    for a in sub["AttributeDetailList"] if a["IsInvisible"] != "Y")
    return (f'<section class="isum stack"><div class="isum-head"><span>{html.escape(sub["Description"])}</span>'
            f'<button type="button" class="tog" aria-label="Collapse details">{svg(ICON["more"])}</button></div>'
            f'<dl class="isum-body">{cells}</dl></section>')


def programs(sub: dict) -> str:
    head = {a["ComponentType"]: a["ComponentLabel"] for a in sub["AttributeDetailList"] if a["ComponentType"] in ("Heading", "SubHeading")}
    boxes = "".join(f'<label><input type="checkbox" name="{html.escape(a["AttributeName"])}" value="{html.escape(a["ComponentLabel"])}"> {html.escape(a["ComponentLabel"])}</label>'
                    for a in sub["AttributeDetailList"] if a["ComponentType"] == "CheckBox" and a["IsInvisible"] != "Y")
    return (f'<section class="progcard"><h2>{html.escape(head["Heading"])}</h2><h3>{html.escape(head["SubHeading"])}</h3>'
            f'<div id="programs" role="group" aria-label="{html.escape(head["SubHeading"])}">{boxes}</div></section>')


def nav(sub: dict) -> str:
    btns = "".join(f'<button class="btn" type="button"{" id=lob-next disabled" if a["Action"].get("goto") == "next" else " id=lob-prev"}>{html.escape(a["ComponentLabel"])}</button>'
                   for a in sub["AttributeDetailList"])
    return f'<div class="lobnav">{btns}</div>'


def screen(page: dict, expand: dict, logo: str) -> str:
    t = tiles(page)
    foot = ('<footer class="footer"><span><a href="https://solartis.com" target="_blank" rel="noopener noreferrer">Solartis</a> &copy; 2026</span>'
            '<span>Powered by <a href="https://solartis.com" target="_blank" rel="noopener noreferrer">Solartis</a></span></footer>')
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Line Of Business - Commercial Umbrella</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body>{header(logo)}{sidebar()}<main class="main"><div class="page">'
            f'{steps()}{details(expand)}{programs(t["ProgramInformation"])}{nav(t["NavigationButtonsSubmission"])}</div>{foot}</main>'
            f'<div class="code-tab" aria-label="Show request/response">{svg("M8 6l-6 6 6 6M16 6l6 6-6 6").replace("<svg", "<svg fill=none stroke=currentColor stroke-width=2.2 width=20 height=20")}</div>'
            f'<button class="fab" aria-label="AI Assistant">{svg(ICON["chat"])}</button><script>{JS}</script></body></html>')


if __name__ == "__main__":
    lob, exp, logo, out = (Path(a) for a in sys.argv[1:5])
    uri = "data:image/png;base64," + base64.b64encode(logo.read_bytes()).decode("ascii")
    out.write_text(screen(json.loads(lob.read_text("utf-8")), json.loads(exp.read_text("utf-8")), uri), encoding="utf-8")
    print("wrote", out)
