import typing
from pydantic import BaseModel


class News(BaseModel):
    id: str
    pubdate: str
    title: str
    text: str
    keywords: str
    producer_id: str
    producer_desc: str
    producer_position: str
    volume_now: float
    volume_yesterday: float
