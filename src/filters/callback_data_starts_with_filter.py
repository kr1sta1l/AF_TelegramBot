from aiogram.types import CallbackQuery
from aiogram.filters import Filter


class CallbackDataStartsWithFilter(Filter):
    def __init__(self, callback_data: str) -> None:
        self.callback_data = callback_data

    async def __call__(self, callback_query: CallbackQuery) -> bool:
        return callback_query.data.startswith(self.callback_data)
