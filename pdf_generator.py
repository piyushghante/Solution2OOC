# from weasyprint import HTML

# def generate_pdf_from_analysis(analysis: dict, output_path: str = "rfp_report.pdf"):
#     html = f"""
#     <html>
#     <head>
#         <style>
#             body {{ font-family: Arial, sans-serif; padding: 20px; }}
#             h1 {{ color: #333; }}
#             h2 {{ color: #0055a5; border-bottom: 1px solid #ddd; }}
#             pre {{ background: #f5f5f5; padding: 10px; white-space: pre-wrap; }}
#         </style>
#     </head>
#     <body>
#         <h1>📄 RFP Analysis Report</h1>

#         <h2>✅ Eligibility Verdict</h2>
#         <p><strong>{analysis.get("Eligibility Verdict", "N/A")}</strong></p>

#         <h2>🧠 Executive Summary</h2>
#         <p>{analysis.get("Executive Summary", "N/A")}</p>

#         <h2>📋 Submission Checklist</h2>
#         <pre>{analysis.get("Submission Checklist", "N/A")}</pre>

#         <h2>⚠️ Contract Risks</h2>
#         <pre>{analysis.get("Contract Risks", "N/A")}</pre>

#         <h2>🔍 Full Gemini Verdict Response</h2>
#         <pre>{analysis.get("Verdict Full Response", "N/A")}</pre>
#     </body>
#     </html>
#     """

#     HTML(string=html).write_pdf(output_path)
#     return output_path
