
import pymysql
from tests.helpers import (
    get_dst_hash,
    get_src_hash,
)

from etl.transfer_service import TransferService
from .helpers import ping_container


def test_container_is_alive(mysql_source_image):
    assert ping_container(mysql_source_image)


def test_containers_assets_is_ready(mysql_source_image,
                                    mysql_destination_image):

    src_conn = pymysql.connect(**mysql_source_image,
                               cursorclass=pymysql.cursors.DictCursor)

    with src_conn:
        with src_conn.cursor() as c:
            src_query = """
                SELECT 
                    COUNT(*) AS total 
                FROM transactions t
                    JOIN operation_types ot ON t.idoper = ot.id
            """

            c.execute(src_query)
            src_result = c.fetchone()

    dst_conn = pymysql.connect(**mysql_destination_image,
                               cursorclass=pymysql.cursors.DictCursor)

    with dst_conn:
        with dst_conn.cursor() as c:
            dst_query = """
                SELECT 
                    COUNT(*) AS total 
                FROM transactions_denormalized t
            """

            c.execute(dst_query)
            dst_result = c.fetchone()

    assert src_result['total'] > 0
    assert dst_result['total'] == 0


def test_data_transfer(mysql_src_connection, mysql_dst_connection):
    transfer_service = TransferService()
    for _ in range(15):
        transfer_service.transfer()
    src_hash = get_src_hash(mysql_src_connection)
    dst_hash = get_dst_hash(src_hash, mysql_dst_connection)
    assert dst_hash
    assert dst_hash['MD5'] == src_hash['MD5']
