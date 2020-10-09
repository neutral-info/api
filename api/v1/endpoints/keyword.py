import datetime
import typing

import pymysql
from fastapi import APIRouter, Depends, Form
from loguru import logger
from starlette.requests import Request

from api.tools import load
from api.backend.responses import success_msg
from api.v1.schema.input import DataSetInput, OrderByInput, OrderTypeInput
from api.v1.schema.keywords import News, KeywordList

router = APIRouter()


def convert_vwNews2News(
    listdictdata: typing.List[typing.Dict[str, typing.Union[str, list, float]]], keywords: str, countsinfo: int,
) -> KeywordList:

    group_data_News = []
    for d in listdictdata:
        d["position"] = [{"party": p.split("*")[0], "trend": float(p.split("*")[1])} for p in d["position"].split("|")]
        d["keywords"] = d["keywords"].split(",")
        d["producer"] = {
            "id": d["producer_id"],
            "desc": d["producer_desc"],
            "position": [
                {"party": p.split("*")[0], "trend": float(p.split("*")[1])} for p in d["producer_position"].split("|")
            ],
        }

        d.pop("producer_id", None)
        d.pop("producer_desc", None)
        d.pop("producer_position", None)

        group_data_News.append(News(**d).dict())

    convert_data = {}
    convert_data["totalNews"] = countsinfo["totalNews"]
    convert_data["totalPageNo"] = countsinfo["totalPageNo"]
    convert_data["News"] = group_data_News
    return convert_data


@router.get("/keyword", response_model=KeywordList)
async def get_data(
    request: Request,
    dataset: DataSetInput,
    orderby: OrderByInput,
    ordertype: OrderTypeInput,
    volumeMin: int = None,
    volumeMax: int = None,
    powerMin: int = None,
    powerMax: int = None,
    positions: str = None,
    channel: str = None,
    keywords: str = None,
    pageNo: int = 1,
    pageSize: int = 5,
):
    # FIXME: need to add powerMin, powerMax, channel filter
    ret = load.NID_pages(
        dataset=dataset,
        pageNo=pageNo,
        pageSize=pageSize,
        keywords=keywords,
        positions=positions,
        volumeMin=volumeMin,
        volumeMax=volumeMax,
        datatype="page",
        orderby=orderby,
        ordertype=ordertype,
        version="v1",
    )

    ret_count = load.NID_pages(
        dataset=dataset,
        pageNo=pageNo,
        pageSize=pageSize,
        keywords=keywords,
        positions=positions,
        volumeMin=volumeMin,
        volumeMax=volumeMax,
        datatype="count",
        orderby=orderby,
        ordertype=ordertype,
        version="v1",
    )
    countsinfo = {}
    countsinfo["totalNews"] = ret_count[0]["COUNT(*)"]
    countsinfo["totalPageNo"] = (
        int(countsinfo["totalNews"] / pageSize) + 1
        if (countsinfo["totalNews"] % pageSize)
        else int(countsinfo["totalNews"] / pageSize)
    )

    convert_data = convert_vwNews2News(ret, keywords, countsinfo)

    logger.info(f"get keyword:{keywords} data from {dataset} page {pageNo}")
    return success_msg(convert_data)
