from typing import Optional
from src.config import config
from sqlalchemy.orm import mapped_column, MappedColumn
from sqlalchemy.types import String, Integer, BigInteger, Text

from src.modules.dao.base_dao import BaseDao


class UserDao(BaseDao):
    __tablename__ = "users"
    user_id: MappedColumn[BigInteger] = mapped_column(Integer, nullable=True)
    tg_id: MappedColumn[BigInteger] = mapped_column(BigInteger, primary_key=True, nullable=False)
    token: MappedColumn[Optional[String]] = mapped_column(Text, nullable=True)
    refresh_token: MappedColumn[Optional[String]] = mapped_column(Text, nullable=True)
    language_code: MappedColumn[String] = mapped_column(String(8), nullable=True, default=config.DEFAULT_LANGUAGE,
                                                        unique=False)
