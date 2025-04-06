# # workflows/report_generator.py

# # def format_analysis_report(analysis: dict) -> str:
# #     """
# #     Formats the analysis dictionary into a readable multi-section report.
# #     Ideal for displaying inside Streamlit or exporting to PDF.
# #     """
# #     report = ""

# #     for section, content in analysis.items():
# #         report += f"### 🧾 {section}\n\n"
# #         report += content + "\n\n"
# #         report += "---\n\n"

# #     return report
# import streamlit as st

# def format_analysis_report(analysis: dict):
#     """
#     Displays each section of the analysis dictionary in a separate Streamlit tab.
#     """
#     if not analysis:
#         st.warning("No analysis data to display.")
#         return

#     tab_titles = [f"🧾 {section}" for section in analysis.keys()]
    
#     tabs = st.tabs(tab_titles)

#     for tab, (section, content) in zip(tabs, analysis.items()):
#         with tab:
#             st.markdown(f"### {section}")
#             st.markdown(content)
# report_generator.py

import streamlit as st

def format_analysis_report(analysis: dict):
    """
    Displays each section of the analysis dictionary in a separate Streamlit tab.
    Ensures the 'Executive Summary' always appears first if present.
    """
    if not analysis:
        st.warning("No analysis data to display.")
        return

    # Move Executive Summary to first tab if it exists
    sections = list(analysis.keys())
    if "Executive Summary" in sections:
        sections.remove("Executive Summary")
        sections.insert(0, "Executive Summary")

    # Create tabs
    tab_titles = [f"🧾 {section}" for section in sections]
    tabs = st.tabs(tab_titles)

    for tab, section in zip(tabs, sections):
        with tab:
            st.markdown(f"### {section}")
            st.markdown(analysis[section])


# import streamlit as st
# from fpdf import FPDF
# from io import BytesIO

# def format_analysis_report(analysis: dict):
#     """
#     Displays each section of the analysis dictionary in a separate Streamlit tab.
#     Ensures the 'Executive Summary' always appears first if present.
#     Also provides a download button to save the report as a PDF.
#     """
#     if not analysis:
#         st.warning("No analysis data to display.")
#         return

#     # Move Executive Summary to first tab if it exists
#     sections = list(analysis.keys())
#     if "Executive Summary" in sections:
#         sections.remove("Executive Summary")
#         sections.insert(0, "Executive Summary")

#     # Create tabs
#     tab_titles = [f"🧾 {section}" for section in sections]
#     tabs = st.tabs(tab_titles)

#     for tab, section in zip(tabs, sections):
#         with tab:
#             st.markdown(f"### {section}")
#             st.markdown(analysis[section])

#     # PDF Generation Logic
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     for section in sections:
#         content = analysis.get(section, "")
#         if not isinstance(content, str):
#             content = str(content)

#         # Add section title
#         pdf.set_font("Arial", 'B', 14)
#         pdf.multi_cell(0, 10, section)
#         pdf.ln(2)

#         # Add content
#         pdf.set_font("Arial", size=12)
#         for line in content.split('\n'):
#             pdf.multi_cell(0, 10, line)
#         pdf.ln(5)

#     # Create PDF file in memory
#     pdf_buffer = BytesIO()
#     pdf.output(pdf_buffer)
#     pdf_buffer.seek(0)

#     # Show download button
#     st.download_button(
#         label="📥 Download Full Report as PDF",
#         data=pdf_buffer,
#         file_name="RFP_Analysis_Report.pdf",
#         mime="application/pdf"
#     )
