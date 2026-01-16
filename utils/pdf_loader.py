import pdfplumber
import io

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    text_blocks = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_blocks.append(text)
    return "\n\n".join(text_blocks)
