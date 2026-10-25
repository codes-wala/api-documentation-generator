from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, HRFlowable


def markdown_to_pdf(title: str, markdown_text: str) -> bytes:
    """Render a conservative Markdown subset into a standalone PDF."""
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4, rightMargin=19*mm, leftMargin=19*mm, topMargin=18*mm, bottomMargin=18*mm, title=title, author="API Documentation Generator")
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("DocTitle", parent=base["Title"], fontName="Helvetica-Bold", fontSize=22, leading=27, alignment=TA_LEFT, textColor=colors.HexColor("#202733"), spaceAfter=14),
        "h1": ParagraphStyle("DocH1", parent=base["Heading1"], fontSize=18, leading=23, textColor=colors.HexColor("#202733"), spaceBefore=14, spaceAfter=8, keepWithNext=True),
        "h2": ParagraphStyle("DocH2", parent=base["Heading2"], fontSize=14, leading=18, textColor=colors.HexColor("#29364a"), spaceBefore=12, spaceAfter=6, keepWithNext=True),
        "h3": ParagraphStyle("DocH3", parent=base["Heading3"], fontSize=11, leading=15, textColor=colors.HexColor("#29364a"), spaceBefore=9, spaceAfter=5, keepWithNext=True),
        "body": ParagraphStyle("DocBody", parent=base["BodyText"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=colors.HexColor("#303846"), spaceAfter=6, splitLongWords=1),
        "bullet": ParagraphStyle("DocBullet", parent=base["BodyText"], fontName="Helvetica", fontSize=9.5, leading=14, leftIndent=14, firstLineIndent=-8, spaceAfter=3),
        "code": ParagraphStyle("DocCode", fontName="Courier", fontSize=7.5, leading=10, backColor=colors.HexColor("#f3f5f8"), borderColor=colors.HexColor("#e0e4eb"), borderWidth=.5, borderPadding=7, leftIndent=5, rightIndent=5, spaceBefore=4, spaceAfter=8),
        "quote": ParagraphStyle("DocQuote", parent=base["BodyText"], fontName="Helvetica-Oblique", fontSize=9, leading=13, leftIndent=12, textColor=colors.HexColor("#5c6675"), spaceAfter=7),
    }
    story = [Paragraph(escape(title), styles["title"]), HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#d9dee7"), spaceAfter=12)]
    in_code = False
    code_lines = []
    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True; code_lines = []
            else:
                story.append(Preformatted("\n".join(code_lines), styles["code"], maxLineLength=105))
                in_code = False; code_lines = []
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            story.append(Spacer(1, 3))
        elif line.strip() in {"---", "***", "___"}:
            story.append(HRFlowable(width="100%", thickness=.4, color=colors.HexColor("#d9dee7"), spaceBefore=4, spaceAfter=8))
        elif line.startswith("### "):
            story.append(Paragraph(inline_format(line[4:]), styles["h3"]))
        elif line.startswith("## "):
            story.append(Paragraph(inline_format(line[3:]), styles["h2"]))
        elif line.startswith("# "):
            story.append(Paragraph(inline_format(line[2:]), styles["h1"]))
        elif line.lstrip().startswith(("- ", "* ", "+ ")):
            story.append(Paragraph("• " + inline_format(line.lstrip()[2:]), styles["bullet"]))
        elif line.lstrip()[:1].isdigit() and ". " in line.lstrip()[:5]:
            story.append(Paragraph(inline_format(line.strip()), styles["bullet"]))
        elif line.startswith("> "):
            story.append(Paragraph(inline_format(line[2:]), styles["quote"]))
        else:
            # Basic inline formatting; all content is escaped before markup is introduced.
            story.append(Paragraph(inline_format(line), styles["body"]))
    if in_code and code_lines:
        story.append(Preformatted("\n".join(code_lines), styles["code"], maxLineLength=105))
    def footer(canvas, pdf_doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#e0e4eb")); canvas.line(19*mm, 13*mm, A4[0]-19*mm, 13*mm)
        canvas.setFont("Helvetica", 8); canvas.setFillColor(colors.HexColor("#7a8493"))
        canvas.drawString(19*mm, 8*mm, "Generated with API Documentation Generator")
        canvas.drawRightString(A4[0]-19*mm, 8*mm, f"Page {pdf_doc.page}")
        canvas.restoreState()
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return output.getvalue()


def inline_format(value: str) -> str:
    text = escape(value)
    # Small, intentionally limited Markdown inline subset. HTML remains escaped.
    import re
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", r"\1 (&lt;\2&gt;)", text)
    return text
