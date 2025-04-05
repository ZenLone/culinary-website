from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_username: SecretStr
    db_url: SecretStr
    db_password: SecretStr
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


# При импорте файла сразу создастся 
# и провалидируется объект конфига, 
# который можно далее импортировать из разных мест
config = Settings()