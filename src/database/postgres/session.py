from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings import DatabaseConfig

engine = create_async_engine(
    url=DatabaseConfig.url_str,
    echo=True,
    pool_pre_ping=True
)


def new_session_maker():
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        class_=AsyncSession
    )
