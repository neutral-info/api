import typing

from loguru import logger
from api.tools.db import load
from api.tools.data_dict import (
    TABLE_DICT,
    DATABASE_DICT,
)


def NeutralInfoData(
    dataset: str,
    pageNo: int,
    pageSize: int,
    keywords: str,
    positions: str,
    volumeMin: int,
    volumeMax: int,
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
        datatype=datatype,
        orderby=orderby,
        ordertype=ordertype,
        version=version,
    )
    logger.info(f"parameter: {parameter}")
    data = load(**parameter)
    return data
