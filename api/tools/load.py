import typing

from loguru import logger
from api.tools.db import load
from api.tools.data_dict import (
    TABLE_DICT,
    DATABASE_DICT,
)


def NeutralInfoData(
    dataset: str,
    date: str = "",
    end_date: str = "",
    keywords: str = "",
    version: str = "",
):
    parameter = dict(
        table=TABLE_DICT.get(dataset),
        database=DATABASE_DICT.get(dataset),
        date=f"{date} 00:00:00",
        end_date=f"{end_date} 00:00:00",
        keywords=keywords,
        version=version,
    )
    logger.info(f"parameter: {parameter}")
    data = load(**parameter)
    return data
