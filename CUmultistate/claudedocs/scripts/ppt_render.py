"""Export selected slides of a pptx to PNG via PowerPoint COM.
usage: py -I ppt_render.py <deck.pptx> <out dir> [slide numbers...]
"""
import sys
from pathlib import Path

import win32com.client

deck, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
want = [int(a) for a in sys.argv[3:]]
app = win32com.client.Dispatch("PowerPoint.Application")
pres = app.Presentations.Open(str(deck), ReadOnly=True, WithWindow=False)
try:
    for i in (want or range(1, pres.Slides.Count + 1)):
        pres.Slides(i).Export(str(out / f"s{i:02d}.png"), "PNG", 1280, 720)
        print("exported", i)
finally:
    pres.Close()
