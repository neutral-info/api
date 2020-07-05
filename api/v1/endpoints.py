import importlib
import typing

from starlette.requests import Request
from starlette.responses import UJSONResponse

from api.backend import application
from api.tools import load
from api.v1 import schema


def check_schema(
    ret: typing.List[typing.Dict[str, typing.Union[str, int, float]]], schema,
) -> typing.List[typing.Dict[str, typing.Union[str, int, float]]]:
    ret_schema = [schema(**rr).__dict__ for rr in ret]
    return ret_schema


class Application(application.Application):
    # design api function,
    def __init__(self):
        super(Application, self).__init__()

    async def data_v1(
        self,
        request: Request,
        dataset: schema.input.DataSetInput,
        keywords: str = "",
        start_date: str = "",
        end_date: str = "",
    ):
        _keywords = keywords
        _ip = request.client.host
        # TODO: for future save ip log
        parameter = dict(
            keywords=_keywords,
            start_date=start_date,
            end_date=end_date,
            url="/api/v1",
        )

        ret = load.NeutralInfoData(
            dataset=dataset,
            date=start_date,
            end_date=end_date,
            keywords=_keywords,
            version="v1",
        )

        if len(ret):
            ret_schema = getattr(
                importlib.import_module("api.v1.schema.output_data"), dataset,
            )

            ret = check_schema(ret, ret_schema)

        return UJSONResponse(
            {"msg": "success", "status": 200, "data": ret},
            headers={"Access-Control-Allow-Origin": "*"},
        )
