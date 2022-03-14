import datetime

import pytz
from etl.connection import Connection


class SourceDataRepository:
    def __init__(self, connection: Connection):
        self._connection = connection

    def get_operation_types(self):
        return self._connection.select('SELECT * FROM operation_types')

    def get_transactions(self, start_dt , end_dt):
        return self._connection.select(f'SELECT * FROM transactions WHERE `dt` BETWEEN FROM_UNIXTIME({start_dt}) AND FROM_UNIXTIME({end_dt})')

    def get_data(self, start_dt, end_dt):
        return self._connection.select(
            f"""SELECT t.id, t.dt, t.move, t.amount, ot.id, ot.name FROM transactions t  
                JOIN operation_types ot ON t.idoper = ot.id AND `dt` 
                BETWEEN FROM_UNIXTIME({int(start_dt)}) AND FROM_UNIXTIME({int(end_dt)})
        """)


class DestinationDataRepository:
    def __init__(self, connection: Connection):
        self._connection = connection

    def get_last_datetime_transaction(self):
        """Метод позволяет узнать последней дате для 'Дозагрузка данных с момента последней даты в сервере назначения'. """
        result = self._connection.select('SELECT dt FROM transactions_denormalized ORDER BY id DESC  limit 1')
        if result:
            return result[0][0]
        return result

    def insert_data(self, rows):
        timezone = pytz.timezone('UTC')
        if len(rows) == 0:
            return
        values = []
        for row in rows:
            values.append(f"""
            ({row[0]}, FROM_UNIXTIME({datetime.datetime.timestamp(timezone.localize(row[1]))}), {row[2]}, {row[3]}, {row[4]}, '{row[5]}')
            """)
        values_str = ', '.join(values)
        query = f'INSERT INTO transactions_denormalized ( id, dt, move,  amount, idoper, name_oper ) VALUES {values_str}'
        self._connection.execute(query)
