import logging

from aiogram.types import Message
from aiogram.filters import Filter
from src.utils.messages_match_utils import is_code_text_match


class TextCodeMatchFilter(Filter):
    def __init__(self, code: str) -> None:
        logging.info(f"code: {code}")
        self.code = code

    async def __call__(self, message: Message) -> bool:
        logging.info(f"TextCodeMatchFilter called. Code: {self.code}. Message: {message.text}")
        return await is_code_text_match(message, self.code)
