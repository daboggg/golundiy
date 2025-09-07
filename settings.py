from environs import Env
from dataclasses import dataclass


@dataclass
class Custom:
    max_subscribe: int

@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Database:
    async_db_url: str
    db_url: str
    db_echo: bool
    db_name: str


@dataclass
class Settings:
    bots: Bots
    db: Database
    custom: Custom


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        custom=Custom(
            max_subscribe=env.int("MAX_SUBSCRIBE"),
        ),
        bots=Bots(
            bot_token=env.str('BOT_TOKEN'),
            admin_id=env.int('ADMIN_ID')
        ),
        db=Database(
            async_db_url=env.str('DATABASE_URL_ASYNC'),
            db_url=env.str('DATABASE_URL'),
            db_echo=env.bool('DB_ECHO'),
            db_name=env.str('DB_NAME')
        )
    )


settings = get_settings('.env')