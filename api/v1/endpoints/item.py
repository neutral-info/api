import typing

from fastapi import APIRouter
from loguru import logger
from starlette.requests import Request

from api.backend.responses import success_msg
from api.tools import load
from api.v1.schema.input import ItemTypeInput
from api.v1.schema.items import ItemList

router = APIRouter()


def convert_lisdict2list(
    listdictdata: typing.List[typing.Dict[str, typing.Union[str]]]
) -> typing.List[str]:
    convert_data = []
    for d in listdictdata:
        for k in d:
            convert_data.append(d[k])
    return convert_data


@router.get("/item", response_model=ItemList)
async def get_data(request: Request, itemtype: ItemTypeInput):
    raw_data = load.NID_items(dataset=itemtype)
    convert_data = convert_lisdict2list(raw_data)

    logger.info(f"get itemtype:{itemtype} data")
    return success_msg(convert_data)
