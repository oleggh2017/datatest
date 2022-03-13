from pydantic import (
    BaseSettings,
)


class Settings(BaseSettings):
    host: str = 'localhost'
    database: str = 'sandbox'
    db_user: str = 'etl'
    password: str = 'etl_contest'

    source_port: int = 4441
    destination_port: int = 4442
    # main_sleep_time: int = 60 * 60 * 2
    main_sleep_time: int = 1


settings = Settings()