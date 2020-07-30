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


# def get_start_end_date_sql(
#     colname: str, table: str, date: str, end_date: str, keywords: str,
# ) -> str:
#     sql = """
#         SELECT `{}`
#         FROM `{}`
#         WHERE `pubdate` >= '{}'
#         """.format(
#         "`,`".join(colname), table, date
#     )

#     if end_date:
#         sql = f" {sql} AND `pubdate` < '{end_date}' "

#     if keywords:
#         keywords_statement = []
#         for k in keywords.split(","):  # TODO: need to check format
#             keywords_statement.append(f" `keywords` like '%{k}%' ")
#         keywords_statement = "( " + "OR".join(keywords_statement) + " )"
#         sql = f" {sql} AND {keywords_statement} "
#     return sql


def get_keywords_page_sql(
    colname: str,
    table: str,
    pageNo: str,
    pageSize: str,
    keywords: str,
    positions: str,
    volumeMin: int,
    volumeMax: int,
) -> str:

    statrIndex = (pageNo - 1) * pageSize
    sql = """
        SELECT {0}
        FROM `{1}`
        """.format(colname, table
    )

    first_condiction_flag = True
    if keywords:
        if first_condiction_flag:
            where_or_and = "WHERE"
            first_condiction_flag = False
        else:
            where_or_and = "AND"

        keywords_statement = []
        for k in keywords.split(","):
            k = k.strip()
            keywords_statement.append(f" `keywords` like '%{k}%' ")
        keywords_statement = f"{where_or_and} ( " + "OR".join(keywords_statement) + " )"
        sql = f" {sql} {keywords_statement} "

    if positions:
        if first_condiction_flag:
            where_or_and = "WHERE"
            first_condiction_flag = False
        else:
            where_or_and = "AND"

        position_statement = []
        for p in positions.split(","):
            p = p.strip()
            position_statement.append(f" `producer_position` like '%{p}%'")
        position_statement = f"{where_or_and} ( " + " AND ".join(position_statement) + " )"
        sql = f" {sql} {position_statement} "

    if volumeMin or volumeMax:
        if first_condiction_flag:
            where_or_and = "WHERE"
            first_condiction_flag = False
        else:
            where_or_and = "AND"

        volumeRange_statement = (
            f"{where_or_and} `volume_now` BETWEEN {volumeMin} AND {volumeMax} "
        )
        sql = f" {sql} {volumeRange_statement} "

    if colname != "COUNT(*)":
        order_limit_statement = f"""
                                ORDER BY `pubdate` DESC
                                LIMIT {statrIndex}, {pageSize}
                                """
        sql = f" {sql} {order_limit_statement} "
    return sql


def get_fetch_alllist(cursor) -> list:
    desc = cursor.description
    # q = [
    #     dict(
    #         zip(
    #             [col[0] for col in desc],
    #             (r.decode() if type(r) == bytes else r for r in row),
    #         )
    #     )
    #     for row in cursor.fetchall()
    # ]
    # return q
    return [
        dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()
    ]


def create_load_sql(
    database: str,
    table: str,
    pageNo: int,
    pageSize: int,
    keywords: str,
    positions: str,
    volumeMin: int,
    volumeMax: int,
    datatype: str,
) -> str:
    # TODO: maybe news_id not show
    # colname = get_colname(table, database)
    if datatype == "page":
        colname = "*"
        sql = get_keywords_page_sql(
            colname,
            table,
            pageNo,
            pageSize,
            keywords,
            positions,
            volumeMin,
            volumeMax,
        )
    elif datatype == "count":
        colname = "COUNT(*)"
        sql = get_keywords_page_sql(
            colname,
            table,
            pageNo,
            pageSize,
            keywords,
            positions,
            volumeMin,
            volumeMax,
        )
    return sql


def load(
    database: str = "",
    table: str = "",
    pageNo: int = None,
    pageSize: int = None,
    keywords: str = "",
    positions: str = "",
    volumeMin: int = None,
    volumeMax: int = None,
    datatype: str = None,
    version: str = "",
    **kwargs,
) -> typing.List[typing.Dict[str, typing.Union[str, int, float]]]:

    sql = create_load_sql(
        database,
        table,
        pageNo,
        pageSize,
        keywords,
        positions,
        volumeMin,
        volumeMax,
        datatype,
    )

    logger.info(f"sql cmd:{sql}")

    connect = clients.get_db_client(database)
    cursor = connect.cursor()
    cursor.execute(sql)
    data = get_fetch_alllist(cursor)
    cursor.close()
    connect.close()

    return data
