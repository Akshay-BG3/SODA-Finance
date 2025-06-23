from fpdf import FPDF
import re
import os


# Remove emojis and unsupported characters
def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def generate_pdf(summary_text, ai_text, memory_text=None, file_path="SODA_Report.pdf"):
    try:
        pdf = FPDF()
        pdf.add_page()

        # Load Unicode Font
        font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
        if not os.path.exists(font_path):
            raise FileNotFoundError("TTF Font file not found: DejaVuSans.ttf")

        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", "", 12)

        # Clean input text
        summary_text = remove_emojis(str(summary_text or "No summary available."))
        ai_text = remove_emojis(str(ai_text or "No AI insights available."))
        memory_text = remove_emojis(str(memory_text or "No memory insights available."))

        # Add content
        pdf.cell(0, 10, "📊 Summary", ln=True)
        pdf.multi_cell(0, 10, summary_text)

        pdf.cell(0, 10, "🤖 AI Report", ln=True)
        pdf.multi_cell(0, 10, ai_text)

        pdf.cell(0, 10, "🧠 Memory Insight", ln=True)
        pdf.multi_cell(0, 10, memory_text)

        # Output PDF to memory (byte stream)
        return bytes(pdf.output(dest='S'))



    except Exception as e:
        raise RuntimeError("PDF generation failed: " + str(e))
