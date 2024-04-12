from enum import Enum


class ProfileParametersVisibility(Enum):
    PUBLIC = 0
    FRIENDS = 1
    PRIVATE = 2

    @staticmethod
    def get_visibility_by_str(visibility: str) -> 'ProfileParametersVisibility':
        return {
            "PUBLIC": ProfileParametersVisibility.PUBLIC,
            "FRIENDS": ProfileParametersVisibility.FRIENDS,
            "PRIVATE": ProfileParametersVisibility.PRIVATE
        }[visibility.upper()]

    @staticmethod
    def get_visibility_by_int(visibility: int) -> 'ProfileParametersVisibility':
        return {
            ProfileParametersVisibility.PUBLIC.value: ProfileParametersVisibility.PUBLIC,
            ProfileParametersVisibility.FRIENDS.value: ProfileParametersVisibility.FRIENDS,
            ProfileParametersVisibility.PRIVATE.value: ProfileParametersVisibility.PRIVATE
        }[visibility]

    @staticmethod
    def get_str_by_visibility(visibility: 'ProfileParametersVisibility') -> str:
        return {
            ProfileParametersVisibility.PUBLIC: "PUBLIC",
            ProfileParametersVisibility.FRIENDS: 'FRIENDS',
            ProfileParametersVisibility.PRIVATE: "PRIVATE"
        }[visibility]

    @staticmethod
    def get_emoji_by_visibility(visibility: 'ProfileParametersVisibility') -> str:
        return {
            ProfileParametersVisibility.PUBLIC: '🌍',
            ProfileParametersVisibility.FRIENDS: '👥',
            ProfileParametersVisibility.PRIVATE: '🔒'
        }[visibility]

    @staticmethod
    def get_next_visibility(visibility: 'ProfileParametersVisibility') -> 'ProfileParametersVisibility':
        return ProfileParametersVisibility.get_visibility_by_int((visibility.value + 1) % 3)
