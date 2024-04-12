from src.modules.dto.base_dto import BaseDto


class UserShortDto(BaseDto):
    user_id: int
    user_nickname: str
