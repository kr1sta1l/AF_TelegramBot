from abc import ABC, abstractmethod

from src.controllers.session import get_user_repository
from src.modules.dto import ProfileDto
from typing import List, Dict, AnyStr, Union, Optional

from src.modules.dto.user_short_dto import UserShortDto
from src.modules.dto.buildings.building_dto import BuildingDto
from src.repository.generic_repository import GenericRepository


class ApiClientInterface(ABC):
    @staticmethod
    @abstractmethod
    async def get_user_profile(requester_id: int, user_id: int, token: str = "", refresh_token: str = "",
                               user_repository: GenericRepository = get_user_repository()) -> Dict[
        AnyStr, Union[ProfileDto, None, int]]:
        ...

    @staticmethod
    @abstractmethod
    async def update_user_profile(user_id: int, profile_dto: ProfileDto, token: Optional[str] = None,
                                  refresh_token: str = "",
                                  user_repository: GenericRepository = get_user_repository()) -> bool:
        ...

    @staticmethod
    @abstractmethod
    async def get_user_friends(user_id: int, page_size: int, page: int, token: str = "", refresh_token: str = "",
                               user_repository: GenericRepository = get_user_repository()
                               ) -> Dict[AnyStr, Union[List[UserShortDto], int]]:
        ...

    @staticmethod
    @abstractmethod
    async def get_incoming_friend_requests(user_id: int, page_size: int, page: int,
                                           token: str = "", refresh_token: str = "",
                                           user_repository: GenericRepository = get_user_repository()) -> Dict[
        AnyStr, Union[List[UserShortDto], int]]:
        ...

    @staticmethod
    @abstractmethod
    async def get_outgoing_friend_requests(user_id: int, page_size: int, page: int, token: str, refresh_token: str) -> \
    Dict[AnyStr, Union[List[UserShortDto], int]]:
        ...

    @staticmethod
    @abstractmethod
    async def add_friend_request(request_user_id: int, user_id: int, token: str, refresh_token: str) -> bool:
        ...

    @staticmethod
    @abstractmethod
    async def get_list_of_buildings(page: int = 0, size: int = 10, language: str = "ru", token: str = "",
                                    refresh_token: str = "") -> List[BuildingDto]:
        ...
