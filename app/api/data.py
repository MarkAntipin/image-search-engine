from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException

from core import se
from app.database.models import Image as ImageModel
from app.utils import GeneralResponse


data_router = APIRouter()


class AddData(BaseModel):
    image_data: dict


@data_router.get('/{id}')
def get_data(
    id: int,
):
    result = se.get_image_data(db=db, idx=id)
    if result is None:
        raise HTTPException(status_code=404, detail=f'no such image with id: {id}')
    return GeneralResponse(result=result)


@data_router.post('/{id}')
def add_data(
    id: int,
    data: AddData,
):
    db_image = db.query(ImageModel).filter(ImageModel.id == id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail=f'no such image with id: {id}')
    db_image.data = data.image_data
    db.commit()
    return GeneralResponse(result=id, message='saved', code=201)
