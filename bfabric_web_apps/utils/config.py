from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    CONFIG_FILE_PATH: str = "~/.bfabricpy.yml"

    HOST: str = "127.0.0.1"
    PORT: int = 8050

    DEV: bool = False
    DEBUG: bool = False

    DEVELOPER_EMAIL_ADDRESS: EmailStr = "griffin@gwcustom.com"
    BUG_REPORT_EMAIL_ADDRESS: EmailStr = "gwtools@fgcz.system"

    #Run main pipeline config (only FGCZ specific)
    GSTORE_REMOTE_PATH: str = "/path/to/remote/gstore"
    SCRATCH_PATH: str = "/scratch/folder"
    TRX_LOGIN: str = "trxcopy@fgcz-server.uzh.ch" 
    TRX_SSH_KEY: str = "/home/user/.ssh/your_ssh_key"
    URL: str = "https:/fgcz/dummy/url"

    # Which service id to use for the charge 
    SERVICE_ID: int = 0

    # Which dataset template id to use for dataset creation
    DATASET_TEMPLATE_ID: int = 0

    class Config:

        env_file = ".env"  

        # Disable reading from environment variables
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return file_secret_settings, init_settings 

# Instantiate settings
settings = Settings()

