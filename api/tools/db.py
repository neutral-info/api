import datetime
import typing

from loguru import logger

from api.config import MYSQL_DATA_DATABASE
from api.tools import clients


def query(sql: str, database: str = MYSQL_DATA_DATABASE):
    connect = clients.get_db_client(database)
    cursor = connect.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        connect.close()
        return data
    except Exception as e:
        logger.info(e)
        connect.close()
        return ""


def get_colname(table: str, database: str):
    return query(f"SHOW COLUMNS FROM {table}", database)


def get_start_end_date_sql(
    colname: str, table: str, date: str, end_date: str, keywords: str,
) -> str:
    sql = """
        SELECT `{}`
        FROM `{}`
        WHERE `news_pubdate` >= '{}'
        """.format(
        "`,`".join(colname), table, date
    )

    if end_date:
        sql = f" {sql} AND `news_pubdate` < '{end_date}' "

    if keywords:
        sql = f" {sql} AND `keywords` like '%{keywords}%' "
    return sql


def create_load_sql(
    database: str = "",
    table: str = "",
    date: str = "",
    end_date: str = "",
    keywords: str = "",
) -> str:
    # TODO: maybe news_id not show
    # colname = get_colname(table, database)
    colname = "*"
    sql = get_start_end_date_sql(colname, table, date, end_date, keywords)
    return sql


def get_fetch_alllist(cursor) -> list:
    desc = cursor.description
    # TODO: use loop in row to decode not efficient
    return [
        dict(
            zip(
                [col[0] for col in desc],
                (i.decode() if isinstance(i, bytes) else i for i in row),
            )
        )
        for row in cursor.fetchall()
    ]

    # return [
    #     dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()
    # ]


def load(
    database: str = "",
    table: str = "",
    date: str = "",
    end_date: str = "",
    keywords: str = "",
    version: str = "",
    **kwargs,
) -> typing.List[typing.Dict[str, typing.Union[str, int, float]]]:

    sql = create_load_sql(database, table, date, end_date, keywords)
    logger.info(f"sql cmd:{sql}")

    connect = clients.get_db_client(database)
    cursor = connect.cursor()
    cursor.execute(sql)
    data = get_fetch_alllist(cursor)
    cursor.close()
    connect.close()

    return data


"""
'news_id', b'longtext', 'YES', bytearray(b''), None, '')
01:('news_pubdate', b'longtext', 'YES', bytearray(b''), None, '')
02:('news_title', b'longtext', 'YES', bytearray(b''), None, '')
03:('news_text', b'longtext', 'YES', bytearray(b''), None, '')
04:('keywords', b'longtext', 'YES', bytearray(b''), None, '')
05:('news_keywords', b'longtext', 'YES', bytearray(b''), None, '')
06:('producer_id', b'longtext', 'YES', bytearray(b''), None, '')
07:('producer_desc', b'varchar(100)', 'YES', bytearray(b''), None, '')
08:('producer_position', b'varchar(31)', 'NO', bytearray(b''), b'', '')
09:('volume_now', b'int', 'NO', bytearray(b''), b'0', '')
10:('volume_yesterday', b'int', 'NO', bytearray(b''), b'0', '')
"""
