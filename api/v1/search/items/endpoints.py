from starlette.requests import Request
from starlette.responses import UJSONResponse

from api.backend import application
from api.v1 import schema
from api.v1.search.items.item import get_data


class Application(application.Application):
    # design api function,
    def __init__(self):
        super(Application, self).__init__()

    def item(
        self,
        request: Request,
        itemtype: schema.input.ItemTypeInput,
    ):
        list_dic_data = []
        data = get_data(
            itemtype=itemtype,
        )

        if data:
            list_dic_data = data

        return UJSONResponse(
            {"msg": "success", "status": 200, "data": list_dic_data},
            headers={"Access-Control-Allow-Origin": "*"},
        )
