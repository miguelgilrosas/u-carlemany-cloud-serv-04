import uuid
from typing import Optional
from tortoise.exceptions import DoesNotExist

from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistences.exceptions import UsernameAlreadyTakenException, BadTokenException
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface
from app.authentication.models import UserDB


class UserBOPostgresPersistenceService(UserBOInterface):
    async def create_user(self, user: UserBO):
        users = await UserDB.filter(**{"username": user.username})
        if len(users) > 0:
            raise UsernameAlreadyTakenException

        new_user = await UserDB(
            username=user.username,
            password=user.password,
            mail=user.mail,
            year_of_birth=user.year_of_birth
        )
        await new_user.save()

        user.id = new_user.id

    async def get_user_by_username(self, username: str) -> Optional[UserBO]:
        try:
            user = await UserDB.get(username=username)

        except DoesNotExist:
            return None

        return UserBO(
            id=user.id,
            username=user.username,
            password=user.password,
            mail=user.mail,
            year_of_birth=user.year_of_birth
        )

    async def get_user_by_id(self, user_id: int) -> Optional[UserBO]:
        try:
            user = await UserDB.get(id=int(user_id))

        except DoesNotExist:
            return None

        return UserBO(
            id=user.id,
            username=user.username,
            password=user.password,
            mail=user.mail,
            year_of_birth=user.year_of_birth
        )
