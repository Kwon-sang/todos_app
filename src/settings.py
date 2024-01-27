from functools import lru_cache
from typing import Optional

import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv.load_dotenv()


class DefaultSettings(BaseSettings):
    ENV_STATE: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")


class DevSettings(DefaultSettings):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class TestSettings(DefaultSettings):
    model_config = SettingsConfigDict(env_prefix="TEST_")


class ProdSetting(DefaultSettings):
    model_config = SettingsConfigDict(env_prefix="PROD_")


@lru_cache
def get_settings(env_state: str):
    configs = {"dev": DevSettings, "test": TestSettings, "prod": ProdSetting}
    return configs.get(env_state)()


setting = get_settings(DefaultSettings().ENV_STATE)
