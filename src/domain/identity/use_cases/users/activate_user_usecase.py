import logging

from redis.asyncio import Redis
from sqlalchemy.exc import SQLAlchemyError

from src.config.exception import ApplicationException
from src.domain.identity.schemas.users import UserStatus
from src.domain.identity.use_cases.uow import IdentityUow

logger = logging.getLogger(__name__)


class UpdateStatusUseCase:
    def __init__(self, uow: IdentityUow, redis: Redis) -> None:
        self._uow = uow
        self._redis = redis

    async def execute(self, user_pk: int, code: int) -> None:
        try:
            async with self._uow as uow:
                user = await uow.users.get_user_by_pk(pk=user_pk)
                user_code = await self._redis.get(
                    f"varification:code:{user.email}"
                )
                if user_code is None:
                    raise ApplicationException(
                        message="Code is incorrect, check code"
                    )
                if int(user_code) != code:
                    raise ApplicationException(
                        message="Code is incorrect,Check code"
                    )
                await uow.users.update_user_by_pk(
                    user_pk=user_pk,
                    user_data={"status": UserStatus.ACTIVE}
                )
                await uow.commit()
        except SQLAlchemyError as e:
            logger.error(msg=e)
            raise ApplicationException(message="Fatal error")
