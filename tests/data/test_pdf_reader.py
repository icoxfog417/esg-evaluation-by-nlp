import os
import unittest
import requests
import pytest
from evaluator.data.pdf_reader import PDFReader


class TestPDFReader(unittest.TestCase):
    PATH = os.path.join(os.path.dirname(__file__), "../_data/test_pdf.pdf")

    @classmethod
    def setUpClass(cls):
        url = "https://global.toyota/pages/global_toyota/ir/library/annual/2019_001_annual_jp.pdf"
        r = requests.get(url)
        if r.ok:
            with open(cls.PATH, mode="wb") as f:
                f.write(r.content)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.PATH)

    def test_read_pdf_text(self):
        reader = PDFReader()
        text = reader.read(self.PATH, html=True)
        self.assertEqual(text[:6], "<html>")
        text = reader.read(self.PATH)
        self.assertTrue("目次" in text[:6])

    def test_read_pdf_as_frame(self):
        reader = PDFReader()
        df = reader.read_to_frame(self.PATH)
        self.assertGreater(len(df), 1)

        df = reader.preprocess_frame(df)
        df.to_csv("sample.csv", index=False)
        self.assertGreater(len(df), 1)
        os.remove("sample.csv")

    def test_to_documents(self):
        reader = PDFReader()
        documents = reader.read_as_documents(self.PATH, 1, 2018, lang="ja")
        self.assertTrue(len(documents) > 0)
