from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    CONFIG_FILE_PATH: str = "~/.bfabricpy.yml"

    HOST: str = "127.0.0.1"
    PORT: int = 8050
    DEV: bool = False

    DEVELOPER_EMAIL_ADDRESS: EmailStr = "griffin@gwcustom.com"
    BUG_REPORT_EMAIL_ADDRESS: EmailStr = "gwtools@fgcz.system"

    class Config:

        env_file = ".env"  

        # Disable reading from environment variables
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return file_secret_settings, init_settings 

# Instantiate settings
settings = Settings()