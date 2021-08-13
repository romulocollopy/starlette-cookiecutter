from starlette.config import Config
from starlette.datastructures import URL, Secret
from pathlib import Path

config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', cast=Secret)
DATABASE_URL = config('DATABASE_URL', cast=URL)
BASE_DIR = Path(__file__).resolve().parents[2]

TESTING = config('TESTING', cast=bool, default=False)
if TESTING:
    DATABASE_URL = DATABASE_URL.replace(path=f"{DATABASE_URL.path}_test")
