import os
from pathlib import Path

import dotenv
from fastapi.security import OAuth2PasswordBearer


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent

    dotenv.load_dotenv(Path(BASE_DIR, 'settings', 'env'))

    FILES_DIR = Path(BASE_DIR, 'files')

    ALLOWED_CONTENT_TYPES = {
        'image/jpeg',
        'image/png',
        'image/jpg',
        'image/bmp',
        'image/tiff',
        'image/gif',
    }
    PG_CONFIG = {
        'host': os.environ.get('PG_HOST', 'localhost'),
        'port': int(os.environ.get('PG_PORT', 5432)),
        'user': os.environ.get('PG_USER'),
        'database': os.environ.get('PG_DATABASE'),
        'password': os.environ.get('PG_PASSWORD'),
    }
    PG_URL = (
        f"postgres://{PG_CONFIG['user']}:{PG_CONFIG['password']}"
        f"@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"
    )

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
