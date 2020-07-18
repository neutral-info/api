import typing

from api.tools import load
from api.v1.schema import keywords


def convert_vwNews2News(listdictdata) -> keywords.NewsList:
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

        # convert_data.append(keywords.News(**d))
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
    return convert_data
