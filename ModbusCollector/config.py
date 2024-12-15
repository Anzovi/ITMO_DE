from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    IP_ADDRESS: str
    PORT: int
    REGISTER_ADDRESS: int
    NUMBER_OF_REGISTERS: int

    API_KEY: str
    API_URL: str

    APPWRITE_API_URL: str
    APPWRITE_PROJECT: str
    APPWRITE_API_KEY: str


settings = Settings()
