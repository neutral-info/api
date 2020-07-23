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
    version: str = "",
):
    parameter = dict(
        table=TABLE_DICT.get(dataset),
        database=DATABASE_DICT.get(dataset),
        pageNo=pageNo,
        pageSize=pageSize,
        keywords=keywords,
        version=version,
    )
    logger.info(f"parameter: {parameter}")
    data = load(**parameter)
    return data
