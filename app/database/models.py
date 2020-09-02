from datetime import datetime as dt

from peewee import (
    PostgresqlDatabase, AutoField, CharField, IntegerField,
    DateTimeField, Model
)
from playhouse.postgres_ext import JSONField, ArrayField

from settings.config import Config

db = PostgresqlDatabase(**Config.PG_CONFIG)


class Image(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=128)
    content_type = CharField(max_length=128)
    path = CharField(max_length=255)
    data = JSONField()
    vector = ArrayField(IntegerField, dimensions=1)

    created_at = DateTimeField(default=dt.utcnow)

    class Meta:
        database = db
