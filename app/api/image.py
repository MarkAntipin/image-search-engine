import json

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from core import se
from app.utils import GeneralResponse

image_router = APIRouter()


@image_router.get('/get/all')
async def get_all_images():
    result = await se.get_all_images_data()
    return GeneralResponse(result=result)


@image_router.get('/get/{id}')
async def get_image(id: int):
    result = await se.get_image_data(idx=id)
    if result is None:
        return GeneralResponse(result=result, message=f'no such image id {id}', code=201)
    return FileResponse(
        result.path,
        filename=result.name,
        media_type=result.content_type,
        headers={
            'Content-disposition': f'attachment; filename="{result.name.encode("utf8").decode("latin-1")}"'
        })


@image_router.get('/get/data/{id}')
async def get_image_data(id: int):
    result = await se.get_image_data(idx=id)
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
    image_id = await se.put_in_index(
        image_obj=image_obj, image_name=image_name, image_data=image_data
    )

    return GeneralResponse(result=image_id, message='saved', code=201)


@image_router.post('/search')
async def search_image(
    image: UploadFile = File(...),
):
    image_obj = image.file
    result = se.search(image_obj=image_obj)

    return GeneralResponse(result=result, message='saved', code=201)


@image_router.delete('/delete/{uuid}')
async def delete_item(idx: int):
    image_id = await se.remove_from_index(idx)
    return GeneralResponse(result=image_id, message='deleted', code=201)
