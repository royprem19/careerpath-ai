import pymupdf
import docx
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"Error parsing PDF: {e}")
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    text = ""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
    return text

def parse_resume(file_bytes: bytes, filename: str) -> str:
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif ext in ["doc", "docx"]:
        return extract_text_from_docx(file_bytes)
    elif ext == "txt":
        return file_bytes.decode('utf-8', errors='ignore')
    else:
        return extract_text_from_pdf(file_bytes)
