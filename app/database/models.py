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
    data = JSONField(null=True)
    vector = ArrayField(IntegerField, dimensions=1)

    created_at = DateTimeField(default=dt.utcnow)

    class Meta:
        database = db

    @classmethod
    def get_by_query(cls, query: dict):
        keys, values = zip(*query.items())
        sql_values = keys + values

        sql = (
                'select name, content_type, path, data from image where '
                + ' and '.join('data ->> %s = %s' for _ in query) + ';'
        )
        cur = db.execute_sql(sql, sql_values)
        res = [dict(zip((x[0] for x in cur.description), row)) for row in cur.fetchall()]
        return res

    def search(cls, k: int, query: dict = None):
        pass
