import pymysql


class Connection:
    _con = None
    def __init__(self, host: str, db_user: str, password: str, db_name: str, port: str):
        self._con = pymysql.connect(
            host=host,
            port=port,
            database=db_name,
            user=db_user,
            password=password,
            autocommit=True
        )

    def select(self, query):
        with self._con.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def insert(self, query):
        with self._con.cursor() as cursor:
            cursor.execute(query)
        self._con.commit()

    def __del__(self):
        self._con.close()
