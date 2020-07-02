from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.image import image_router
from settings.config import Config


def create_app():
    app = FastAPI()

    app.include_router(prefix='/image', router=image_router, tags=['item'])

    app.mount('/files', StaticFiles(directory=Config.FILES_DIR), name='files')
    return app
