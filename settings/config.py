import os
from pathlib import Path

import dotenv


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent

    dotenv.load_dotenv(Path(BASE_DIR, 'settings', 'env'))

    FILES_DIR = Path(BASE_DIR, 'files')
    SQL_FUNCTIONS_DIR = Path(BASE_DIR, 'core', 'utils', 'database')

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
