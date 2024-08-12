import os
import logging
from typing import Optional

from dotenv import load_dotenv
from dataclasses import dataclass
from sqlalchemy.engine import URL


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@dataclass
class NGINXConfig:
    APP_PREFIX: str = os.getenv("APP_NGINX_PREFIX")


@dataclass
class PostgresConfig:
    """Database connection variables."""

    name: Optional[str] = os.getenv('POSTGRES_DATABASE')
    user: Optional[str] = os.getenv('POSTGRES_USER')
    password: Optional[str] = os.getenv('POSTGRES_PASSWORD', None)
    port: int = int(os.getenv('POSTGRES_PORT', 5432))
    # host: str = os.getenv('POSTGRES_HOST', 'db')
    host: str = 'localhost'

    driver: str = 'asyncpg'
    database_system: str = 'postgresql'

    url_str = URL.create(
            drivername=f'{database_system}+{driver}',
            username=user,
            database=name,
            password=password,
            port=port,
            host=host,
        ).render_as_string(hide_password=False)


@dataclass
class MongoDBConfig:
    host: str = os.getenv("MONGODB_HOST")
    port: str = os.getenv("MONGODB_PORT")
    database: str = os.getenv("DATABASE")
    filter_collection: str = os.getenv("FILTER_COLLECTION")
    statistics_collection: str = os.getenv("STATISTICS_COLLECTION")
    url: str = f"mongodb://{host}:{port}"


@dataclass
class AppConfig:
    """Bot configuration."""

    title = "ad-olimp.org publications"
    description = "Сервис для работы с публикациями в ленту"
    version = "1.0"
    root_path = NGINXConfig.APP_PREFIX


@dataclass
class BotConfig:
    """Bot configuration."""

    token = os.getenv('TOKEN')
    technical_support = os.getenv('TECHNICAL_SUPPORT')
    admins = os.getenv("ADMINS").split()
    report_chat_id = os.getenv("REPORT_CHAT_ID")


@dataclass
class Configuration:
    """All in one configuration's class."""

    debug = bool(os.getenv('DEBUG'))
    logging_level = int(os.getenv('LOGGING_LEVEL', logging.INFO))

    postgres = PostgresConfig()
    mongo = MongoDBConfig()
    app = AppConfig()
