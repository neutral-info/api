import typing
from pydantic import BaseModel


class ItemList(BaseModel):
    News: typing.List[str]
