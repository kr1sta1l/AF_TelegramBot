import logging

from src.config import config
from src.modules.dao import UserDao
from src.api_client import ApiClient
from src.modules.dto import UserShortDto, ProfileDto
from src.utils.localizer.localizer import localizer
from typing import AnyStr, Dict, Union, List, Optional
from src.controllers.session import get_user_repository
from src.repository.generic_repository import GenericRepository
from src.utils.user_utils import get_user_language_from_message
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from src.keyboards.reply_keyboards import get_reply_keyboard_friend_list
from src.modules.dto.users.user_in_audotorium_dto import UserInAuditoriumDto
from src.keyboards.callback_keyboard import get_incoming_requests_keyboard, get_outgoing_requests_keyboard


async def handle_incoming_requests_message_helper(message: Message, user_dao: Optional[UserDao] = None,
                                                  user_repository: GenericRepository = get_user_repository()) -> None:
    language: str = await get_user_language_from_message(message)
    if user_dao is None:
        user_dao: UserDao = await user_repository.get_one_by_whereclause(UserDao.tg_id == message.from_user.id)

    incoming_requests_list: Dict[AnyStr, Union[List[UserShortDto], int]] = await (
        ApiClient.get_incoming_friend_requests(user_dao.user_id, config.REPLY_KEYBOARD_AMOUNT_IN_PAGE, 1,
                                               user_dao.token, user_dao.refresh_token))
    friends: List[UserShortDto] = incoming_requests_list["entities"]
    if len(friends) == 0:
        await message.answer(localizer.localizations[language]["no_incoming_requests_message"],
                             reply_markup=get_reply_keyboard_friend_list())
        return
    pages_amount: int = incoming_requests_list["pages_amount"]
    need_next_page: bool = pages_amount > 1
    need_prev_page: bool = False

    page_number = 1

    inline_keyboard: InlineKeyboardMarkup = get_incoming_requests_keyboard(friends,
                                                                           "incoming_requests_page",
                                                                           page_number, need_next_page,
                                                                           need_prev_page, language)

    friends_menu_message = localizer.localizations[language]["incoming_requests_menu_message"]
    friends_list_message = localizer.localizations[language]["incoming_requests_list_message"].format(
        entities_amount=incoming_requests_list["entities_amount"], page_number=page_number, pages_amount=pages_amount)

    await message.answer(friends_menu_message,
                         reply_markup=get_reply_keyboard_friend_list())
    await message.answer(friends_list_message, reply_markup=inline_keyboard)


async def handle_outgoing_requests_message_helper(message: Message, user_dao: Optional[UserDao] = None,
                                                  user_repository: GenericRepository = get_user_repository()) -> None:
    language: str = await get_user_language_from_message(message)
    if user_dao is None:
        user_dao: UserDao = await user_repository.get_one_by_whereclause(UserDao.tg_id == message.from_user.id)

    incoming_requests_list: Dict[AnyStr, Union[List[UserShortDto], int]] = await (
        ApiClient.get_outgoing_friend_requests(user_dao.user_id, config.REPLY_KEYBOARD_AMOUNT_IN_PAGE, 1,
                                               user_dao.token, user_dao.refresh_token))
    friends: List[UserShortDto] = incoming_requests_list["entities"]
    if len(friends) == 0:
        await message.answer(localizer.localizations[language]["no_incoming_requests_message"],
                             reply_markup=get_reply_keyboard_friend_list())
        return
    pages_amount: int = incoming_requests_list["pages_amount"]
    need_next_page: bool = pages_amount > 1
    need_prev_page: bool = False

    page_number = 1

    inline_keyboard: InlineKeyboardMarkup = get_outgoing_requests_keyboard(friends,
                                                                           "outgoing_requests_page",
                                                                           page_number, need_next_page,
                                                                           need_prev_page, language)

    friends_menu_message = localizer.localizations[language]["outgoing_requests_menu_message"]
    friends_list_message = localizer.localizations[language]["outgoing_requests_list_message"].format(
        entities_amount=incoming_requests_list["entities_amount"], page_number=page_number, pages_amount=pages_amount)

    await message.answer(friends_menu_message,
                         reply_markup=get_reply_keyboard_friend_list())
    await message.answer(friends_list_message, reply_markup=inline_keyboard)


async def update_message_helper(callback_query: CallbackQuery, status_code: int, language: str) -> Optional[Message]:
    logging.warning(f"update_message_helper status_code: {status_code}")
    if status_code == 404:
        await callback_query.message.answer(localizer.localizations[language]["request_doesnt_exists"])
    elif status_code != 200:
        await callback_query.message.answer(localizer.localizations[language]["internal_server_error_message"])
    await callback_query.message.delete()
    return callback_query.message


async def update_incoming_message_helper(callback_query: CallbackQuery, status_code: int, language: str,
                                         user_dao: Optional[UserDao] = None) -> None:
    message: Optional[Message] = await update_message_helper(callback_query, status_code, language)
    await handle_incoming_requests_message_helper(message, user_dao)


async def update_outgoing_message_helper(callback_query: CallbackQuery, status_code: int, language: str,
                                         user_dao: Optional[UserDao] = None) -> None:
    message: Optional[Message] = await update_message_helper(callback_query, status_code, language)
    await handle_outgoing_requests_message_helper(message, user_dao)


async def user_in_auditorium_user_shot_list_converter(user_list: List[UserInAuditoriumDto], requester_id,
                                                      language: str) -> List[UserShortDto]:
    result: List[UserShortDto] = []
    for user in user_list:
        response: dict[AnyStr, ProfileDto | None | int] = await ApiClient.get_user_profile(requester_id, user.id,
                                                                                           language)
        if response["status_code"] != 200:
            continue
        profile_dto: ProfileDto = response["dto"]
        result.append(UserShortDto(user_id=profile_dto.user_id, user_nickname=profile_dto.user_nickname))
    return result
