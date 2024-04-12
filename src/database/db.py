from sqlalchemy import URL
from src.config import config
from functools import lru_cache


@lru_cache
def get_db_url():
    return URL.create(
        config.TG_DB_DIALECT,
        config.TG_DB_USERNAME,
        config.TG_DB_PASSWORD,
        config.TG_DB_HOST,
        config.TG_DB_PORT,
        config.TG_DB_DATABASE
    )


@lru_cache
def get_not_async_db_url():
    return URL.create(
        config.TG_DB_NOT_ASYNC_DIALECT,
        config.TG_DB_USERNAME,
        config.TG_DB_PASSWORD,
        config.TG_DB_HOST,
        config.TG_DB_PORT,
        config.TG_DB_DATABASE
    )


@lru_cache
def get_db_settings():
    return {
        "not_async_url": get_not_async_db_url(),
        "database_url": get_db_url(),
        "echo": config.TG_DB_ECHO,
    }
