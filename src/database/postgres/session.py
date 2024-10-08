from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings import PostgresConfig

engine = create_async_engine(
    url=PostgresConfig.url_str,
    echo=False,
    pool_pre_ping=True
)


def postgres_session_maker():
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        class_=AsyncSession
    )
