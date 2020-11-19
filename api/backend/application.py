from loguru import logger

from fastapi import FastAPI
from starlette.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware


class FastAPI(FastAPI):
    def __init__(self):
        super(FastAPI, self).__init__()
        self.get("/")(self.main)
        self.on_event("shutdown")(self.close)
        descritption = '<h2> \
            不同網站可能會基於演算法，來改變使用者會看見的資訊 \
            <a href = "https://github.com/neutral-info"  target="_blank" style="font-size:20pt">neutral-info</a> \
            希望建立一個中立的資訊平台，使用者可以利用關鍵字，找到你想知道的訊息，\
            這些訊息來自多元管道，並可以依照訊息特徵（聲量、情緒、來源），做出篩選 \
            </h2>'
        self.descritption = descritption
        self.title = "neutral-info api"
        self.version = "1.0.0"
        origins = [
            "http://localhost",
            "http://localhost:80",
            "http://localhost:443",
            "http://localhost:8080",
            "http://localhost:5000",
            "http://neutral-info.herokuapp.com",
            "https://neutral-info.herokuapp.com",
        ]
        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        )

    async def main(self):
        return UJSONResponse(
            {"status": "ok"}, headers={"Access-Control-Allow-Origin": "*"}
        )

    async def close(self):
        """ Gracefull shutdown. """
        logger.info("Shutting down the app.")
