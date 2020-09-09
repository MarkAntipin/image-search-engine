from typing import Tuple
from pathlib import Path
from datetime import datetime as dt

from peewee import (
    PostgresqlDatabase, AutoField, CharField, FloatField,
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
    vector = ArrayField(FloatField, dimensions=1)

    created_at = DateTimeField(default=dt.utcnow)

    class Meta:
        database = db

    @classmethod
    def model_fields(cls) -> set:
        return {
            v for v in vars(cls).keys()
            if not v.startswith('_')
            and not callable(getattr(cls, v))
        }

    @staticmethod
    def compile_sql(
            query: dict,
            model_fields: set,
            is_search: bool = False,
            vector: list = None,
            k: int = 10
    ) -> Tuple[str, list]:
        simple_fields = {}
        json_fields = {}

        for key, value in query.items():
            if key in model_fields:
                simple_fields[key] = value
            else:
                json_fields[key] = value

        if is_search:
            sql = 'select id, name, content_type, path, data, cube(vector) <-> cube(%s) as dist from image'
            sql_values = [vector] + list(simple_fields.items()) + list(json_fields.items()) + [k]
        else:
            sql = 'select id, name, content_type, path, data from image '
            sql_values = list(simple_fields.items()) + list(json_fields.items())

        if simple_fields or json_fields:
            sql += 'where '

        where_statements = [
            ' and '.join('%s = %s' for _ in simple_fields),
            ' and '.join('data ->> %s = %s' for _ in json_fields)
        ]
        sql += ' and '.join(state for state in where_statements if state)

        if is_search:
            sql += ' order by dist limit %s'

        sql += ';'
        return sql, sql_values

    @staticmethod
    def get_query_result(sql: str, sql_values: list) -> list:
        cur = db.execute_sql(sql, sql_values)
        return [dict(zip((x[0] for x in cur.description), row)) for row in cur.fetchall()]

    @classmethod
    def get_by_query(cls, query: dict) -> list:
        model_fields = cls.model_fields()
        sql, sql_values = cls.compile_sql(query, model_fields)
        return cls.get_query_result(sql, sql_values)

    @classmethod
    def search(cls, vector: list, k: int = 10, query: dict = None):
        model_fields = cls.model_fields()
        sql, sql_values = cls.compile_sql(query, model_fields, is_search=True, vector=vector, k=k)

        print(sql)
        print(sql_values)
        return cls.get_query_result(sql, sql_values)

    @staticmethod
    def crate_sql_functions():
        db.execute_sql(open(Path(Config.SQL_FUNCTIONS_DIR, 'cosine_similarity.sql'), 'r').read())

