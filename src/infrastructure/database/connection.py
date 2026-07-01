from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
session_factory = async_sessionmaker(engine, expire_on_commit=False)
