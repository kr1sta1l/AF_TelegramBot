import re
from typing import Optional
from datetime import datetime
from aiogram.types import TelegramObject
from src.modules.dto.profile_dto import ProfileDto
from src.modules.dto.users.user_auditorium_dto import UserAuditoriumDto
from src.utils.localizer.localizer import localizer
from src.modules.enum import ProfileParametersVisibility


async def get_user_language_from_message(message: TelegramObject) -> str:
    user_language = message.from_user.language_code
    if user_language not in localizer.available_languages:
        user_language = localizer.default_language
    return user_language


def get_user_filed_with_visibility(field_value: str, visibility_s: str, language: str = "ru") -> str:
    if field_value is None:
        return localizer.localizations[language]["field_hidden"]
    return field_value


def get_user_profile_card(user_dto: ProfileDto, user_auditorium_dto: Optional[UserAuditoriumDto], language: str = "ru") -> str:
    if user_dto is None:
        return localizer.localizations[language]["user_not_found"]
    auditorium_info: str = (f"{user_auditorium_dto.auditorium.corpus.name}"
                            f"{user_auditorium_dto.auditorium.name}") if user_auditorium_dto is not None else localizer.localizations[language]["user_not_in_auditorium"]
    return localizer.localizations[language]["user_profile_card"].format(
        user_nickname_field=user_dto.user_nickname,
        user_id_filed=user_dto.user_id,
        telegram_handler_field=get_user_filed_with_visibility(user_dto.telegram_handler, user_dto.telegram_visibility),
        email_field=get_user_filed_with_visibility(user_dto.email, user_dto.email_visibility),
        auditorium_info=auditorium_info
    )


def check_hh_mm_format(time: str) -> tuple[bool, Optional[datetime]]:
    try:
        if bool(re.match(r"([01]?[0-9]|2[0-3]):[0-5][0-9]", time)):
            date_time = datetime.strptime(time, "%H:%M")
            return True, date_time
    except ValueError:
        pass
    return False, None
