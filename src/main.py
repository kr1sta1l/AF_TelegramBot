import asyncio
import logging
from src.database.db import get_db_settings
from src.config import config
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from src.controllers.session import init_db
from aiogram.client.bot import DefaultBotProperties

from src.routers import command_routes
from src.routers import state_routes
from src.routers import text_routes
from src.routers import callback_button_routes


def configure_dispatcher(dp: Dispatcher) -> None:
    dp.include_router(command_routes.router)
    dp.include_router(state_routes.router)
    dp.include_router(text_routes.router)
    dp.include_router(callback_button_routes.router)


async def main() -> None:
    logging.warning(get_db_settings())
    logging.warning("Initializing database...")
    await init_db()
    logging.warning("Initializing bot...")
    tg_bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logging.warning("Bot initialized. Adding dispatcher...")
    dp = Dispatcher()
    logging.warning("Dispatcher added. Configuring dispatcher...")
    configure_dispatcher(dp)
    logging.warning("Dispatcher configured. Starting bot...")
    await dp.start_polling(tg_bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
