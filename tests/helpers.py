import time
import uuid
import socket
import pymysql
import docker   # noqa
from .assets import (source_ddl_transactions,
                     source_ddl_type_opers,
                     source_data_transactions,
                     source_data_opers,
                     destination_ddl_transactions)


def get_session_id():
    return str(uuid.uuid4())


def get_unused_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def ping_container(mysql_credentials, container_id=None):

    timeout = 0.001

    for i in range(100):
        try:
            conn = pymysql.connect(**mysql_credentials)

            cursor = conn.cursor()
            cursor.execute('SELECT VERSION()')
            result = cursor.fetchall()

            return result
        except pymysql.Error:
            time.sleep(timeout)
            timeout *= 2
    else:
        raise RuntimeError(f'Cannot connect to container {container_id}.')


def load_assets_to_source_db(mysql_credentials):
    conn = pymysql.connect(**mysql_credentials)
    with conn:
        with conn.cursor() as c:
            for ddl in (source_ddl_transactions,
                        source_ddl_type_opers):
                c.execute(ddl)

            c.executemany(
                'INSERT INTO transactions (dt, idoper, move, amount) VALUES (%s, %s, %s, %s)',  # noqa
                source_data_transactions)

            c.executemany(
                'INSERT INTO operation_types (id, name) VALUES (%s, %s)',
                source_data_opers)


def load_struct_to_destination_db(mysql_credentials):
    conn = pymysql.connect(**mysql_credentials)
    with conn:
        with conn.cursor() as c:
            c.execute(destination_ddl_transactions)


def get_src_hash(mysql_src_connection):
    src_query = f"""SELECT 
                    t.id,
                    CONCAT(t.dt, t.move, t.amount, ot.id, ot.name),
                    MD5(CONCAT(t.dt, t.move, t.amount, ot.id, ot.name)) AS MD5 FROM transactions t  
                    JOIN operation_types ot ON t.idoper = ot.id LIMIT 1
            """

    with mysql_src_connection.cursor() as c:

        c.execute(src_query)
        src_result = c.fetchone()
    return src_result


def get_dst_hash(src_hash, mysql_dst_connection):
    src_query = f"""
        SELECT 
        id,
        CONCAT(dt, move,  amount, idoper, name_oper),
        MD5(CONCAT(dt, move,  amount, idoper, name_oper)) AS MD5
        FROM transactions_denormalized where transactions_denormalized.id = {src_hash['id']}  limit 1
    """

    with mysql_dst_connection.cursor() as c:

        c.execute(src_query)
        dst_result = c.fetchone()
    return dst_result
