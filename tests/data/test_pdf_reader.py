import os
import unittest
from chariot.storage import Storage
from evaluator.data.pdf_reader import PDFReader


class TestPDFReader(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        PDFReader.stop()

    def xtest_read_pdf_text(self):
        path = os.path.join(os.path.dirname(__file__), "../_data")
        storage = Storage(path)
        url = "https://global.toyota/pages/global_toyota/ir/library/annual/2019_001_annual_jp.pdf"
        file_path = storage.download(url, "./test_pdf.pdf")
        reader = PDFReader()
        content = reader.read(file_path)
        self.assertTrue(content.metadata)
        self.assertTrue(content.content)
        self.assertEqual(content.metadata["Author"],
                         "TOYOTA MOTOR CORPORATION")
        self.assertTrue("アニュアルレポート2019", content.content[:200])
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
