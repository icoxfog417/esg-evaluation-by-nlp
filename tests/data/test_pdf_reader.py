import os
import unittest
from chariot.storage import Storage
from evaluator.data.pdf_reader import PDFReader


class TestPDFReader(unittest.TestCase):

    def test_read_pdf_text(self):
        path = os.path.join(os.path.dirname(__file__), "../_data")
        storage = Storage(path)
        url = "https://global.toyota/pages/global_toyota/ir/library/annual/2019_001_annual_jp.pdf"
        file_path = storage.download(url, "./test_pdf.pdf")
        reader = PDFReader()
        text = reader.read(file_path, html=True)
        self.assertEqual(text[:6], "<html>")

        text = reader.read(file_path)
        self.assertTrue("目次" in text[:6])
        os.remove(file_path)

    def test_read_pdf_as_frame(self):
        path = os.path.join(os.path.dirname(__file__), "../_data")
        storage = Storage(path)
        url = "https://global.toyota/pages/global_toyota/ir/library/annual/2019_001_annual_jp.pdf"
        file_path = storage.download(url, "./test_pdf.pdf")
        reader = PDFReader()
        df = reader.read_to_frame(file_path)
        self.assertGreater(len(df), 1)
        os.remove(file_path)

    def test_preprocess(self):
        path = os.path.join(os.path.dirname(__file__), "../_data")
        storage = Storage(path)
        url = "https://global.toyota/pages/global_toyota/ir/library/annual/2019_001_annual_en.pdf"
        file_path = storage.download(url, "./test_pdf_preprocess.pdf")
        reader = PDFReader()
        df = reader.read_to_frame(file_path)
        df = reader.preprocess_frame(df)
        df.to_csv("sample.csv", index=False)
        self.assertGreater(len(df), 1)
        os.remove(file_path)
