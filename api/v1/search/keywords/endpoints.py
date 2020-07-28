import typing
from starlette.requests import Request
from starlette.responses import UJSONResponse

from api.backend import application
from api.v1 import schema
from api.v1.search.keywords.keyword import get_data


class Application(application.Application):
    # design api function,
    def __init__(self):
        super(Application, self).__init__()

    def keyword(
        self,
        request: Request,
        dataset: schema.input.DataSetInput,
        keywords: str = "",
        pageNo: int = 1,
        pageSize: int = 10,
        volumeMin: int = None,
        volumeMax: int = None,
        power: int = None,
        positions: str = None,
        channel: str = None,
    ):
        list_dic_data = []
        data = get_data(
            dataset=dataset,
            pageNo=pageNo,
            pageSize=pageSize,
            keywords=keywords,
            volumeMin=volumeMin,
            volumeMax=volumeMax,
            power=power,
            positions=positions,
            channel=channel,
        )

        if data:
            list_dic_data = data

        return UJSONResponse(
            {"msg": "success", "status": 200, "data": list_dic_data},
            headers={"Access-Control-Allow-Origin": "*"},
        )
