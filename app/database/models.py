from datetime import datetime as dt

from sqlalchemy import (
    Column, Integer, Float, String, JSON, DateTime
)
from sqlalchemy.dialects.postgresql import ARRAY

from .engine import Base, engine


class Image(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    content_type = Column(String)
    path = Column(String)
    data = Column(JSON)
    vector = Column(ARRAY(Float))

    created_at = Column(DateTime, default=dt.utcnow)

    __tablename__ = 'images'


Base.metadata.create_all(bind=engine)
