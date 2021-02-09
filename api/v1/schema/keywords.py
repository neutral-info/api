import typing
from pydantic import BaseModel, Field


class NewsPosition(BaseModel):
    party: str = Field(description="News party")
    trend: float = Field(description="News party trend")


class NewsAuthorPosition(BaseModel):
    party: str = Field(description="News writer party")
    trend: float = Field(description="News writer party trend")


class NewsAuthor(BaseModel):
    id: str = Field(description="News author id")
    desc: str = Field(description="News author describe")
    position: typing.List[NewsAuthorPosition]


class NewsProducerPosition(BaseModel):
    party: str = Field(description="News producer party")
    trend: float = Field(description="News producer party trend")


class NewsProducer(BaseModel):
    id: str = Field(description="News producer id")
    desc: str = Field(description="News producer describe")
    position: typing.List[NewsProducerPosition]


class NewsChannel(BaseModel):
    id: str = Field(description="News channel id")
    desc: str = Field(description="News channel describe")


class News(BaseModel):
    id: str = Field(description="News id")
    position: typing.List[NewsPosition] = Field(description="News party position trend")
    pubdate: str = Field(description="News public date")
    title: str = Field(description="News title")
    text: str  = Field(description="News content")
    keywords: typing.List[str]  = Field(description="Query keywords")
    author: NewsAuthor = Field(description="News author detail")
    producer: NewsProducer = Field(description="News producer detail")
    channel: NewsChannel = Field(description="News channel detail")
    volume_now: float = Field(description="News current volume")
    volume_yesterday: float = Field(description="News yesterday volume")
    bomb_now: float = Field(description="News current bomb")


class KeywordList(BaseModel):
    totalNews: int = Field(description="Number of total query news")
    totalPageNo: int = Field(description="Number of total web page")
    News: typing.List[News]
