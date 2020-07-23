import typing

from api.tools import load
from api.v1.schema.keywords import News, NewsList
from loguru import logger


def convert_vwNews2News(
    listdictdata: typing.List[typing.Dict[str, typing.Union[str, list, float]]],
    keywords: str
) -> NewsList:

    group_data = {}
    group_data["keyword"] = [keywords]
    group_data["News"] = []
    for d in listdictdata:
        d["keywords"] = d["keywords"].split(",")
        d["producer"] = {
            "id": d["producer_id"],
            "desc": d["producer_desc"],
            "position": [
                {
                    "party:": p.split("*")[0],
                    "trend":float(p.split("*")[1])
                } for p in d["producer_position"].split("|")
            ]
        }

        d.pop("producer_id", None)
        d.pop("producer_desc", None)
        d.pop("producer_position", None)

        group_data["News"].append(News(**d).dict())
        group_data["News"].append(d)

    convert_data = [group_data]
    return convert_data


def get_data(
    dataset: str, start_date: str, end_date: str, keywords: str
) -> NewsList:
    ret = load.NeutralInfoData(
        dataset=dataset,
        date=start_date,
        end_date=end_date,
        keywords=keywords,
        version="v1",
    )

    convert_data = convert_vwNews2News(ret, keywords)

    logger.info(
        f"get keyword:{keywords} data from {dataset} between {start_date} and {end_date} result"
    )
    return convert_data
