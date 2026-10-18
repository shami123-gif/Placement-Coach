from pypdf import PdfReader
from io import BytesIO

from reportlab.lib.pagesizes import A4


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from a PDF uploaded through Streamlit.
    """

    try:
        pdf_bytes = uploaded_file.getvalue()

        reader = PdfReader(BytesIO(pdf_bytes))

        pages_text = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages_text.append(text)

        full_text = "\n".join(pages_text).strip()

        if not full_text:
            return "No readable text was found in this PDF."

        return full_text

    except Exception as e:
        raise RuntimeError(
            f"Could not read the PDF file: {e}"
        )

    from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from io import BytesIO
import re


def create_pdf_report(title: str, content: str):
    """
    Create a downloadable PDF report from AI-generated Markdown text.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#1f3c88")

    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    story.append(
        Paragraph(title, title_style)
    )

    story.append(Spacer(1, 20))

    for line in content.splitlines():

        line = line.strip()

        if not line:
            story.append(Spacer(1, 8))
            continue

        # Main heading
        if line.startswith("# "):

            text = line[2:].strip()

            story.append(
                Paragraph(
                    text,
                    styles["Heading1"]
                )
            )

        # Section heading
        elif line.startswith("## "):

            text = line[3:].strip()

            story.append(
                Paragraph(
                    text,
                    heading_style
                )
            )

            story.append(Spacer(1, 6))

        # Bullet point
        elif line.startswith("- "):

            text = line[2:].strip()

            story.append(
                Paragraph(
                    f"• {text}",
                    body_style
                )
            )

        # Numbered list
        elif re.match(r"^\d+\.\s", line):

            story.append(
                Paragraph(
                    line,
                    body_style
                )
            )

        # Normal text
        else:

            story.append(
                Paragraph(
                    line,
                    body_style
                )
            )

        story.append(Spacer(1, 5))

    document.build(story)

    buffer.seek(0)

    return buffer