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
        start_date: str = "",
        end_date: str = "",
    ):
        list_dic_data = []
        data = get_data(
            dataset=dataset,
            start_date=start_date,
            end_date=end_date,
            keywords=keywords,
        )

        if data:
            list_dic_data = data

        return UJSONResponse(
            {"msg": "success", "status": 200, "data": list_dic_data},
            headers={"Access-Control-Allow-Origin": "*"},
        )
