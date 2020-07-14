import json

from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import FileResponse

from core import se
from app.utils import GeneralResponse
from app.database.engine import Session, get_db

image_router = APIRouter()


@image_router.get('/get/data/all')
async def get_all_images(
    db: Session = Depends(get_db)
):
    result = se.get_all_images_data(db=db)
    return GeneralResponse(result=result)


@image_router.get('/get/{id}')
async def get_image(
    id: int,
    db: Session = Depends(get_db)
):
    result = se.get_image_data(db=db, idx=id)
    if result is None:
        return GeneralResponse(result=result, message=f'no such image with id: {id}', code=201)
    return FileResponse(
        result['path'],
        filename=result['name'],
        media_type=result['content_type'],
        headers={
            'Content-disposition': f'attachment; filename="{result["name"].encode("utf8").decode("latin-1")}"'
        })


@image_router.get('/get/data/{id}')
async def get_image_data(
    id: int,
    db: Session = Depends(get_db)
):
    result = se.get_image_data(db=db, idx=id)
    if result is None:
        return GeneralResponse(result=result, message=f'no such image with id: {id}', code=201)
    return GeneralResponse(result=result)


@image_router.post('/add')
def add_image(
    image: UploadFile = File(...),
    image_data: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    if image_data:
        image_data = json.loads(image_data.file)

    image_obj = image.file
    image_name = image.filename
    image_id = se.put_in_index(
        db=db,
        image_obj=image_obj,
        image_name=image_name,
        image_data=image_data
    )
    return GeneralResponse(result=image_id, message='saved', code=201)


@image_router.post('/search')
async def search_image(
    k: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    image_obj = image.file
    result = se.search(
        db=db,
        k=k,
        image_obj=image_obj
    )
    if result is None:
        return GeneralResponse(result=result, message=f'not enough images in index for such query', code=400)
    return GeneralResponse(result=result)


@image_router.delete('/delete/{uuid}')
async def delete_image(
    id: int,
    db: Session = Depends(get_db)
):
    image_id = se.remove_from_index(db=db, idx=id)
    if image_id is None:
        return GeneralResponse(result=image_id, message=f'no such image with id: {id}', code=201)
    return GeneralResponse(result=image_id, message='deleted')
