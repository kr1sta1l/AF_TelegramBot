import logging

from src.utils.localizer.localizer import localizer
from aiogram.types.message import Message
from src.utils.user_utils import get_user_language_from_message


async def is_code_text_match(message: Message, code: str) -> bool:
    if message is None:
        return False
    user_language = await get_user_language_from_message(message)
    logging.info(f"user_language: {user_language}. \n"
                 f"message_text: {message.text.lower()}"
                 f"localized_text: {localizer.localizations[user_language][code].lower()}")
    return message.text.lower() == localizer.localizations[user_language][code].lower()
