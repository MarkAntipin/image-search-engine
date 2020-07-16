from fastapi import APIRouter, Depends


from core import se
from app.utils import GeneralResponse
from app.database.engine import Session, get_db

index_router = APIRouter()


@index_router.get('/reindex')
async def reindex():
    se.reindex()
    return GeneralResponse(result=None, message='reindex finished')


@index_router.get('/health')
async def check_health(
    db: Session = Depends(get_db)
):
    is_healthy = se.check_health(db=db)
    message = 'everything is good'
    if is_healthy is False:
        message = 'something is wrong'
    return GeneralResponse(result=is_healthy, message=message)
