import unicodedata
from io import StringIO
from pdfminer.high_level import extract_text, extract_text_to_fp
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter, TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd


class PDFReader():

    def __init__(self):
        pass

    def read(self, path, html=False):
        text = StringIO()
        if html:
            with open(path, "rb") as f:
                extract_text_to_fp(f, text, laparams=LAParams(),
                                   output_type="html", codec=None)
            text = text.getvalue()
        else:
            text = extract_text(path)
        return text

    def read_pages(self, path, html=False,
                   laparams=None, maxpages=0, page_numbers=None,
                   password="", scale=1.0, rotation=0, layoutmode='normal',
                   output_dir=None, strip_control=False, debug=False,
                   disable_caching=False, **kwargs):

        rsrcmgr = PDFResourceManager(caching=True)
        pages = []
        with open(path, "rb") as f:
            for page in PDFPage.get_pages(f, None, maxpages=0,
                                          check_extractable=True):
                page.rotate = (page.rotate + rotation) % 360
                text = StringIO()
                if html:
                    device = HTMLConverter(rsrcmgr, text, codec=None, scale=scale,
                                           layoutmode=layoutmode, laparams=laparams)
                else:
                    device = TextConverter(rsrcmgr, text, codec=None, laparams=laparams)

                interpreter = PDFPageInterpreter(rsrcmgr, device)
                interpreter.process_page(page)
                pages.append(text.getvalue())
                device.close()

        return pages

    def read_to_frame(self, path):
        items = []
        pages = self.read_pages(path, html=True)
        page_index = 0
        for i, p in enumerate(pages):
            p = p.replace("<br>", "\n").replace("<br/>", "\n")
            html = BeautifulSoup(p, "html.parser")
            if not html:
                continue
            page = html.get_text("\n")
            contents = page.split("\n\n")
            content_index = 0
            for j, s in enumerate(contents):
                c = s.strip()
                if not c:
                    continue

                item = {
                    "page": page_index,
                    "order": content_index,
                    "content": c
                }
                items.append(item)
                content_index += 1

            page_index += 1

        df = pd.DataFrame(items)
        return df

    def normalize(self, text):
        if text is None:
            return ""
        _text = text.replace("\r", "").replace("\n", "").strip()
        _text = unicodedata.normalize("NFKC", _text)
        return _text

    def preprocess_frame(self, df, lower=True):
        repeat_check = []
        preprocessed = []

        for i, row in df.iterrows():
            content = self.normalize(row["content"])
            if lower:
                content = content.lower()
            if content in repeat_check:
                continue
            repeat_check.append(content)

            item = {}
            for c in df.columns:
                item[c] = row[c]
                if c == "content":
                    item[c] = content

            preprocessed.append(item)

        df = pd.DataFrame(preprocessed)
        return df
