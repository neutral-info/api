import typing

from api.tools import load
from api.v1.schema import keywords
from loguru import logger


def convert_vwNews2News(listdictdata: typing.List[typing.Dict[str, typing.Union[str, list, float]]]) -> keywords.NewsList:
    convert_data = []
    for d in listdictdata:
        d["keywords"] = d["keywords"].split(",")
        d["producer"] = {
            "id": d["producer_id"],
            "desc": d["producer_desc"],
            "position": {
                s.split("*")[0]:float(s.split("*")[1]) for s in d["producer_position"].split("|")
            },
        }

        d.pop('producer_id', None)
        d.pop('producer_desc', None)
        d.pop('producer_position', None)

        convert_data.append(keywords.News(**d).dict())
        convert_data.append(d)
    return convert_data

def get_data(dataset :str, start_date: str, end_date: str, keywords: str) -> keywords.NewsList:
    ret = load.NeutralInfoData(
        dataset=dataset,
        date=start_date,
        end_date=end_date,
        keywords=keywords,
        version="v1",
    )

    convert_data = convert_vwNews2News(ret)

    logger.info(
        f"get keyword:{keywords} data from {dataset} between {start_date} and {end_date} result"
    )
    return convert_data
