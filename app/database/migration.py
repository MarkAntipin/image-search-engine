from peeweedbevolve import evolve

from .models import db


def migrate():
    evolve(db, interactive=False)
