from uuid import UUID
from typing import Dict, List

from tortoise.models import Model
from tortoise.fields import (
    DatetimeField, IntField, CharField,
    UUIDField, JSONField,
)


class Image(Model):
    id = IntField(pk=True)
    name = CharField(max_length=128)
    content_type = CharField(max_length=128)

    uuid = UUIDField(index=True)
    image_data = JSONField(null=True)
    vector = JSONField()

    created_at = DatetimeField(auto_now=True)

    class Meta:
        table = 'image'

    @staticmethod
    async def add(
            name: str,
            content_type: str,
            image_uuid: UUID,
            vector: List[float],
            image_data: Dict = None
    ):
        image = await Image.create(
            name=name,
            content_type=content_type,
            uuid=image_uuid,
            vector=vector,
            image_data=image_data
        )
        return image.id
