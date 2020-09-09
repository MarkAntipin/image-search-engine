import json
from json.decoder import JSONDecodeError
from typing import List

from fastapi import (
    APIRouter, File, UploadFile, HTTPException, Depends, Query
)
from fastapi.responses import FileResponse

from core import se
from app.utils import GeneralResponse
from core.utils import get_content_type
from settings.config import Config

image_router = APIRouter()


@image_router.get('/{id}')
def get_image(id: int):
    result = se.get(idx=id)
    if result is None:
        raise HTTPException(detail=f'no such image with id: {id}', status_code=404)
    return FileResponse(
        result['path'],
        filename=result['name'],
        media_type=result['content_type'],
        headers={
            'Content-disposition': f'attachment; filename="{result["name"].encode("utf8").decode("latin-1")}"'
        })


@image_router.delete('/{id}')
def delete_image(id: int,):
    image_id = se.delete(idx=id)
    if image_id is None:
        raise HTTPException(detail=f'no such image with id: {id}', status_code=404)
    return GeneralResponse(result=image_id, message='deleted')


@image_router.post('')
def add_image(
    image: UploadFile = File(...),
):
    image_obj = image.file
    image_name = image.filename
    content_type, extension = get_content_type(image_obj, image_name)
    if content_type not in Config.ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail=f'not allowed content type {content_type}')
    image_id = se.add(
        content_type=content_type,
        extension=extension,
        image_obj=image_obj,
        image_name=image_name,
    )
    return GeneralResponse(result=image_id, message='saved', code=201)


# @image_router.post('/bulk')
# def add_image_bulk(
#     images: List[UploadFile] = File(...),
# ):
#     images_data = []
#     for image in images:
#         image_obj = image.file
#         image_name = image.filename
#         content_type, extension = get_content_type(image_obj, image_name)
#         if content_type not in Config.ALLOWED_CONTENT_TYPES:
#             raise HTTPException(
#                 status_code=400, detail=f'not allowed content type {content_type} for image: {image_name}'
#             )
#         images_data.append({
#             'content_type': content_type,
#             'extension': extension,
#             'image_name': image_name,
#             'image_obj': image_obj
#         })
#
#     image_ids = se.add_bulk(images_data=images_data)
#     return GeneralResponse(result=image_ids, message='saved', code=201)

def dict_in_params(query: str = Query(None)):
    if query is None:
        return
    try:
        query = json.loads(query)
    except JSONDecodeError:
        return False
    if not isinstance(query, dict):
        return False
    return query


@image_router.post('/search')
def search_image(
    k: int = 10,
    query: dict = Depends(dict_in_params),
    image: UploadFile = File(...)
):
    if query is False:
        raise HTTPException(detail=f'invalid query: {query}; query must be a dict', status_code=404)
    image_obj = image.file
    result = se.search(
        k=k,
        image_obj=image_obj,
        query=query
    )
    return GeneralResponse(result=result)
