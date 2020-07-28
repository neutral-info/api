from enum import Enum


class DataSetInput(str, Enum):
    News = "News"


class ItemTypeInput(str, Enum):
    Position = "Position"
    Channel = "Channel"
