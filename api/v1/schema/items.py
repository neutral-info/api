import typing
from pydantic import BaseModel


class ItemList(BaseModel):
    Item: typing.List[str]
