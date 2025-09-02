from pypdf import PdfReader
from io import BytesIO

def pdf_loader(uploaded_file) -> str:
    """
    Extracts text from a Streamlit UploadedFile (PDF).
    """
    text = []
    # UploadedFile is a SpooledTemporaryFile; wrap bytes for PdfReader
    reader = PdfReader(BytesIO(uploaded_file.read()))
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text:
            text.append(page_text)
    return "\n".join(text).strip()
