from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 2
ALGORITHM = "HS256"


class Settings:
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_SECRET_KEY = os.getenv('GITHUB_SECRET_KEY')
    GITHUB_URL = os.getenv('GITHUB_URL')

    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_SECRET_KEY = os.getenv('GOOGLE_SECRET_KEY')
    GOOGLE_URL = os.getenv('GOOGLE_URL')
setting = Settings()
