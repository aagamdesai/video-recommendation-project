from pydantic import BaseModel
from dotenv import load_dotenv
import os


load_dotenv()


class Settings(BaseModel):
    flic_token: str = os.getenv("FLIC_TOKEN", "")
    api_base_url: str = os.getenv("API_BASE_URL", "https://api.socialverseapp.com")


settings = Settings()
