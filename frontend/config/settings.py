from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class DBSettings(BaseSettings):
    """
    db_name - название базы данных
    echo - True, если нужно выводить запросы в консоль или False
    """

    db_name: str
    echo: bool = False

    @property
    def url(self) -> str:
        """
        Возвращает строку для подключения к базе данных.
        """
        return f"sqlite:///{self.db_name}.sqlite3"


class BotSettings(BaseSettings):
    """
    token - токен бота
    """

    token: str


class RedisSettings(BaseSettings):
    """
    redis_host - хост редиса
    """

    redis_host: str


class ApiSettings(BaseSettings):
    """
    api_host - хост бэкэнда
    port - порт бэкэнда
    """

    api_host: str
    port: int

    @property
    def url(self):
        return f"{self.api_host}:{self.port}"


class Settings(BaseSettings):
    """
    db - настройки базы данных
    bot - настройки бота
    redis - настройки redis
    api - настройки бэкэнда
    """

    model_config = SettingsConfigDict(
        case_sensitive=False,
    )
    db: DBSettings = DBSettings()
    bot: BotSettings = BotSettings()
    redis: RedisSettings = RedisSettings()
    api: ApiSettings = ApiSettings()


settings = Settings()
