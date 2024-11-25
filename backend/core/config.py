from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()
BASE_DIR = Path(__file__).parent.parent


class AuthJWTSettings(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    access_token_expire_minutes: int = 30
    algorithm: str = "RS256"


class DBSettings(BaseSettings):
    """
    Класс для настройки параметров подключения к базе данных.
    """

    db_host: str
    db_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    echo: bool = False

    @property
    def url(self) -> str:
        """
        Возвращает строку для подключения к базе данных.
        """
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.db_host}:{self.db_port}/{self.postgres_db}"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )
    db: DBSettings = DBSettings()
    auth_jwt: AuthJWTSettings = AuthJWTSettings()


settings = Settings()
