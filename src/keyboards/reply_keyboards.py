from src.utils.localizer.localizer import localizer
from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup


def get_reply_keyboard_main_menu(language: str = "ru") -> ReplyKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=localizer.localizations[language]["search_auditorium"])
            ],
            [
                KeyboardButton(text=localizer.localizations[language]["friends_list"]),
                KeyboardButton(text=localizer.localizations[language]["edit_profile"]),
            ],
        ],
        resize_keyboard=True,
    )


def get_reply_back_key_keyboard(language: str = "ru") -> ReplyKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=localizer.localizations[language]["back_key"])
            ],
        ],
        resize_keyboard=True,
    )


def get_reply_keyboard_friend_list(language: str = "ru") -> ReplyKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=localizer.localizations[language]["add_friend_button_text"])
            ],
            [
                KeyboardButton(text=localizer.localizations[language]["incoming_requests_button_text"]),
                KeyboardButton(text=localizer.localizations[language]["outgoing_requests_button_text"]),
            ],
            [
                KeyboardButton(text=localizer.localizations[language]["to_main_menu"])
            ],
        ],
        resize_keyboard=True,
    )


def get_reply_keyboard_auditorium(language: str = "ru") -> ReplyKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=localizer.localizations[language]["mark_in_auditorium"]),
            ],
            [
                KeyboardButton(text=localizer.localizations[language]["to_main_menu"])
            ],
        ],
        resize_keyboard=True,
    )


def get_reply_keyboard_edit_profile(language: str = "ru") -> ReplyKeyboardMarkup:
    if language not in localizer.available_languages:
        language = localizer.default_language

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=localizer.localizations[language]["leave_from_active_account_message"]),
            ],
            [
                KeyboardButton(text=localizer.localizations[language]["close_other_sessions_message"]),
            ],
            [
                KeyboardButton(text=localizer.localizations[language]["back_key"])
            ],
        ],
        resize_keyboard=True,
    )
