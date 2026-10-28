"""Write preview_seeded.html: the built Program Selection page with a sample CU policy already in sessionStorage. usage: py -I make_preview.py"""
from pathlib import Path

d = Path(__file__).resolve().parent
seed = ("<script>sessionStorage.setItem('cuRisk',JSON.stringify([{state:'IL',form:'Commercial Umbrella Liability',"
        "limit:'5000000',sir:'10000',underlying:'3 saved'}]))</script>")
s = (d / "cu_program_screen.html").read_text("utf-8")
(d / "preview_seeded.html").write_text(s.replace("<head>", "<head>" + seed, 1), "utf-8")
print("wrote preview_seeded.html")
