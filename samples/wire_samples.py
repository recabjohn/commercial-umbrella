"""One-off: wire the sample data into the four sites (toast muted while the page replays a sample; make_site injects seed + selector)."""
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
SITES = {"single": root, "v2": root / "CUmultistate", "v3": root / "CUmultistate3", "v4": root / "CUmultistate4"}

for kind, base in SITES.items():
    p = base / "build/risk-page/build_risk_screen.py"
    s = p.read_text("utf-8")
    if "window.QUIET" not in s:
        a = "function toast(t,bad){const e=H("
        assert a in s, p
        s = s.replace(a, "function toast(t,bad){if(window.QUIET)return;const e=H(", 1)
        b = "function restore(){let s=null;"
        assert b in s, p
        s = s.replace(b, "function restore(){window.QUIET=true;try{restore0()}finally{window.QUIET=false}}\nfunction restore0(){let s=null;", 1)
        p.write_text(s, "utf-8")
    m = base / "deploy/make_site.py"
    t = m.read_text("utf-8")
    if "seed_" not in t:
        a = 'assert "cuFlow" in lob and "cuFlow" in risk'
        assert a in t, m
        blk = (f"SAMP = next(p / 'samples' for p in Path(__file__).resolve().parents if (p / 'samples').exists())\n"
               f"risk = risk.replace('</head>', (SAMP / 'seed_{kind}.html').read_text('utf-8') + '</head>', 1).replace(\n"
               f"    '</body>', (SAMP / 'bar_{kind}.html').read_text('utf-8') + '</body>', 1)\n")
        t = t.replace(a, blk + a, 1)
        m.write_text(t, "utf-8")
    print("wired", kind)
