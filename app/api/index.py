from fastapi import APIRouter, Depends


from core import se
from app.utils import GeneralResponse
from app.database.engine import Session, get_db

index_router = APIRouter()


@index_router.get('/reindex')
async def reindex(
    db: Session = Depends(get_db)
):
    se.reindex(db=db)
    return GeneralResponse(result=None, message='reindex started')


@index_router.get('/health')
async def check_health(
    db: Session = Depends(get_db)
):
    result = se.check_health(db=db)
    return GeneralResponse(result=result)
