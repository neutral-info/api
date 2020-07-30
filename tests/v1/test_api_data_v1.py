import datetime
import time
from multiprocessing import Process

import pytest
import requests
import uvicorn

from api.main import App


@pytest.fixture(scope="module")
def index_url():
    return "http://127.0.0.1:5000"


@pytest.fixture(scope="module")
def keyword_url(index_url):
    return f"{index_url}/api/v1/keyword"


@pytest.fixture(scope="module")
def setUp():
    app = App()
    proc = Process(
        target=uvicorn.run,
        args=(app.api,),
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


def test_News(setUp, keyword_url):
    payload = {
        "dataset": "News",
        "keywords": "蔡英文",
        "pageNo": 1,
        "pageSize": 1,
        "volumeMin": 0,
        "volumeMax": 10,
        "orderby": "pubdate",
        "ordertype": "DESC",
        "positions": "國民黨",
    }
    res = requests.get(keyword_url, params=payload)
    resp = res.json()["data"]
    assert resp == {
        "totalNews": 8,
        "totalPageNo": 8,
        "News": [
            {
                "id": "55a47e60-f6ef-455c-908c-d0e52ed9fed8",
                "pubdate": "2020-06-02T15:08:00",
                "title": "主持4千噸級「嘉義艦」下水典禮 蔡英文：「國艦國造」的雙重里程碑 -- 上報 / 焦點",
                "text": "2日上午，蔡英文總統與行政院副院長陳其邁、海洋委員會李仲威、海巡署署長陳國恩及台船公司董事長鄭文隆等人共同出席於台船公司高雄廠舉行的「4000噸級巡防艦首艦命名暨下水典禮」。  蔡英文除了為巡防艦命名為「嘉義艦」外，並按照慣例執行「擲瓶下水」儀式。她表示，「嘉義艦」開創了兩個新的里程碑，除了是國艦國造的重大成功外，船上搭載的醫療設備也為台灣海上醫療救護能量寫下嶄新的一頁。  蔡英文2日主持「嘉義艦」的命名暨擲瓶下水典禮，嘉義艦未來將隸屬於中部地區機動海巡隊。  4千噸級的嘉義艦是海巡署歷來噸位最大的海巡艦，能承受10級強風、續航力超過10000浬；嘉義艦",
                "keywords": [
                    "嘉義艦",
                    "巡防艦",
                    "蔡英文",
                    "海巡署"
                    ],
                "producer": {
                    "id": "5030b49f-81fe-11ea-8627-f23c92e71bad",
                    "desc": "上報",
                    "position": [
                        {
                        "party:": "民進黨",
                        "trend": "0.65"
                        },
                        {
                        "party:": "國民黨",
                        "trend": "0.2"
                        },
                        {
                        "party:": "時力",
                        "trend": "0.65"
                        },
                        {
                        "party:": "親中",
                        "trend": "0.2"
                        }
                    ]
                },
                "volume_now": 0,
                "volume_yesterday": 0
            }
        ]
    }
