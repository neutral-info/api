import datetime
import time
from multiprocessing import Process

import pytest
import requests
import uvicorn

from api.main import app


@pytest.fixture(scope="module")
def index_url():
    return "http://127.0.0.1:5000"


@pytest.fixture(scope="module")
def api_v1_url(index_url):
    return f"{index_url}/api/v1"


@pytest.fixture(scope="module")
def keyword_url(api_v1_url):
    return f"{api_v1_url}/keyword"


@pytest.fixture(scope="module")
def setUp():
    proc = Process(
        target=uvicorn.run,
        args=(app,),
        kwargs={"host": "127.0.0.1", "port": 5000, "log_level": "info"},
        daemon=True,
    )
    proc.start()
    time.sleep(1)
    return 1


def test_index(setUp, index_url):
    res = requests.get(index_url)
    assert res.json() == {"status": "ok"}
    assert res.headers["access-control-allow-origin"] == "*"


def test_openapi(setUp, index_url):
    res = requests.get(f"{index_url}/openapi.json")
    assert res.status_code == 200


# def test_News(setUp, keyword_url):
#     payload = {
#         "dataset": "News",
#         "keywords": "蔡英文",
#         "pageNo": 1,
#         "pageSize": 1,
#         "volumeMin": 0,
#         "volumeMax": 10,
#         "powerMin": 0,
#         "powerMax": 1,
#         "orderby": "pubdate",
#         "producers": "自由時報",
#         "ordertype": "DESC",
#         "positions": "國民黨",
#     }
#     res = requests.get(keyword_url, params=payload)
#     resp = res.json()["data"]
#     assert resp == {
#         "totalNews": 7,
#         "totalPageNo": 7,
#         "News": [
#             {
#                 "id": "1a389b4edbfa47ab8995600953b41a7e",
#                 "position": [
#                     {
#                         "party": "民進黨",
#                         "trend": 0.75
#                     },
#                     {
#                         "party": "國民黨",
#                         "trend": 0.25
#                     },
#                     {
#                         "party": "時力",
#                         "trend": 0.6
#                     }
#                 ],
#                 "pubdate": "2021-02-08T03:54:14Z",
#                 "title": "新任最高行政法院院長 吳明鴻宣誓就職 - 自由時報電子報",
#                 "text": "蔡英文總統今上午主持「新任行政院政務人員及最高行政法院院長宣誓典禮」。宣誓儀式開始後，總統就監誓人位置，隨後司儀唱名宣誓人，宣誓人由最高行政法院院長吳明鴻帶領宣讀誓詞；宣誓後，總統逐一向宣誓人拱手致意，儀式簡單隆重。副總統賴清德、司法院院長許宗力及總統府秘書長李大維等人均在場觀禮。",
#                 "keywords": [
#                     "上午",
#                     "最高行政法院",
#                     "自由時報",
#                     "蔡英文",
#                     " 吳明鴻",
#                     "行政院"
#                 ],
#                 "author": {
#                     "id": "test",
#                     "desc": "新聞記者",
#                     "position": [
#                         {
#                             "party": "民進黨",
#                             "trend": 0.75
#                         },
#                         {
#                             "party": "國民黨",
#                             "trend": 0.25
#                         },
#                         {
#                             "party": "時力",
#                             "trend": 0.6
#                         }
#                     ]
#                 },
#                 "producer": {
#                     "id": "ltn.com.tw",
#                     "desc": "自由時報",
#                     "position": [
#                         {
#                             "party": "民進黨",
#                             "trend": 0.75
#                         },
#                         {
#                             "party": "國民黨",
#                             "trend": 0.25
#                         },
#                         {
#                             "party": "時力",
#                             "trend": 0.6
#                         }
#                     ]
#                 },
#                 "channel": {
#                     "id": "1",
#                     "desc": "新聞"
#                 },
#                 "volume_now": 0,
#                 "volume_yesterday": 0,
#                 "power_now": 0,
#             }
#         ]
#     }
