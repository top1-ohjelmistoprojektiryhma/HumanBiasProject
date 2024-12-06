import unittest
from unittest.mock import MagicMock, patch
import backend.services.file_reader as file_reader


class TestFileReader(unittest.TestCase):
    def test_read_txt_file(self):
        mock_file = MagicMock()
        mock_file.filename = "test.txt"
        mock_file.read.return_value = b"Hello, this is a text file."

        result = file_reader.read_file(mock_file)
        self.assertEqual(result, "Hello, this is a text file.")

    def test_read_pdf_file(self):
        mock_file = MagicMock()
        mock_file.filename = "test.pdf"

        # Mock pdfplumber behavior
        with patch("pdfplumber.open") as mock_pdfplumber_open:
            mock_pdf = MagicMock()
            mock_pdf.pages = [MagicMock(extract_text=lambda: "Page 1 content"), MagicMock(extract_text=lambda: "Page 2 content")]
            mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf

            result = file_reader.read_file(mock_file)
            self.assertEqual(result, "Page 1 content\nPage 2 content\n")

    def test_read_docx_file(self):
        mock_file = MagicMock()
        mock_file.filename = "test.docx"

        # Mock docx.Document behavior
        with patch("docx.Document") as mock_docx_document:
            mock_doc = MagicMock()
            mock_doc.paragraphs = [MagicMock(text="Paragraph 1"), MagicMock(text="Paragraph 2")]
            mock_docx_document.return_value = mock_doc

            result = file_reader.read_file(mock_file)
            self.assertEqual(result, "Paragraph 1\nParagraph 2\n")

    def test_read_odt_file(self):
        mock_file = MagicMock()
        mock_file.filename = "test.odt"

        # Mock odf.opendocument.load behavior
        with patch("backend.services.file_reader.load") as mock_load:
            mock_odt_document = MagicMock()
            mock_paragraph = MagicMock(firstChild=MagicMock(data="ODT Paragraph"))
            mock_odt_document.getElementsByType.return_value = [mock_paragraph]
            mock_load.return_value = mock_odt_document

            result = file_reader.read_file(mock_file)
            self.assertEqual(result, "ODT Paragraph\n")

    def test_invalid_file(self):
        mock_file = MagicMock()
        mock_file.filename = "unsupported.xyz"
        result = file_reader.read_file(mock_file)
        self.assertIsNone(result)

    def test_file_reading_error(self):
        mock_file = MagicMock()
        mock_file.filename = "test.txt"
        mock_file.read.side_effect = Exception("File reading error")

        result = file_reader.read_file(mock_file)
        self.assertIsNone(result)
