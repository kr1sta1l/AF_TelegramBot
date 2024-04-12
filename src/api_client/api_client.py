import httpx
import random
import logging
from datetime import datetime
from src.modules.dao import UserDao
from src.modules.dto import ProfileDto
from src.config import config, create_url
from typing import List, Dict, AnyStr, Union, Optional

from src.modules.dto.auditoriums.auditorium_users_dto import AuditoriumUsersDto
from src.modules.dto.user_short_dto import UserShortDto
from src.controllers.session import get_user_repository
from src.modules.dto.buildings.building_dto import BuildingDto
from src.repository.generic_repository import GenericRepository
from src.api_client.api_client_interface import ApiClientInterface
from src.modules.dto.users.user_auditorium_dto import UserAuditoriumDto
from src.modules.dto.buildings.building_auditoriums_dto import BuildingAuditoriumsDto
from src.modules.dto.users.users_in_auditorium_dto import UsersInAuditoriumDto


class ApiClient(ApiClientInterface):
    @staticmethod
    async def get_user_profile(requester_id: int, user_id: int, token: str = "", refresh_token: str = "") -> Dict[
        AnyStr, Union[ProfileDto, None, int]]:

        user_profile_response: Dict[AnyStr, Union[ProfileDto, int, None]] = \
            await ApiClient.get_user_profile_caller(requester_id, user_id, token)
        if user_profile_response["response"] == 200:
            return {"dto": user_profile_response["dto"], "response": 200}
        elif user_profile_response["response"] == 401 or user_profile_response["response"] == -1:
            token: Optional[str] = await ApiClient.refresh_token(requester_id, token, refresh_token)
            if token is None:
                return {"dto": None, "response": 401}
            user_profile_response = await ApiClient.get_user_profile_caller(requester_id, user_id, token)
            if user_profile_response["response"] == 200:
                return {"dto": user_profile_response["dto"], "response": 200}
        return {"dto": None, "response": user_profile_response["response"]}

    @staticmethod
    async def update_user_profile(user_id: int, profile_dto: ProfileDto, token: Optional[str] = None,
                                  refresh_token: str = "", user_repository: GenericRepository = get_user_repository()
                                  ) -> int:
        response_code: int = await ApiClient.update_user_profile_nickname(user_id, profile_dto.user_nickname, token)
        if response_code == 401 or response_code == -1:
            token = await ApiClient.refresh_token(user_id, token, token)
            if token is None:
                return 401
        response_code = await ApiClient.update_user_profile_nickname(user_id, profile_dto.user_nickname, token)
        return response_code

        body = {"telegramVisibility": profile_dto.telegram_visibility,
                "emailVisibility": profile_dto.email_visibility}
        async with httpx.AsyncClient() as client:
            response = await client.patch(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/profile/visibility"),
                                          json=body,
                                          headers={"Authorization": f"Bearer {token}", "userid": str(user_id)})

            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, token)
                if token is None:
                    return 401
                response = await client.patch(
                    create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/profile/visibility"),
                    json=body, headers={"Authorization": f"Bearer {token}", "userid": str(user_id)})
            return response.status_code

    @staticmethod
    async def get_user_friends(user_id: int, page_size: int, page: int, token: str = "", refresh_token: str = "",
                               user_repository: GenericRepository = get_user_repository()) -> Dict[
        AnyStr, Union[List[UserShortDto], int]]:

        async with httpx.AsyncClient() as client:
            response = await client.get(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends",
                                                   [("userid", user_id), ("page", page), ("size", page_size)]))

            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return {"entities": [], "pages_amount": 0, "entities_amount": 0, "entities_in_page": 0}
                response = await client.get(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends",
                                                       [("userid", user_id), ("page", page), ("size", page_size)]))
                pages_amount = int(response.headers["pages_amount"])
                entities_amount = int(response.headers["entities_amount"])
                entities_in_page = len(response.json())
            user_list = response.json()
            result_list = []
            for user in user_list:
                result_list.append(UserShortDto(**user))
            return {"entities": result_list,
                    "pages_amount": pages_amount,
                    "entities_amount": entities_amount,
                    "entities_in_page": entities_in_page}

    @staticmethod
    async def get_incoming_friend_requests(user_id: int, page_size: int, page: int,
                                           token: str = "", refresh_token: str = "",
                                           user_repository: GenericRepository = get_user_repository()
                                           ) -> Dict[AnyStr, Union[List[UserShortDto], int]]:
        if page_size <= 0 or page <= 0:
            raise ValueError(f"Page size and page must be positive numbers (now page_size={page_size}, page={page})")

        async with httpx.AsyncClient() as client:
            response = await client.get(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/incoming",
                                                   [("userid", user_id), ("page", page), ("size", page_size)]))
            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return {"entities": [], "pages_amount": 0, "entities_amount": 0, "entities_in_page": 0}
                response = await client.get(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/incoming",
                                                       [("userid", user_id), ("page", page), ("size", page_size)]))
            pages_amount = int(response.headers["pages_amount"])
            entities_amount = int(response.headers["entities_amount"])
            entities_in_page = len(response.json())
            user_list = response.json()
            result_list = []
            for user in user_list:
                result_list.append(UserShortDto(**user))
            return {"entities": result_list,
                    "pages_amount": pages_amount,
                    "entities_amount": entities_amount,
                    "entities_in_page": entities_in_page}

    @staticmethod
    async def get_outgoing_friend_requests(user_id: int, page_size: int, page: int, token: str, refresh_token: str,
                                           user_repository: GenericRepository = get_user_repository()) -> \
            Dict[
                AnyStr, Union[List[UserShortDto], int]]:
        logging.info(f"User_id: {user_id}, page_size: {page_size}, page: {page}")
        if page_size <= 0 or page <= 0:
            raise ValueError(f"Page size and page must be positive numbers (now page_size={page_size}, page={page})")
        user_dao: Optional[UserDao] = await user_repository.get_one_by_whereclause(UserDao.user_id == user_id)
        url = create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/outgoing",
                         [("userid", user_id), ("page", page), ("size", page_size)])
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return {"entities": [], "pages_amount": 0, "entities_amount": 0, "entities_in_page": 0}
                response = await client.get(url, headers={"Authorization": f"Bearer {token}"})
                if response.status_code == 401:
                    return {"entities": [], "pages_amount": 0, "entities_amount": 0, "entities_in_page": 0}
                await user_repository.update(user_dao)

            pages_amount = int(response.headers["pages_amount"])
            entities_amount = int(response.headers["entities_amount"])
            entities_in_page = len(response.json())
            user_list = response.json()
            result_list = []
            for user in user_list:
                result_list.append(UserShortDto(**user))
            return {"entities": result_list,
                    "pages_amount": pages_amount,
                    "entities_amount": entities_amount,
                    "entities_in_page": entities_in_page}

    @staticmethod
    async def add_friend_request(request_user_id: int, user_id: int, token: str, refresh_token: str) -> int:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/request",
                                                    [("userid", user_id), ("requesterid", request_user_id)]),
                                         headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(request_user_id, token, refresh_token)
                if token is None:
                    return 401
                response = await client.post(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/request",
                                                        [("userid", user_id), ("requesterid", request_user_id)]),
                                             headers={"Authorization": f"Bearer {token}"})
            return response.status_code

    @staticmethod
    async def get_list_of_buildings(page: int = 0, size: int = 10, language: str = "ru", token: str = "",
                                    refresh_token: str = "") -> Dict[AnyStr, Union[List[BuildingDto], int]]:
        headers = {"Authorization": f"Bearer {token}"}
        url = create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/buildings",
                         [("languageCode", language), ("page", page), ("size", size)])
        logging.warning(f"get_list_of_buildings_url: {url}")
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(0, token, refresh_token)
                if token is None:
                    return {"entities_amount": 0,
                            "pages_amount": 0,
                            "entities": None}
            response = await client.get(url, headers={"Authorization": f"Bearer {token}"})

            logging.warning(str(response.headers))
            # headers = {"entities_amount": str(list_of_buildings["buildings_amount"]),
            #            "pages_amount": str(list_of_buildings["pages_amount"])}
            return {"entities_amount": int(response.headers["entities_amount"]),
                    "pages_amount": int(response.headers["pages_amount"]),
                    "entities": [BuildingDto(**building) for building in response.json()]}

    @staticmethod
    async def get_building(building_id: int, language="ru", token: str = "", refresh_token: str = ""
                           ) -> Optional[BuildingDto]:
        if not isinstance(building_id, int):
            return None
        headers = {"Authorization": f"Bearer {token}"}
        url = create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, f"/buildings/{building_id}",
                         [("languageCode", language)])
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(0, token, refresh_token)
                if token is None:
                    return None
                response = await client.get(url, headers={"Authorization": f"Bearer {token}"})
            if response.status_code == 200:
                return BuildingDto(**response.json())
            return None

    @staticmethod
    async def get_list_of_auditoriums_in_building(building_id: int, interval_start: datetime, interval_end: datetime,
                                                  noise_users_presence: bool = True,
                                                  page: int = 0, size: int = 10,
                                                  language: str = "ru",
                                                  token: str = "", refresh_token: str = ""
                                                  ) -> Dict[AnyStr, Union[None, BuildingAuditoriumsDto, int]]:
        if not isinstance(building_id, int):
            return {"status_code": -1,
                    "auditoriums_amount": 0,
                    "entities_amount": 0,
                    "pages_amount": 0,
                    "entities": None}
        interval_start_str = interval_start.strftime("%Y-%m-%d-%H-%M")
        interval_end_str = interval_end.strftime("%Y-%m-%d-%H-%M")

        url = create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, f"/auditorium/building/{building_id}",
                         [("languageCode", language), ("page", page), ("size", size),
                          ("intervalStart", interval_start_str),
                          ("intervalEnd", interval_end_str), ("noiseUsersPresence", noise_users_presence)])

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers={"Authorization": f"Bearer {token}"})

            if response.status_code == 401:
                token = await ApiClient.refresh_token(0, token, refresh_token)
                if token is None:
                    return {"status_code": 401,
                            "auditoriums_amount": 0,
                            "entities_amount": 0,
                            "pages_amount": 0,
                            "entities": None}
                response = await client.get(url, headers={"Authorization": f"Bearer {token}"})

            if response.status_code == 200:
                return {"status_code": 200,
                        "auditoriums_amount": int(response.headers["auditoriums_amount"]),
                        "entities_amount": int(response.headers["entities_amount"]),
                        "pages_amount": int(response.headers["pages_amount"]),
                        "entities": BuildingAuditoriumsDto(**response.json())}
            return {"status_code": response.status_code,
                    "auditoriums_amount": 0,
                    "entities_amount": 0,
                    "pages_amount": 0,
                    "entities": None}

    @staticmethod
    async def get_auditoriums_with_users(auditorium_id, page: int = 0, size: int = 10,
                                         language: str = "ru",
                                         token: str = "", refresh_token: str = ""
                                         ) -> Dict[AnyStr, Union[None, UsersInAuditoriumDto, int]]:
        if not isinstance(auditorium_id, int):
            return {"status_code": -1,
                    "auditoriums_amount": 0,
                    "entities_amount": 0,
                    "pages_amount": 0,
                    "entities": None}

        url = create_url(config.AUDITORIUM_HOST, config.AUDITORIUM_PORT, f"/auditorium/info/{auditorium_id}/users",
                         [("languageCode", language), ("page", page), ("size", size)])

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return {"status_code": 200,
                        "entities_amount": int(response.headers["entities_amount"]),
                        "pages_amount": int(response.headers["pages_amount"]),
                        "entities": UsersInAuditoriumDto(**response.json())}
            return {"status_code": response.status_code,
                    "entities_amount": 0,
                    "pages_amount": 0,
                    "entities": None}

    @staticmethod
    async def refresh_token(user_id: int, token: str, refresh_token: str,
                            user_repository: GenericRepository = get_user_repository()
                            ) -> Optional[str]:
        user_dao: Optional[UserDao] = await user_repository.get_one_by_whereclause(UserDao.user_id == user_id)
        if user_dao is None:
            return None
        async with httpx.AsyncClient() as client:
            response = await client.post(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/auth/refresh"),
                                         json={"token": refresh_token})
            response.raise_for_status()
            d_response = response.json()
            if response.status_code == 200:
                user_dao.token = d_response["token"]
                user_dao.refresh_token = d_response["refresh_token"]
                try:
                    await user_repository.update(user_dao)
                except Exception as e:
                    logging.error(f"Error while updating user dao: {e}")
                    return None
                return response.json()["token"]
        return None

    @staticmethod
    async def get_user_profile_caller(requester_id: int, user_id: int, token: str = "") -> Dict[
        AnyStr, Union[ProfileDto, int, None]]:
        logging.warning(f"Requester_id: {requester_id}, User_id: {user_id}")
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/profile",
                                                       [("userid", user_id)]),
                                            headers=headers)
            except Exception as e:
                logging.error(f"Error while creating url to get info about user: {e}")
                return {"response": -1,
                        "dto": None}
            if response.status_code == 200:
                return {"response": 200,
                        "dto": ProfileDto(**response.json())}
        return {"response": response.status_code,
                "dto": None}

    @staticmethod
    async def update_user_profile_nickname(user_id: int, nickname: str, token: str, refresh_token: str) -> int:
        body = {"nickname": nickname}
        headers = {"Authorization": f"Bearer {token}", "userid": str(user_id)}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.patch(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/profile",
                                                         [("userid", user_id)]),
                                              json=body, headers=headers)
            except Exception as e:
                logging.error(f"Error while creating url to get info about user: {e}")
                return -1
            logging.warning(str(response.headers))
        return response.status_code

    @staticmethod
    async def update_user_profile_visibility(user_id: int, token: str, refresh_token: str, body) -> int:
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.patch(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/profile",
                                                         [("userid", user_id)]),
                                              json=body, headers=headers)
            except Exception as e:
                logging.error(f"Error while creating url to get info about user: {e}")
                return -1
            logging.warning(str(response.headers))
        return response.status_code
        pass

    @staticmethod
    async def get_in_account(user_id: int, username: str, email: str, code: str) -> int:
        sign_up_code = await ApiClient.sign_up_tg(user_id, username, email, code)
        if sign_up_code == 200:
            return 200
        sign_in_code = await ApiClient.sign_in_tg(user_id, username, email, code)
        return sign_in_code

    @staticmethod
    async def sign_up_tg(user_id: int, username: str, email: str, code: str) -> int:
        headers = {"Authorization": f"Bearer {config.TG_BOT_SESSION_TOKEN}"}
        body = {
            "emailCode": code,
            "email": email,
            "telegramHandle": f"@{username}" if username != "" else "",
            "nickname": "New User" if username == "" else f"@{username}"
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/signup/tg"),
                                             json=body, headers=headers)
            except Exception as e:
                logging.error(f"Error while sign up user: {e}")
                return -1
            logging.warning(str(response.headers))
        return await ApiClient.sign_in_out_postfix(response, user_id)

    @staticmethod
    async def sign_in_tg(user_id: int, username: str, email: str, code: str) -> int:
        headers = {"Authorization": f"Bearer {config.TG_BOT_SESSION_TOKEN}"}
        body = {
            "emailCode": code,
            "email": email,
            "telegramHandle": f"@{username}" if username != "" else "",
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/signin/tg"),
                                             json=body, headers=headers)
            except Exception as e:
                logging.error(f"Error while sign up user: {e}")
                return -1
            logging.warning(str(response.headers))
        return await ApiClient.sign_in_out_postfix(response, user_id)

    @staticmethod
    async def sign_in_out_postfix(response, user_id, user_repository: GenericRepository = get_user_repository()) -> int:
        if response.status_code != 200:
            return response.status_code
        response_body = response.json()
        user_dao: UserDao = await user_repository.get_one_by_whereclause(UserDao.tg_id == user_id)
        user_dao.token = response_body["jwt"]
        user_dao.refresh_token = response_body["refresh_token"]
        user_dao.user_id = response_body["userId"]
        await user_repository.update(user_dao)
        return response.status_code

    @staticmethod
    async def add_to_friend(request_id: int, user_id: int, token: str, refresh_token: str) -> int:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/accept",
                                                    [("userid", user_id), ("requesterid", request_id)]),
                                         headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return 401
                response = await client.post(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/accept",
                                                        [("userid", user_id), ("requesterid", request_id)]),
                                             headers={"Authorization": f"Bearer {token}"})
            return response.status_code

    @staticmethod
    async def decline_request(request_id: int, user_id: int, token: str, refresh_token: str) -> int:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.delete(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/decline",
                                                      [("userid", user_id), ("requesterid", request_id)]),
                                           headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return 401
                response = await client.delete(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/decline",
                                                          [("userid", user_id), ("requesterid", request_id)]),
                                               headers={"Authorization": f"Bearer {token}"})
            return response.status_code

    @staticmethod
    async def reject_friend_request(request_id: int, user_id: int, token: str, refresh_token: str) -> int:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.delete(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/reject",
                                                      [("userid", user_id), ("requesterid", request_id)]),
                                           headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return 401
                response = await client.delete(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/reject",
                                                          [("userid", user_id), ("requesterid", request_id)]),
                                               headers={"Authorization": f"Bearer {token}"})
            return response.status_code

    @staticmethod
    async def remove_from_friend(request_id: int, user_id: int, token, refresh_token) -> int:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.delete(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/remove",
                                                      [("userid", user_id), ("requesterid", request_id)]),
                                           headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return 401
                response = await client.delete(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/remove",
                                                          [("userid", user_id), ("requesterid", request_id)]),
                                               headers={"Authorization": f"Bearer {token}"})
            return response.status_code

    @staticmethod
    async def accept_friend(request_id: int, user_id: int, token: str, refresh_token: str) -> int:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/accept",
                                                    [("userid", user_id), ("requesterid", request_id)]),
                                         headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return 401
                response = await client.post(create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/friends/accept",
                                                        [("userid", user_id), ("requesterid", request_id)]),
                                             headers={"Authorization": f"Bearer {token}"})
            return response.status_code

    @staticmethod
    async def add_user_into_auditorium(user_id: int, auditorium_id: int, silent_status: bool,
                                       token: str, refresh_token: str, language: str = "ru"
                                       ) -> Optional[UserAuditoriumDto]:
        url = create_url(config.AUDITORIUM_HOST, config.AUDITORIUM_PORT, "/auditorium/users/add_user",
                         [("languageCode", language), ("userid", user_id)])
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"auditoriumId": auditorium_id, "silentStatus": silent_status},
                                         headers={"Authorization": f"Bearer {token}"})
            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return None
                response = await client.post(url, json={"auditoriumId": auditorium_id, "silentStatus": silent_status},
                                             headers={"Authorization": f"Bearer {token}"})
        if response.status_code != 200:
            return None
        return UserAuditoriumDto(**response.json())

    @staticmethod
    async def remove_user_from_auditorium(user_id: int, token: str, refresh_token: str, language: str = "ru") -> int:
        url = create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/auditorium/remove_user",
                         [("languageCode", language)])
        headers = {"userid": str(user_id),
                   "Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return 401
                response = await client.delete(url, headers={"userid": str(user_id),
                                                             "Authorization": f"Bearer {token}"})
        return response.status_code

    @staticmethod
    async def complain_request(requester_id: int, user_id: int, complain: str, token: str, refresh_token: str,
                               language: str = "ru") -> int:
        url = create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/complain",
                         [("languageCode", language), ("userid", requester_id)])
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={"complainedUserId": user_id, "complain": complain}, headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(requester_id, token, refresh_token)
                if token is None:
                    return 401
                response = await client.post(url, json={"complainedUserId": user_id, "complain": complain},
                                             headers={"Authorization": f"Bearer {token}"})
        return response.status_code

    @staticmethod
    async def leave_from_active_account(user_id: int, token, refresh_token: str) -> int:
        url = create_url(config.GATEWAY_HOST, config.GATEWAY_PORT, "/leave", [])
        headers = {"userid": str(user_id)}
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return 401
                response = await client.delete(url, headers={"userid": str(user_id)})
        return response.status_code

    @staticmethod
    async def get_auditorium_where_user_located_in(user_id: int, token: str, refresh_token: str, language: str = "ru"
                                                   ) -> Dict[AnyStr, Union[UserAuditoriumDto, None, int]]:
        headers = {"userid": str(user_id)}
        url = create_url(config.AUDITORIUM_HOST, config.AUDITORIUM_PORT, "/auditorium/user",
                         [("languageCode", language)])
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 401:
                token = await ApiClient.refresh_token(user_id, token, refresh_token)
                if token is None:
                    return {"dto": None, "code": 401}
                response = await client.get(url, headers={"userid": str(user_id)})
        if response.status_code == 200:
            return {"dto": UserAuditoriumDto(**response.json()), "code": 200}
        return {"dto": None, "code": response.status_code}
