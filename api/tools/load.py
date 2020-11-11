import typing

from loguru import logger
from api.tools.db import load_pages
from api.tools.data_dict import (
    TABLE_DICT,
    DATABASE_DICT,
)


def NID_pages(
    dataset: str,
    pageNo: int,
    pageSize: int,
    keywords: str,
    positions: str,
    volumeMin: int,
    volumeMax: int,
    author: str,
    channel: str,
    producer: str,
    ordertype: str,
    orderby: str,
    datatype: str = "page",
    version: str = "",
):
    parameter = dict(
        table=TABLE_DICT.get(dataset),
        database=DATABASE_DICT.get(dataset),
        pageNo=pageNo,
        pageSize=pageSize,
        keywords=keywords,
        positions=positions,
        volumeMin=volumeMin,
        volumeMax=volumeMax,
        author=author,
        channel=channel,
        producer=producer,
        datatype=datatype,
        orderby=orderby,
        ordertype=ordertype,
        version=version,
    )
    logger.info(f"NID_pages parameter: {parameter}")
    data = load_pages(**parameter)
    return data
