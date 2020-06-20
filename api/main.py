from loguru import logger
from starlette.responses import UJSONResponse

from api import v1


class App(v1.Application):
    # design api interface
    def __init__(self):
        super(App, self).__init__()
        # register endpoints
        self.api.get("/")(self.main)
        self.api.on_event("shutdown")(self.close)

    async def main(self):
        return UJSONResponse(
            {"status": "ok"}, headers={"Access-Control-Allow-Origin": "*"}
        )

    async def close(self):
        """ Gracefull shutdown. """
        logger.info("Shutting down the app.")


app = App().api
