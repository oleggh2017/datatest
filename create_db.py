from settings import settings
from tests.helpers import (
    load_assets_to_source_db,
    load_struct_to_destination_db,
)


def main():
    credentials = {
        'host': settings.host,
        'port': 0,
        'database': settings.database,
        'user': settings.db_user,
        'password': settings.password,
        'autocommit': True
    }
    credentials['port'] = int(settings.source_port)
    load_assets_to_source_db(credentials)
    credentials['port'] = int(settings.destination_port)
    load_struct_to_destination_db(credentials)


if __name__ == "__main__":
    main()
