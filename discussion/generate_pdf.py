from pathlib import Path
from fpdf import FPDF
import re

md = Path("/workspace/solar-system-planets/discussion/DISCUSSION.md").read_text()

header_match = re.search(
    r"# (.+)\n\n\*\*Module:\*\* (.+)\n\*\*Assignment:\*\* (.+)\n\*\*Student:\*\* (.+)\n",
    md,
)
title = header_match.group(1)
module = header_match.group(2)
assignment = header_match.group(3)
student = header_match.group(4)

body_m = re.search(r"## Discussion\n\n(.*)\n\n---\n\n## References\n\n(.*)\Z", md, re.S)
body = body_m.group(1).strip()
refs = body_m.group(2).strip()

WORD_COUNT = len(body.split())


class PDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")


pdf = PDF(format="A4")
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.set_margins(18, 16, 18)
pdf.add_page()

pdf.set_font("Helvetica", "B", 11)
pdf.multi_cell(0, 6, "Sheffield Hallam University")
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "", 10)
pdf.multi_cell(0, 5, f"Module: {module}")
pdf.set_x(pdf.l_margin)
pdf.multi_cell(0, 5, f"Assignment: {assignment}")
pdf.set_x(pdf.l_margin)
pdf.multi_cell(0, 5, f"Student: {student}")
pdf.set_x(pdf.l_margin)
pdf.ln(2)
pdf.set_draw_color(40, 40, 40)
y = pdf.get_y()
pdf.line(18, y, 192, y)
pdf.set_y(y + 4)
pdf.set_x(pdf.l_margin)

pdf.set_font("Helvetica", "B", 13)
pdf.multi_cell(0, 7, title)
pdf.set_x(pdf.l_margin)
pdf.ln(2)


def sanitize(s: str) -> str:
    return (
        s.replace("\u2014", "--")
        .replace("\u2013", "-")
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2026", "...")
        .replace("\u00e7", "c")  # unlikely
    )


def write_prose(pdf_obj, text):
    parts = re.split(r"(`[^`]+`)", text)
    line_h = 5.2
    pdf_obj.set_x(pdf_obj.l_margin)
    pdf_obj.set_font("Times", "", 11)
    for part in parts:
        if not part:
            continue
        if part.startswith("`") and part.endswith("`"):
            pdf_obj.set_font("Courier", "", 9)
            pdf_obj.write(line_h, sanitize(part[1:-1]))
            pdf_obj.set_font("Times", "", 11)
        else:
            pdf_obj.write(line_h, sanitize(part))
    pdf_obj.ln(line_h + 1)


def write_code_block(pdf_obj, code):
    pdf_obj.ln(1)
    x = pdf_obj.l_margin
    y = pdf_obj.get_y()
    usable = pdf_obj.w - pdf_obj.l_margin - pdf_obj.r_margin
    pdf_obj.set_font("Courier", "", 8)
    lines = code.strip("\n").split("\n")
    line_h = 3.8
    block_h = line_h * len(lines) + 4
    if y + block_h > pdf_obj.h - pdf_obj.b_margin:
        pdf_obj.add_page()
        y = pdf_obj.get_y()
    pdf_obj.set_fill_color(245, 245, 245)
    pdf_obj.set_draw_color(200, 200, 200)
    pdf_obj.rect(x, y, usable, block_h, style="DF")
    pdf_obj.set_xy(x + 2, y + 2)
    for line in lines:
        safe = sanitize(line.replace("\t", "    "))
        safe = safe.encode("latin-1", "replace").decode("latin-1")
        pdf_obj.set_x(x + 2)
        pdf_obj.cell(usable - 4, line_h, safe, new_x="LMARGIN", new_y="NEXT")
    pdf_obj.set_y(y + block_h + 2)
    pdf_obj.set_font("Times", "", 11)


segments = re.split(r"(```python\n.*?```)", body, flags=re.S)
for seg in segments:
    if seg.startswith("```python"):
        code = re.sub(r"^```python\n|```$", "", seg, flags=re.S)
        write_code_block(pdf, code)
    else:
        paras = re.split(r"\n\n+", seg.strip()) if seg.strip() else []
        for p in paras:
            p = " ".join(line.strip() for line in p.splitlines())
            if p:
                write_prose(pdf, p)
                pdf.ln(1.5)

pdf.ln(2)
pdf.set_draw_color(40, 40, 40)
y = pdf.get_y()
pdf.line(18, y, 192, y)
pdf.set_y(y + 4)
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 6, "References", new_x="LMARGIN", new_y="NEXT")
pdf.set_x(pdf.l_margin)
pdf.ln(2)

for ref_line in refs.split("\n\n"):
    ref_line = ref_line.strip()
    if not ref_line:
        continue
    clean = sanitize(ref_line.replace("*", ""))
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Times", "", 10)
    pdf.multi_cell(0, 5, clean)
    pdf.set_x(pdf.l_margin)
    pdf.ln(1.5)

out1 = Path("/workspace/solar-system-planets/discussion/OOP_Discussion_Irfan_Asrar.pdf")
out2 = Path("/workspace/OOP_Discussion_Irfan_Asrar.pdf")
pdf.output(str(out1))
pdf.output(str(out2))
print("Wrote", out1, "size", out1.stat().st_size)
print("Wrote", out2, "size", out2.stat().st_size)
print("WORD_COUNT", WORD_COUNT)
