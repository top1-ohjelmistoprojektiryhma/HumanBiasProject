from pypdf import PdfReader
import docx
from odf.opendocument import load
from odf.text import P


def read_file(file):
    print("reading file in backend")
    try:
        if file and file.filename.endswith(".txt"):
            file_content = file.read().decode("utf-8")
            return file_content
        if file and file.filename.endswith(".pdf"):
            return read_pdf(file)
        if file and file.filename.endswith(".docx"):
            return read_docx(file)
        if file and file.filename.endswith(".odt"):
            return read_odt(file)
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def read_pdf(file):
    pdf_reader = PdfReader(file)
    page = pdf_reader.pages[0]
    text = page.extract_text()
    return text


def read_docx(file):
    doc = docx.Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def read_odt(file):
    odt_document = load(file)
    text = ""
    for paragraph in odt_document.getElementsByType(P):
        text += paragraph.firstChild.data + "\n"
    return text