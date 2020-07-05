import typing
from pydantic import BaseModel


class News(BaseModel):
    news_id: str
    news_pubdate: str
    news_title: str
    news_text: str
    keywords: str
    producer_id: str
    producer_desc: str
    producer_position: str
    volume_now: float
    volume_yesterday: float
