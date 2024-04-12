from cachetools import TTLCache
from aiogram.filters import Filter
from aiogram.types import TelegramObject
from src.modules.dao.user_dao import UserDao
from src.controllers.session import get_user_repository
from src.repository.generic_repository import GenericRepository

cache = TTLCache(maxsize=100, ttl=30)


class UserInDatabaseFilter(Filter):
    def __init__(self) -> None:
        self.repository: GenericRepository = get_user_repository()

    async def __call__(self, telegram_object: TelegramObject) -> bool:
        user_id = int(telegram_object.from_user.id)

        cached_user_available = cache.get(user_id)
        if cached_user_available is not None:
            cache[user_id] = cached_user_available
            return cached_user_available
        user = await self.repository.get_one_by_whereclause(UserDao.tg_id == user_id)
        cache[user_id] = user is not None
        return user is not None
