# services/document_processor.py

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts and concatenates text from all pages of a PDF.
    """
    try:
        text = ""
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"❌ PDF Extraction Error: {str(e)}"


def clean_text(text: str) -> str:
    """
    Optional: Preprocess the extracted text (remove junk, normalize whitespace, etc.)
    """
    cleaned = text.replace("\n", " ").replace("\r", " ")
    cleaned = " ".join(cleaned.split())  # Collapse whitespace
    return cleaned

from docx import Document

def extract_text_from_docx(docx_file) -> str:
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])
