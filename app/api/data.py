from typing import Dict
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from core import se
from app.utils import GeneralResponse


data_router = APIRouter()


class AddData(BaseModel):
    image_data: dict


@data_router.get('/{id}')
def get_data(id: int):
    result = se.get_data(idx=id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'no such image with id: {id}')
    return GeneralResponse(result=result)


@data_router.post('/query')
def get_data_query(query: dict):
    result = se.get_data_query(query=query)
    return GeneralResponse(result=result)


@data_router.post('/{id}')
def add_data(
    id: int,
    data: dict,
):
    image_id = se.add_data(idx=id, data=data)
    if image_id is None:
        raise HTTPException(status_code=404, detail=f'no such image with id: {id}')
    return GeneralResponse(result=id, message='saved', code=201)


# @data_router.post('/bulk')
# def add_data_bulk(
#     data: Dict[int, dict],
# ):
#     image_id = se.add_data_bulk(idx=id, data=data)
#     if image_id is None:
#         raise HTTPException(status_code=404, detail=f'no such image with id: {id}')
#     return GeneralResponse(result=id, message='saved', code=201)
