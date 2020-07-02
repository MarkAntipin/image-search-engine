import uvicorn
from tortoise.contrib.fastapi import register_tortoise

from settings.config import Config
from app.app import create_app

app = create_app()
register_tortoise(app=app, config=Config.DB_CONFIG, generate_schemas=True)


if __name__ == '__main__':
    uvicorn.run(app=app)
