import os
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    FILES_DIR = Path(BASE_DIR, 'files')
    FILES_DIR.mkdir(exist_ok=True)

    PG_CONFIG = {
        'host': os.environ.get('PG_HOST', 'localhost'),
        'port': int(os.environ.get('PG_PORT', 5432)),
        'user': os.environ.get('PG_USER'),
        'database': os.environ.get('PG_DATABASE'),
        'password': os.environ.get('PG_PASSWORD'),
    }

    DB_CONFIG = {
        'connections': {
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {**PG_CONFIG},
            }
        },
        'apps': {
            'models': {
                'models': ['app.database.models'],
                'default_connection': 'default'
            }
        }
    }
