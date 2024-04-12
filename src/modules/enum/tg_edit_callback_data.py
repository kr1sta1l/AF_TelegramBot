from enum import Enum


class TgEditCallbackData(Enum):
    """Telegram edit callback data enum."""
    EDIT_NAME = "edit_name"
    EDIT_EMAIL = "edit_email"
    EDIT_EMAIL_VISIBILITY = "edit_email_visibility"
    EDIT_TELEGRAM = "edit_telegram"
    EDIT_TELEGRAM_VISIBILITY = "edit_telegram_visibility"
    CONFIRM_EDITING = "confirm_editing"
