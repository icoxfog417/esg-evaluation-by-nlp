import os
import time
from functools import wraps, partial
import unicodedata
import docker
import requests
import tika
import pandas as pd
from bs4 import BeautifulSoup
from tika import parser


def unset_proxy(func):

    @wraps(func)
    def _unset_proxy(*args, **kwargs):
        encoding = os.getenv("PYTHONIOENCODING", "")
        http_proxy = os.getenv("HTTP_PROXY", "")
        https_proxy = os.getenv("HTTPS_PROXY", "")

        os.environ["PYTHONIOENCODING"] = "utf8"
        os.environ["HTTP_PROXY"] = ""
        os.environ["HTTPS_PROXY"] = ""

        result = func(*args, **kwargs)

        os.environ["PYTHONIOENCODING"] = encoding
        os.environ["HTTP_PROXY"] = http_proxy
        os.environ["HTTPS_PROXY"] = https_proxy
        return result

    return _unset_proxy


def wait_docker_up(host, interval):

    def _wait_docker_up(_host, _interval, func):

        @wraps(func)
        def __wait_docker_up(*args, **kwargs):
            result = func(*args, **kwargs)
            is_up = False
            while not is_up:
                try:
                    resp = requests.get(_host,
                                        proxies={
                                            "http": None,
                                            "https": None
                                        })
                    if resp.ok:
                        is_up = True
                except Exception as ex:
                    pass
                time.sleep(_interval)

            return result

        return __wait_docker_up

    return partial(partial(_wait_docker_up, host), interval)


class PDFReader():
    _CONTAINER = None

    @wait_docker_up(host="http://localhost:9998", interval=1)
    def __init__(self):
        self.client = docker.from_env()
        if PDFReader._CONTAINER is None:
            PDFReader._CONTAINER = self.client.containers.run(
                "logicalspark/docker-tikaserver:latest",
                ports={"9998/tcp": "9998"},
                remove=True, detach=True)

    @unset_proxy
    def read(self, path, xml_content=False):
        parsed = parser.from_file(path, xmlContent=xml_content)
        return Content(parsed)

    def normalize(self, text):
        if text is None:
            return ""
        _text = text.replace("\r", "").replace("\n", " ")
        _text = _text.strip()
        _text = unicodedata.normalize("NFKC", _text)
        return _text

    @unset_proxy
    def read_to_frame(self, path):
        parsed = parser.from_file(path, xmlContent=True)
        xml = BeautifulSoup(parsed["content"], "lxml-xml")
        body = xml.find("body")
        items = []
        for p, page in enumerate(body.find_all("div")):
            page_index = p + 1
            for c, content in enumerate(page.find_all("p")):
                content_index = c + 1
                item = {
                    "page": page_index,
                    "order": content_index,
                    "content": content.text.strip()
                }
                items.append(item)

        df = pd.DataFrame(items)
        return df

    def preprocess_frame(self, df):
        prefixes = []
        suffixes = []
        preprocessed = []
        magic_number = 10

        for i, row in df.iterrows():
            content = self.normalize(row["content"])
            if len(content) < magic_number:
                continue
            else:
                length = int(magic_number / 2)
                prefix = content[:length]
                suffix = content[-length:]
                if prefix in prefixes:
                    continue
                else:
                    prefixes.append(prefix)

                if suffix in suffixes:
                    continue
                else:
                    suffixes.append(suffix)

                item = {}
                for c in df.columns:
                    item[c] = row[c]
                    if c == "content":
                        item[c] = content

                preprocessed.append(item)

        df = pd.DataFrame(preprocessed)
        return df

    @classmethod
    def stop(cls):
        if cls._CONTAINER:
            cls._CONTAINER.stop()


class Content():

    def __init__(self, parsed):
        self._parsed = parsed

    @property
    def metadata(self):
        return self._parsed["metadata"]

    @property
    def content(self):
        return self._parsed["content"]
