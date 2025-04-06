# # pdf_generator.py
# from fpdf import FPDF
# import tempfile

# def generate_rfp_pdf(analysis: dict) -> str:
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.set_font("Arial", size=12)

#     for section, content in analysis.items():
#         pdf.set_font("Arial", 'B', 14)
#         pdf.multi_cell(0, 10, f"{section}", align='L')
#         pdf.set_font("Arial", size=11)
#         pdf.multi_cell(0, 8, content.strip())
#         pdf.ln(4)

#     tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
#     pdf.output(tmp_path)
#     return tmp_path
