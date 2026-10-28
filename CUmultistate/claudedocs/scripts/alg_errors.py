"""Extract validation rules (name, condition tokens, message) from ALG human-readable Err-* / ErrorMessages sheets.
usage: py -I alg_errors.py <ALG_HR.xlsx> <out.json>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from xlsx_raw import Book  # noqa: E402

book, out = Book(sys.argv[1]), Path(sys.argv[2])
res = {}
for sheet in book.sheets:
    if not (sheet.startswith("Err-") or sheet == "ErrorMessages"):
        continue
    rules, cur = [], None
    for r in book.rows(sheet):
        r += [""] * (8 - len(r))
        tag = r[0]
        if tag == "PCH":
            cur = {"rule": r[4], "cond": [], "msg": ""}
            rules.append(cur)
        elif cur is not None and tag in ("IFM", "IFB"):
            cur["cond"].append(" ".join(x for x in (r[3], r[4]) if x))
        elif cur is not None and tag == "CVE" and r[4].startswith('"'):
            cur["msg"] = r[4].strip('"')
    res[sheet] = rules
out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
print({k: len(v) for k, v in res.items()})
