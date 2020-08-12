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


def is_where_or_and(first_condiction_flag):
    if first_condiction_flag:
        where_or_and = "WHERE"
        first_condiction_flag = False
    else:
        where_or_and = "AND"
    return first_condiction_flag, where_or_and


def get_keywords_page_sql(
    colname: str,
    table: str,
    pageNo: str,
    pageSize: str,
    keywords: str,
    positions: str,
    volumeMin: int,
    volumeMax: int,
    orderby: str,
    ordertype: str,
) -> str:

    statrIndex = (pageNo - 1) * pageSize
    sql = """
        SELECT {0}
        FROM `{1}`
        """.format(colname, table)

    first_condiction_flag = True
    if keywords:
        first_condiction_flag, where_or_and = is_where_or_and(
            first_condiction_flag
        )

        keywords_statement = []
        for k in keywords.split(","):
            k = k.strip()
            keywords_statement.append(f" `keywords` like '%{k}%' ")
        keywords_statement = (
            f"{where_or_and} ( " + "OR".join(keywords_statement) + " )"
        )
        sql = f" {sql} {keywords_statement} "

    if positions:
        first_condiction_flag, where_or_and = is_where_or_and(
            first_condiction_flag
        )

        position_statement = []
        for p in positions.split(","):
            p = p.strip()
            position_statement.append(f" `position` like '%{p}%'")
        position_statement = (
            f"{where_or_and} ( " + " AND ".join(position_statement) + " )"
        )
        sql = f" {sql} {position_statement} "

    if volumeMin:
        first_condiction_flag, where_or_and = is_where_or_and(
            first_condiction_flag
        )

        volumeRange_statement = f"{where_or_and} `volume_now` >= {volumeMin}"
        sql = f" {sql} {volumeRange_statement} "

    if volumeMax:
        first_condiction_flag, where_or_and = is_where_or_and(
            first_condiction_flag
        )

        volumeRange_statement = f"{where_or_and} `volume_now` <= {volumeMax} "
        sql = f" {sql} {volumeRange_statement} "

    if colname != "COUNT(*)":
        order_limit_statement = f"""
                                ORDER BY `{orderby}` {ordertype}
                                LIMIT {statrIndex}, {pageSize}
                                """
        sql = f" {sql} {order_limit_statement} "
    return sql


def get_fetch_alllist(cursor) -> list:
    desc = cursor.description
    q = [
        dict(
            zip(
                [col[0] for col in desc],
                (r.decode() if isinstance(r, bytes) else r for r in row),
            )
        )
        for row in cursor.fetchall()
    ]
    return q
    # return [
    #     dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()
    # ]


def create_pages_sql(
    database: str,
    table: str,
    pageNo: int,
    pageSize: int,
    keywords: str,
    positions: str,
    volumeMin: int,
    volumeMax: int,
    datatype: str,
    orderby: str,
    ordertype: str,
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
            orderby,
            ordertype,
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
            orderby,
            ordertype,
        )
    return sql


def load_pages(
    database: str = "",
    table: str = "",
    pageNo: int = None,
    pageSize: int = None,
    keywords: str = "",
    positions: str = "",
    volumeMin: int = None,
    volumeMax: int = None,
    datatype: str = "",
    orderby: str = "",
    ordertype: str = "",
    version: str = "",
    **kwargs,
) -> typing.List[typing.Dict[str, typing.Union[str, int, float]]]:

    sql = create_pages_sql(
        database,
        table,
        pageNo,
        pageSize,
        keywords,
        positions,
        volumeMin,
        volumeMax,
        datatype,
        orderby,
        ordertype,
    )

    logger.info(f"sql cmd:{sql}")

    connect = clients.get_db_client(database)
    cursor = connect.cursor()
    cursor.execute(sql)
    data = get_fetch_alllist(cursor)
    cursor.close()
    connect.close()

    return data
