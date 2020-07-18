import typing
from pydantic import BaseModel


class News(BaseModel):
    id: str
    pubdate: str
    title: str
    text: str
    keywords: typing.List[str]
    producer: typing.Dict[str, typing.Union[str, typing.Dict[str, float]]]
    volume_now: float
    volume_yesterday: float


class NewsList(BaseModel):
    News: typing.List[News]