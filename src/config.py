import os
from pathlib import Path
from pydantic import Field
from typing import Optional, Tuple, List, Any
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # model_config = SettingsConfigDict(env_file=Path(os.path.dirname(os.path.realpath(__file__))) / '.env',
    #                                   env_file_encoding='utf-8')

    TG_BOT_SESSION_TOKEN: str = Field("TG_BOT_SESSION_TOKEN", env="TG_BOT_SESSION_TOKEN")
    BOT_TOKEN: str = Field("TOKEN", validation_alias="BOT_TOKEN", env="BOT_TOKEN")
    DEFAULT_LANGUAGE: str = Field("ru", validation_alias="DEFAULT_LANGUAGE", env="DEFAULT_LANGUAGE")
    AVAILABLE_LANGUAGES: str = Field("ru|en", validation_alias="AVAILABLE_LANGUAGES", env="AVAILABLE_LANGUAGES")
    LOCALIZER_PATH: str = Field("path", validation_alias="LOCALIZER_PATH", env="LOCALIZER_PATH")

    GATEWAY_HOST: str = Field("GATEWAY_HOST", env="GATEWAY_HOST")
    GATEWAY_PORT: int = Field(8000, env="GATEWAY_PORT")

    TG_STOMP_HOST: str = Field("0.0.0.0", env="TG_STOMP_HOST")
    TG_STOMP_PORT: int = Field(8010, env="TG_STOMP_PORT")
    TG_DB_DIALECT: str = Field("TG_DB_DIALECT", validation_alias="TG_DB_DIALECT", env="TG_DB_DIALECT")
    TG_DB_NOT_ASYNC_DIALECT: str = Field("TG_DB_NOT_ASYNC_DIALECT", validation_alias="TG_DB_NOT_ASYNC_DIALECT",
                                         env="TG_DB_NOT_ASYNC_DIALECT")
    TG_DB_USERNAME: str = Field("TG_DB_USERNAME", validation_alias="TG_DB_USERNAME", env="TG_DB_USERNAME")
    TG_DB_PASSWORD: str = Field("TG_DB_PASSWORD", validation_alias="TG_DB_PASSWORD", env="TG_DB_PASSWORD")
    TG_DB_HOST: str = Field("TG_DB_HOST", validation_alias="TG_DB_HOST", env="TG_DB_HOST")
    TG_DB_PORT: str = Field("TG_DB_PORT", validation_alias="TG_DB_PORT", env="TG_DB_PORT")
    TG_DB_DATABASE: str = Field("TG_DB_PORT", validation_alias="TG_DB_DATABASE", env="TG_DB_DATABASE")
    TG_DB_ECHO: bool = Field("TG_DB_PORT", validation_alias="TG_DB_ECHO", env="TG_DB_ECHO")
    AVAILABLE_EMAILS_DOMAINS: str = Field("hse.ru|edu.hse.ru", validation_alias="AVAILABLE_EMAILS_DOMAINS",
                                          env="AVAILABLE_EMAILS_DOMAINS")
    REPLY_KEYBOARD_AMOUNT_IN_PAGE: int = Field(10, validation_alias="REPLY_KEYBOARD_AMOUNT_IN_PAGE",
                                               env="REPLY_KEYBOARD_AMOUNT_IN_PAGE")
    AUDITORIUM_HOST: str = Field("0.0.0.0", validation_alias="AUDITORIUM_HOST", env="AUDITORIUM_HOST")
    AUDITORIUM_PORT: int = Field(8000, validation_alias="AUDITORIUM_PORT", env="AUDITORIUM_PORT")


def create_url(host: str, port: int, path: str, query: Optional[List[Tuple[str, Any]]] = None
               ) -> str:
    url = f"http://{host}:{port}"
    if path:
        url += f"{path}"
    if query:
        url += "?"
        for i, (key, value) in enumerate(query):
            if isinstance(value, bool):
                value = str(value).lower()
            url += f"{key}={value}"
            if i != len(query) - 1:
                url += "&"
    return url


config = Config()
