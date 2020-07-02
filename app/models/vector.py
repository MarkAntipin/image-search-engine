from typing import List

from pydantic import BaseModel


class GetVectorRequest(BaseModel):
    id: int


class GetVectorResponse(BaseModel):
    result: List
