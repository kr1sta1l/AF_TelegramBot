from typing import List, Optional
from src.modules.dto.tag_dto import TagDto
from src.modules.dto.user_short_dto import UserShortDto


class ProfileDto(UserShortDto):
    user_tags: List[TagDto]
    telegram_handler: Optional[str]
    telegram_visibility: str
    email: Optional[str]
    email_visibility: str
    is_friend: Optional[bool]
