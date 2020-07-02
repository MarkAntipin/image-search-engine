import json
from uuid import uuid4, UUID
from datetime import datetime as dt

from shutil import copyfileobj
from pathlib import Path

from fastapi import APIRouter, Query, File, UploadFile

from app.database.models import Image
from app.utils import GeneralResponse, get_content_type
from settings.config import Config

image_router = APIRouter()


@image_router.get('/get/all')
async def get_image():
    result = [i for i in await Image.all()]
    return GeneralResponse(result=result)


@image_router.get('/get/{uuid}')
async def get_image(uuid: UUID):
    result = await Image.get(uuid=uuid).values()
    return GeneralResponse(result=result)


@image_router.get('/get/info/{uuid}')
async def get_image(uuid: UUID):
    result = await Image.get(uuid=uuid).values()
    return GeneralResponse(result=result)


@image_router.post('/add')
async def add_image(
    image: UploadFile = File(...),
    image_data: UploadFile = File(None)
):
    if image_data:
        image_data = json.loads(image_data.file)

    image_obj = image.file
    image_name = image.filename

    return GeneralResponse(result=image, message='saved', code=201)


@image_router.delete('/delete/{uuid}')
async def delete_item(uuid: UUID):
    image = await Image.get(uuid=uuid)
    image = await image.delete()
    return GeneralResponse(result=image, message='deleted', code=201)
