from typing import Optional
import uuid
import redis

from app.authentication.domain.persistences.exceptions import BadTokenException
from app.authentication.domain.persistences.token_interface import TokenInterface


class TokenRedisPersistenceService(TokenInterface):
    def __init__(self):
        self.redis_instance = redis.Redis(host="redis", port=6379, decode_responses=True)

    def create_token(self, user_id: int) -> str:
        token = str(uuid.uuid4())
        while self.redis_instance.get(token) is not None:
            token = str(uuid.uuid4())

        self.redis_instance.set(token, str(user_id))

        return token

    def get_user_id_by_token(self, token: str) -> Optional[int]:
        result = self.redis_instance.get(token)
        if result is None:
            return None

        return int(result)

    def delete_token(self, token: str):
        result = self.redis_instance.get(token)
        if result is None:
            raise BadTokenException

        self.redis_instance.delete(token)
