from pydantic import BaseModel
from environs import Env


class LoggerSettings(BaseModel):
    level: str
    format: str
    encoding: str


class DatabaseSettings(BaseModel):
    path: str
    book_path: str


class BotSettings(BaseModel):
    token: str


class Config(BaseModel):
    logger: LoggerSettings
    database: DatabaseSettings
    bot: BotSettings


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path, override=True)
    return Config(
        logger=LoggerSettings(
            level=env.str('LOG_LEVEL'),
            format=env.str('LOG_FORMAT'),
            encoding=env.str('LOG_ENCODING'),
        ),
        database=DatabaseSettings(
            path=env.str('DATABASE_PATH'),
            book_path=env.str('BOOK_PATH'),
        ),
        bot=BotSettings(
            token=env.str('BOT_TOKEN'),
        )
    )
