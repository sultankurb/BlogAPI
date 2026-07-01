import logging

from redis.asyncio import Redis
from sqlalchemy.exc import SQLAlchemyError

from domain.identity.services.password_service import PasswordService
from src.config.exception import ApplicationException
from src.domain.identity.dto import UserStatus, UserUpdateData
from src.infrastructure.database import UnitOfWork

logger = logging.getLogger(__name__)


class UpdateStatusUseCase:
    def __init__(self, uow: UnitOfWork, redis: Redis) -> None:
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
                    user_data=UserUpdateData(
                        status=UserStatus.ACTIVE,
                    ),
                )
                await uow.commit()
        except SQLAlchemyError as e:
            logger.error(msg=e)
            raise ApplicationException(message="Fatal error")
