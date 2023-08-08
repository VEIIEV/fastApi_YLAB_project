import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    POSTGRES_USER: str | None = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str | None = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER: str | None = os.getenv('POSTGRES_SERVER')
    POSTGRES_DB: str | None = os.getenv('POSTGRES_DB')

    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}'
    # POSTGRES_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

    REDIS_HOST: str | None = os.getenv('REDIS_HOST')
    REDIS_PORT: str | None = os.getenv('REDIS_PORT')
    REDIS_EXPIRE_TIME: int = int(os.environ.get('REDIS_EXPIRE_TIME', 60))


# через него будем обращаться к конфигурациям
settings = Settings()
