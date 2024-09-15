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
    password: Optional[str] = os.getenv('POSTGRES_PASSWORD')
    port: int = int(os.getenv('POSTGRES_PORT', 5432))
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
    host: str = os.getenv("MONGO_HOST", 'db_mongo')
    port: int = os.getenv("MONGO_PORT", 27017)
    database: str = os.getenv("MONGO_INITDB_DATABASE")
    # username: str = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    # password: str = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    filter_collection: str = os.getenv("FILTER_COLLECTION")
    statistics_collection: str = os.getenv("STATISTICS_COLLECTION")
    # url: str = f"mongodb://{username}:{password}@{host}:{port}/{database}"
    url: str = f"mongodb://localhost:{port}/{database}"


@dataclass
class AppConfig:
    """Bot configuration."""

    title = "APO Training Service"
    description = "Сервис для тренировок АПО"
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
