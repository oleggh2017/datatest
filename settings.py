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


settings = Settings()