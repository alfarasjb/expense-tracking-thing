import os
from dotenv import load_dotenv

from src.definitions.constants import SERVER_BASE_URL

load_dotenv()


class EnvVariables:

    @classmethod
    def server_base_url(cls) -> str:
        return os.getenv(SERVER_BASE_URL, "http://localhost:3000")
