"""Minimal xlsx reader (zip+xml; openpyxl fails on these files' styles).
usage: py -I xlsx_raw.py <file.xlsx> [sheet name] [max rows]   -> no sheet: list sheets with dims
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def col(ref: str) -> int:
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group():
        n = n * 26 + ord(ch) - 64
    return n - 1


class Book:
    def __init__(self, path):
        self.z = zipfile.ZipFile(path)
        wb = ET.fromstring(self.z.read("xl/workbook.xml"))
        rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(self.z.read("xl/_rels/workbook.xml.rels"))}
        self.sheets = {s.get("name"): "xl/" + rels[s.get(f"{{{NS['r']}}}id")].lstrip("/").replace("xl/", "")
                       for s in wb.find("m:sheets", NS)}
        self.ss = []
        if "xl/sharedStrings.xml" in self.z.namelist():
            for si in ET.fromstring(self.z.read("xl/sharedStrings.xml")):
                self.ss.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))

    def rows(self, name):
        for ev, row in ET.iterparse(self.z.open(self.sheets[name]), events=("end",)):
            if row.tag != f"{{{NS['m']}}}row":
                continue
            out = []
            for c in row:
                i = col(c.get("r")) if c.get("r") else len(out)
                out += [""] * (i + 1 - len(out))
                v = c.find("m:v", NS)
                if c.get("t") == "s" and v is not None:
                    out[i] = self.ss[int(v.text)]
                elif c.get("t") == "inlineStr":
                    out[i] = "".join(t.text or "" for t in c.iter(f"{{{NS['m']}}}t"))
                elif v is not None:
                    out[i] = v.text
            row.clear()
            yield out


if __name__ == "__main__":
    b = Book(sys.argv[1])
    if len(sys.argv) == 2:
        for n in b.sheets:
            rs = list(b.rows(n))
            print(f"{n!r}: {len(rs)} rows; header={rs[0][:14] if rs else None}")
    else:
        for i, r in enumerate(b.rows(sys.argv[2])):
            if i >= int(sys.argv[3] if len(sys.argv) > 3 else 5):
                break
            print(r)
