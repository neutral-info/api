from fastapi import APIRouter
from loguru import logger
from api.v1 import schema

router = APIRouter()


@router.get("/item")
async def get_data(itemtype: schema.input.ItemTypeInput):
    convert_data = []
    if itemtype == "Position":
        convert_data = ["時代力量", "國民黨", "民進黨", "親民黨", "民眾黨", "無立場"]
    elif itemtype == "Channel":
        convert_data = ["新聞", "社群論壇", "聊天", "部落格", "內容農場", "影音"]

    logger.info(f"get itemtype:{itemtype} data")
    return convert_data
