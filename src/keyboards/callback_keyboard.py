import logging
from datetime import datetime
from typing import List, AnyStr, Optional

from src.api_client import ApiClient
from src.modules.dto import ProfileDto
from src.modules.dto import UserShortDto
from src.utils.localizer.localizer import localizer
from src.modules.dto.buildings.building_dto import BuildingDto
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from src.modules.dto.users.users_in_auditorium_dto import UsersInAuditoriumDto
from src.modules.dto.buildings.building_auditoriums_dto import BuildingAuditoriumsDto
from src.modules.enum.profile_parameters_visibility import ProfileParametersVisibility


def get_callback_keyboard_main_menu(language: str = "ru") -> InlineKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=localizer.localizations[language]["search_auditorium"],
                                     callback_data="search_auditorium")
            ],
            [
                InlineKeyboardButton(text=localizer.localizations[language]["friends_list"],
                                     callback_data="friends_list"),
                InlineKeyboardButton(text=localizer.localizations[language]["edit_profile"],
                                     callback_data="edit_profile"),
            ],
        ],
    )


def get_callback_keyboard_edit_profile(profile_dto: ProfileDto, language: str = "ru") -> InlineKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language
    email_visibility = ProfileParametersVisibility.get_visibility_by_str(profile_dto.email_visibility)
    telegram_visibility = ProfileParametersVisibility.get_visibility_by_str(profile_dto.telegram_visibility)
    # logging.info()

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=profile_dto.user_nickname,
                                     callback_data=f"edit_name"),
            ],
            [
                InlineKeyboardButton(text=profile_dto.email,
                                     callback_data="info_message_email"),
                InlineKeyboardButton(text=ProfileParametersVisibility.get_emoji_by_visibility(email_visibility),
                                     callback_data="edit_visibility_email_" + str(email_visibility.value))
            ],
            [
                InlineKeyboardButton(text=profile_dto.telegram_handler,
                                     callback_data="info_telegram_email"),
                InlineKeyboardButton(text=ProfileParametersVisibility.get_emoji_by_visibility(telegram_visibility),
                                     callback_data="edit_visibility_telegram_" + str(telegram_visibility.value))
            ],
            [
                InlineKeyboardButton(text=localizer.localizations[language]["confirm_editing"],
                                     callback_data="confirm_editing"),
            ]
        ],
    )


def get_list_user_short_dto_keyboard(friend_list: List[UserShortDto], callback_prefix: str, page_number: int = 1,
                                     add_next_button: bool = False,
                                     add_prev_button: bool = False, language: str = "ru") -> InlineKeyboardMarkup:
    return get_callback_keyboard_class_list(friend_list, "user_nickname", "user_info",
                                            "user_id", callback_prefix, page_number,
                                            add_next_button, add_prev_button, language)


def get_add_friend_button(user_id: int, language: str = "ru") -> InlineKeyboardButton:
    if language not in localizer.available_languages:
        language = localizer.default_language

    return InlineKeyboardButton(text=localizer.localizations[language]["add_friend_message"],
                                callback_data=f"add_friend_{user_id}")


def get_remove_friend_button(user_id: int, language: str = "ru") -> InlineKeyboardButton:
    if language not in localizer.available_languages:
        language = localizer.default_language

    return InlineKeyboardButton(text=localizer.localizations[language]["remove_friend_message"],
                                callback_data=f"remove_friend_{user_id}")


def get_complain_button(user_id: int, language: str = "ru") -> InlineKeyboardButton:
    if language not in localizer.available_languages:
        language = localizer.default_language

    return InlineKeyboardButton(text=localizer.localizations[language]["complain_message"],
                                callback_data=f"complain_{user_id}")


def get_remove_message_button(language: str = "ru") -> InlineKeyboardButton:
    if language not in localizer.available_languages:
        language = localizer.default_language

    return InlineKeyboardButton(text=localizer.localizations[language]["remove_message"],
                                callback_data="remove_message_keyboard")


def get_callback_keyboard_user_info(profile_dto: Optional[ProfileDto], language: str = "ru"
                                    ) -> Optional[InlineKeyboardMarkup]:
    if language not in localizer.available_languages:
        language = localizer.default_language
    if profile_dto is None:
        return None

    result_keyboard: List[List[InlineKeyboardButton]] = []
    if profile_dto.is_friend is not None:
        if profile_dto.is_friend:
            result_keyboard.append([get_remove_friend_button(profile_dto.user_id, language)])
        else:
            result_keyboard.append([get_add_friend_button(profile_dto.user_id, language)])
    result_keyboard.append([get_complain_button(profile_dto.user_id, language)])
    result_keyboard.append([get_remove_message_button(language)])
    return InlineKeyboardMarkup(inline_keyboard=result_keyboard)



def get_callback_keyboard_class_list(class_list: List, text_field: str,
                                     callback_prefix: str,
                                     callback_postfix_field: str,
                                     callback_page_prefix: str,
                                     page_number: int = 1,
                                     add_next_button: bool = False,
                                     add_prev_button: bool = False, language: str = "ru") -> InlineKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language

    keyboard = []
    for class_object in class_list:
        keyboard.append([InlineKeyboardButton(text=getattr(class_object, text_field),
                                              callback_data=f"{callback_prefix}_"
                                                            f"{getattr(class_object, callback_postfix_field)}")])

    add_navigation_buttons(keyboard, page_number, callback_page_prefix, add_next_button, add_prev_button, language)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def add_navigation_buttons(keyboard: List[List[InlineKeyboardButton]], page_number: int, callback_page_prefix: str,
                           add_next_button: bool, add_prev_button: bool, language: str = "ru") -> None:
    if language not in localizer.available_languages:
        language = localizer.default_language

    if add_prev_button:
        keyboard.append([InlineKeyboardButton(text=localizer.localizations[language]["prev_page"],
                                              callback_data=f"{callback_page_prefix}_{page_number - 1}")])
    if add_next_button:
        if add_prev_button:
            keyboard[-1].append(InlineKeyboardButton(text=localizer.localizations[language]["next_page"],
                                                     callback_data=f"{callback_page_prefix}_{page_number + 1}"))
        else:
            keyboard.append([InlineKeyboardButton(text=localizer.localizations[language]["next_page"],
                                                  callback_data=f"{callback_page_prefix}_{page_number + 1}")])


def get_callback_keyboard_auditorium_list(building_auditoriums_dto: BuildingAuditoriumsDto,
                                          start_interval_time: datetime, end_interval_time: datetime,
                                          noise_presence: bool, page_number: int = 1,
                                          add_next_button: bool = False,
                                          add_prev_button: bool = False, language: str = "ru") -> InlineKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language
    keyboard: List[List[InlineKeyboardButton]] = []
    for auditorium in building_auditoriums_dto.auditoriums:
        keyboard.append([InlineKeyboardButton(
            text=f"{auditorium.corpus.name}{auditorium.name} | {auditorium.type} | {auditorium.silent_users_amount} : {auditorium.noise_users_amount}",
            callback_data=f"auditorium_info_{auditorium.id}")])
    button_postfix = f"{building_auditoriums_dto.building.id}_{start_interval_time.strftime('%Y-%m-%d-%H-%M')}_" \
                     f"{end_interval_time.strftime('%Y-%m-%d-%H-%M')}_{1 if noise_presence else 0}"

    if add_prev_button:
        keyboard.append([InlineKeyboardButton(text=localizer.localizations[language]["prev_page"],
                                              callback_data=f"auditorium_list_{page_number - 1}_{button_postfix}")])
    if add_next_button:
        next_button_callback = f"auditorium_list_{page_number + 1}_{button_postfix}"
        if add_prev_button:
            keyboard[-1].append(InlineKeyboardButton(text=localizer.localizations[language]["next_page"],
                                                     callback_data=next_button_callback))
        else:
            keyboard.append([InlineKeyboardButton(text=localizer.localizations[language]["next_page"],
                                                  callback_data=next_button_callback)])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_callback_keyboard_users_in_auditorium_list(users_in_auditorium_dto: UsersInAuditoriumDto,
                                                         requester_id: int,
                                                         page_number: int = 1,
                                                         add_next_button: bool = False,
                                                         add_prev_button: bool = False,
                                                         language: str = "ru") -> InlineKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language
    keyboard = []
    silent_message = localizer.localizations[language]["silent"]
    noise_message = localizer.localizations[language]["noice"]
    logging.warning(users_in_auditorium_dto.users)
    for user in users_in_auditorium_dto.users:
        silence_message = silent_message if user.silent_status else noise_message
        response: dict[AnyStr, ProfileDto | None | int] = await ApiClient.get_user_profile(requester_id, user.id,
                                                                                           language)
        if response["response"] != 200:
            button_text = f"{user.id} | {silence_message}"
        else:
            profile_dto: ProfileDto = response["dto"]
            button_text = f"{profile_dto.user_nickname} | {silence_message}"
        keyboard.append([InlineKeyboardButton(
            text=button_text,
            callback_data=f"user_info_{user.id}")])
    logging.warning(users_in_auditorium_dto.users)
    add_navigation_buttons(keyboard, page_number, "users_in_auditorium_list",
                           add_next_button, add_prev_button, language)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_callback_building_keyboard(building_dto: BuildingDto, language: str = "ru",
                                   noise_presence: bool = True) -> InlineKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language
    noice_presence = "noice_presence_active" if noise_presence else "noice_presence_inactive"
    noise_presence_callback = 0
    keyboard = [[InlineKeyboardButton(text=localizer.localizations[language]["set_start_interval_time"],
                                      callback_data=f"set_interval_time_start_{building_dto.id}")],
                [InlineKeyboardButton(text=localizer.localizations[language]["set_end_interval_time"],
                                      callback_data=f"set_interval_time_end_{building_dto.id}")],
                [InlineKeyboardButton(text=localizer.localizations[language][noice_presence],
                                      callback_data=f"set_noise_presence_{str(noise_presence_callback)}")],
                [InlineKeyboardButton(text=localizer.localizations[language]["confirm_interval_time"],
                                      callback_data=f"confirm_interval_time_{building_dto.id}")]
                ]
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard)


def get_outgoing_requests_keyboard(outgoing_request_list: List[UserShortDto], callback_prefix: str,
                                   page_number: int = 1,
                                   add_next_button: bool = False,
                                   add_prev_button: bool = False, language: str = "ru") -> InlineKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language
    keyboard: List[List[InlineKeyboardButton]] = []
    for user in outgoing_request_list:
        keyboard.append([InlineKeyboardButton(
            text=f"{user.user_nickname}",
            callback_data=f"user_info_{user.user_id}"),
            InlineKeyboardButton(text=localizer.localizations[language]["cancel_request"],
                                 callback_data=f"cancel_request_{user.user_id}")])
    add_navigation_buttons(keyboard, page_number, callback_prefix, add_next_button,
                           add_prev_button, language)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_incoming_requests_keyboard(incoming_requests_list: List[UserShortDto], callback_prefix: str,
                                   page_number: int = 1,
                                   add_next_button: bool = False,
                                   add_prev_button: bool = False, language: str = "ru") -> InlineKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language
    keyboard: List[List[InlineKeyboardButton]] = []
    for user in incoming_requests_list:
        keyboard.append([InlineKeyboardButton(
            text=f"{user.user_nickname}",
            callback_data=f"user_info_{user.user_id}"),
            InlineKeyboardButton(text=localizer.localizations[language]["confirm_request"],
                                 callback_data=f"accept_request_{user.user_id}"),
            InlineKeyboardButton(text=localizer.localizations[language]["cancel_request"],
                                 callback_data=f"reject_request_{user.user_id}")])
    add_navigation_buttons(keyboard, page_number, callback_prefix, add_next_button,
                           add_prev_button, language)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_exit_auditorium_keyboard(user_id: int, auditorium_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language
    keyboard: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text=f"{localizer.localizations[language]['leave_auditorium']}",
                callback_data=f"leave_auditorium_{user_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_callback_keyboard_auditorium(language: str = "ru") -> InlineKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=localizer.localizations[language]["mark_in_auditorium"]),
            ]
        ],
    )
