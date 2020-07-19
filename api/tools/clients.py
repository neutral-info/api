# import pymysql
import mysql.connector  # TODO: change to pymysql
import datetime
from api.config import (
    MYSQL_DATA_HOST,
    MYSQL_DATA_PASSWORD,
    MYSQL_DATA_PORT,
    MYSQL_DATA_USER,
    MYSQL_DATA_DATABASE,
    var_test,
)


def data_db(database: str,):
    print("test_var:{}".format(var_test))
    connect = mysql.connector.connect(
        host=MYSQL_DATA_HOST,
        port=MYSQL_DATA_PORT,
        user=MYSQL_DATA_USER,
        password=MYSQL_DATA_PASSWORD,
        database=database,
        charset="utf8",
    )
    return connect


def get_db_client(database: str = MYSQL_DATA_DATABASE):
    return data_db(database)
