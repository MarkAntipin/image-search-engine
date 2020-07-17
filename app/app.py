from fastapi import FastAPI

from app.api import image_router, index_router, data_router
from core import se


def startup_event():
    se.reindex()


app = FastAPI(
    title='image-search-engine'
)
app.add_event_handler('startup', startup_event)
app.include_router(prefix='/image', router=image_router, tags=['image'])
app.include_router(prefix='/index', router=index_router, tags=['index'])
app.include_router(prefix='/data', router=data_router, tags=['data'])
