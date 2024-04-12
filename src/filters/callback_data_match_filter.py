import logging

from aiogram.types import CallbackQuery
from aiogram.filters import Filter


class CallbackDataMatchFilter(Filter):
    def __init__(self, callback_data: str) -> None:
        logging.info(f"code: {callback_data}")
        self.callback_data = callback_data

    async def __call__(self, callback_query: CallbackQuery) -> bool:
        return self.callback_data == callback_query.data
