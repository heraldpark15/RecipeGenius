from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(recipe_text):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize = letter)
    pdf.setFont("Helvetica", 12)

    y_position = 750
    for line in recipe_text.split("\n"):
        pdf.drawString(50, y_position, line)
        y_position -= 20

    pdf.save()
    buffer.seek(0)
    return buffer