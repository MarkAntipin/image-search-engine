from fastapi import APIRouter, Depends, HTTPException


from core import se
from app.utils import GeneralResponse
from app.database.engine import Session, get_db

index_router = APIRouter()


@index_router.get('/reindex')
def reindex():
    if se.is_indexing:
        raise HTTPException(status_code=400, detail='indexing in progress')
    se.reindex()
    return GeneralResponse(result=None, message='reindex finished')


@index_router.get('/health')
def check_health(
    db: Session = Depends(get_db)
):
    if se.is_indexing:
        raise HTTPException(status_code=400, detail='indexing in progress')
    healthy_message, is_healthy = se.check_health(db=db)
    return GeneralResponse(result=is_healthy, message=healthy_message)
