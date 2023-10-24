from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    # Желательно вместо str использовать SecretStr
    # для конфиденциальных данных, например, токена бота
    bot_token: SecretStr
    db_name: str
    db_user: str
    db_password: SecretStr
    db_host: str
    db_pool_min_size: int
    db_pool_max_size: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# При импорте файла сразу создастся
# и провалидируется объект конфига,
# который можно далее импортировать из разных мест
config = Settings()
