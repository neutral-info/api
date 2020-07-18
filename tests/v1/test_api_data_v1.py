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
def data_url(index_url):
    return f"{index_url}/api/v1/search"


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


def test_News(setUp, data_url):
    payload = {
        "dataset": "News",
        "keywords": "蔡英文",
        "start_date": "2020-06-01",
        "end_date": "2020-06-02",
    }
    res = requests.get(data_url, params=payload)
    resp = res.json()["data"][:1]
    assert resp == [
        {
            "id": "6ad51805-494f-49c3-b55e-0b732c7a76a3",
            "pubdate": "2020-06-01T11:57:00",
            "title": "【國艦國造】4000噸級巡防艦內建負壓隔離病房 蔡英文2日主持下水典禮 -- 上報 / 焦點",
            "text": "海巡署委託台船公司製造的首艘4000噸級巡防艦，配備有鎮海火箭、負壓隔離病房，2日將進行下水典禮，並由蔡英文總統親自擲瓶主持並命名。  4000噸級巡防艦有鎮海火箭彈、20機槍、20砲塔等配備，其中，「鎮海火箭彈」，其系統是由中科院研發，可搭載42枚2.75吋火箭彈，這可取代過去海巡巡防艦主砲40砲。  為因應疫情來勢洶洶，艦隊分署特別規劃升級病房設備，一般病房均增設負壓隔離罩，以降低病患間交叉感染機會，同時減低醫療人員受感染之風險，艦上也建置手術室、溫度室，提供完整醫療設備。  4000噸級巡防艦也建置直升機庫，可供海軍S-70C直昇機臨時駐艦，遇有海",
            "keywords": [
                "4000噸級巡防艦",
                "蔡英文",
                "鎮海火箭"
            ],
            "volume_now": 0,
            "volume_yesterday": 0,
            "producer": {
                "id": "5030b49f-81fe-11ea-8627-f23c92e71bad",
                "desc": "上報",
                "position": {
                    "民進黨": 0.65,
                    "國民黨": 0.2,
                    "時力": 0.65,
                    "親中": 0.2
                }
            }
        },
    ]
