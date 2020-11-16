from starlette.responses import UJSONResponse
import typing


def success_msg(
    resp_data: typing.List[typing.Union[str, typing.Dict]]
) -> UJSONResponse:
    resp = {"msg": "success", "status": 200}
    resp.update({"data": resp_data})
    return UJSONResponse(
        resp,
        headers={"Access-Control-Allow-Origin": "*"},
    )
