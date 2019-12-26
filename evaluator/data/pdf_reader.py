import os
import tika
from tika import parser
from chariot.storage import Storage


os.environ["PYTHONIOENCODING"] = "utf8"
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

storage = Storage(os.path.join(os.path.dirname(__file__), "../../data"))
path = storage.raw("toyota_2019_001_annual_en.pdf")
parsed = parser.from_file(path, xmlContent=True)
print(parsed["metadata"])
print(">>>>>>>>>>>>>>>>>>>")
print(parsed["content"])
