import time

import datetime
from connection import Connection
from settings import settings
from data_repository import SourceDataRepository, DestinationDataRepository


class TransferService:


    def __init__(self):
        self._src_connection = Connection(host=settings.host, db_user=settings.db_user, password=settings.password,
                   db_name=settings.database, port=settings.source_port)
        self._dst_connection = Connection(host=settings.host, db_user=settings.db_user, password=settings.password,
                                    db_name=settings.database, port=settings.destination_port)
        self._src_data_repository = SourceDataRepository(self._src_connection)
        self._dst_data_repository = DestinationDataRepository(self._dst_connection)

    def transfer_part(self, start_date, end_date):
        rows = self._src_data_repository.get_data(datetime.datetime.timestamp(start_date),
                                                  datetime.datetime.timestamp(end_date))
        self._dst_data_repository.insert_data(rows)

    def transfer(self):
        start_date = self._dst_data_repository.get_last_datetime_transaction()
        if not start_date:
            start_date = datetime.datetime(2022, 1, 1, 0, 0, 0)
        end_date = datetime.datetime(2022, 1, 2, 0, 0, 0)

        while start_date <= end_date:
            self.transfer_part(start_date, start_date + datetime.timedelta(minutes=59, seconds=59))
            start_date = start_date + datetime.timedelta(hours=1)

