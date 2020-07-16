from fastapi import FastAPI

from app.api import image_router, index_router, data_router


def create_app():
    app = FastAPI(
        title='image-search-engine'
    )

    app.include_router(prefix='/image', router=image_router, tags=['image'])
    app.include_router(prefix='/index', router=index_router, tags=['index'])
    app.include_router(prefix='/data', router=data_router, tags=['data'])

    return app


app = create_app()

