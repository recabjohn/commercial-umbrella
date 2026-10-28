"""Export the 5 FRC sheets (Page, Page Fields, Domain Tables/Keys/Entries) with ALL columns to CSV.
usage: py -I frc_sheets_full.py <FRC xlsx> <tag> <out dir>
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from xlsx_raw import Book  # noqa: E402

SHEETS = {"Page": "page", "Page Fields": "fields", "Domain Tables": "domains", "Domain Table Keys": "domainkeys",
          "Domain Table Entries": "entries"}
HEAD = {"Page": "Name", "Page Fields": "Page", "Domain Tables": "Table", "Domain Table Keys": "Domain Table", "Domain Table Entries": None}

book, tag, out = Book(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
for sheet, short in SHEETS.items():
    rows = [r for r in book.rows(sheet)]
    if sheet == "Domain Table Entries":
        header, body = ["Table", "Sequence", "DisplayValue", "DataValue", "Status"], [r[7:12] for r in rows[3:] if len(r) > 7 and r[7]]
    else:
        hi = next(i for i, r in enumerate(rows) if len(r) > 6 and r[6] == HEAD[sheet])
        header = rows[hi][6:]
        body = [r[6:] for r in rows[hi + 1:] if len(r) > 6 and r[6]]
    with open(out / f"{tag}_{short}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows([c or "" for c in r] + [""] * (len(header) - len(r)) for r in body)
    print(sheet, len(body), "rows,", len(header), "cols")
