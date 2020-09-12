from fastapi import FastAPI

from app.api import image_router, data_router
from app.database import migrate, Image

app = FastAPI(
    title='image-search-engine'
)
app.include_router(prefix='/image', router=image_router, tags=['image'])
app.include_router(prefix='/data', router=data_router, tags=['data'])
migrate()
Image.crate_extensions()
