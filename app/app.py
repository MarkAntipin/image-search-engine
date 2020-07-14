from fastapi import FastAPI

from app.api import image_router, index_router


def create_app():
    app = FastAPI()

    app.include_router(prefix='/image', router=image_router, tags=['image'])
    app.include_router(prefix='/index', router=index_router, tags=['index'])

    return app
