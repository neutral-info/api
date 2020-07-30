import typing

from api.tools import load
from api.v1.schema.keywords import News, KeywordList
from loguru import logger


def convert_vwNews2News(
    listdictdata: typing.List[typing.Dict[str, typing.Union[str, list, float]]],
    keywords: str,
    countsinfo: int,
) -> KeywordList:

    group_data_News = []
    for d in listdictdata:
        d["keywords"] = d["keywords"].split(",")
        d["producer"] = {
            "id": d["producer_id"],
            "desc": d["producer_desc"],
            "position": [
                {"party:": p.split("*")[0], "trend": float(p.split("*")[1])}
                for p in d["producer_position"].split("|")
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


def get_data(
    dataset: str,
    pageNo: int,
    pageSize: int,
    keywords: str,
    volumeMin: int,
    volumeMax: int,
    power: int,
    positions: str,
    channel: str,
):
    # FIXME: need to add power, channel filter
    ret = load.NeutralInfoData(
        dataset=dataset,
        pageNo=pageNo,
        pageSize=pageSize,
        keywords=keywords,
        positions=positions,
        volumeMin=volumeMin,
        volumeMax=volumeMax,
        datatype="page",
        version="v1",
    )

    ret_count = load.NeutralInfoData(
        dataset=dataset,
        pageNo=pageNo,
        pageSize=pageSize,
        keywords=keywords,
        positions=positions,
        volumeMin=volumeMin,
        volumeMax=volumeMax,
        datatype="count",
        version="v1",
    )
    countsinfo = {}
    countsinfo["totalNews"] = ret_count[0]["COUNT(*)"]
    countsinfo["totalPageNo"] = int(countsinfo["totalNews"] / pageSize) + 1 if (countsinfo["totalNews"] % pageSize) else int(countsinfo["totalNews"] / pageSize)

    convert_data = convert_vwNews2News(ret, keywords, countsinfo)

    logger.info(f"get keyword:{keywords} data from {dataset} page {pageNo}")
    return convert_data
