from pathlib import Path

from starlette.config import Config
from starlette.datastructures import URL, Secret

config = Config(".env")

PORT = config("PORT", default='8088')
DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', cast=Secret)
DATABASE_URL = config('DATABASE_URL', cast=URL)
BASE_DIR = Path(__file__).resolve().parents[2]

TESTING = config('TESTING', cast=bool, default=False)
if TESTING:
    DATABASE_URL = DATABASE_URL.replace(path=f"{DATABASE_URL.path}_test")
