from src.modules.dto.base_dto import BaseDto


class TagDto(BaseDto):
    tag_id: str
    description: str
