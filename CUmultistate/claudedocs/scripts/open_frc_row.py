"""Open the FRC workbook in Excel (read-only), go to the Page Fields sheet and select a field's row.
usage: py -I open_frc_row.py <FRC xlsx> <field name>
"""
import sys
from pathlib import Path

import win32com.client

path, field = str(Path(sys.argv[1]).resolve()), sys.argv[2]
xl = win32com.client.Dispatch("Excel.Application")
xl.Visible = True
wb = xl.Workbooks.Open(path, ReadOnly=True)
ws = wb.Worksheets("Page Fields")
ws.Activate()
hit = ws.UsedRange.Find(What=field, LookAt=1)          # xlWhole
assert hit is not None, f"{field} not found on Page Fields"
row = hit.Row
ws.Rows(row).Select()
xl.ActiveWindow.ScrollRow = max(1, row - 3)
xl.ActiveWindow.ScrollColumn = 1
print("opened", path, "sheet Page Fields, row", row)
