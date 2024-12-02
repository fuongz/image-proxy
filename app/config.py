from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    LOG_DISABLED: bool = False
    SUPPORTED_SCHEMES: list = ["http", "https"]
    MAX_FILE_SIZE: int = 12400000
    TIMEOUT: int = 15
    SUPPORTED_FILE_TYPES: list = [
        "image/png",
        "image/jpeg",
        "image/heif",
        "image/heic",
        "image/webp",
    ]
    SUPPORTED_OUTPUT_IMAGE_TYPES: list = ["JPG", "JPEG", "PNG", "WEBP"]

    # GET CONFIG FROM .env FILE
    model_config = SettingsConfigDict(env_file=".env")
