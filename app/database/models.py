from uuid import UUID
from typing import Dict, List

from tortoise.models import Model
from tortoise.fields import (
    DatetimeField, IntField, CharField,
    JSONField
)


class Image(Model):
    id = IntField(pk=True)
    name = CharField(max_length=128)
    content_type = CharField(max_length=128)
    path = CharField(max_length=256)

    data = JSONField(null=True)
    vector = JSONField()

    created_at = DatetimeField(auto_now=True)

    class Meta:
        table = 'image'
