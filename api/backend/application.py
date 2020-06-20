from loguru import logger

from fastapi import FastAPI
from starlette.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware


class Application:
    """ Core application to test. """

    def __init__(self):
        # 模板無法更改，需要到 fastapi 修改底層 code
        descritption = '<h2> \
            不同網站可能會基於演算法，來改變使用者會看見的資訊 \
            <a href = "https://github.com/neutral-info"  target="_blank" style="font-size:20pt">neutral-info</a> \
            希望建立一個中立的資訊平台，使用者可以利用關鍵字，找到你想知道的訊息，\
            這些訊息來自多元管道，並可以依照訊息特徵（聲量、情緒、來源），做出篩選 \
            </h2>'
        self.api = FastAPI(
            title="neutral-info api", version="1.1.1", description=descritption
        )
        origins = [
            "http://localhost",
            "http://localhost:80",
            "http://localhost:443",
            "http://localhost:8080",
            "http://localhost:5000",
        ]
        self.api.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        )
        self.api.get("/")(self.main)
        self.api.on_event("shutdown")(self.close)

    async def main(self):
        return UJSONResponse(
            {"status": "ok"}, headers={"Access-Control-Allow-Origin": "*"}
        )

    async def close(self):
        """ Gracefull shutdown. """
        logger.info("Shutting down the app.")
