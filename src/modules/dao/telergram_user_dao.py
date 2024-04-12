from sqlalchemy import Integer, BigInteger
from src.modules.dao.base_dao import BaseDao
from sqlalchemy.orm import mapped_column, Mapped


class TelegramUserDao(BaseDao):
    __tablename__ = "telegram_users"

    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, autoincrement=False, unique=True)
    state: Mapped[Integer] = mapped_column(Integer, nullable=True)
    edit_profile_message_id: Mapped[BigInteger] = mapped_column(BigInteger, nullable=True, unique=False)
    chosen_building_id: Mapped[Integer] = mapped_column(Integer, nullable=True, unique=False)
    chosen_building_message_id: Mapped[BigInteger] = mapped_column(BigInteger, nullable=True, unique=False)
    chosen_auditorium_id: Mapped[Integer] = mapped_column(Integer, nullable=True, unique=False)
