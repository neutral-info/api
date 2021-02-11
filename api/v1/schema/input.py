from enum import Enum


class DataSetInput(str, Enum):
    News = "News"


class ItemTypeInput(str, Enum):
    Position = "Position"
    Channel = "Channel"
    Producer = "Producer"


class OrderByInput(str, Enum):
    pubdate = "pubdate"
    power = "power_now"
    volume = "volume_now"


class OrderTypeInput(str, Enum):
    DESC = "DESC"
    ASC = "ASC"
