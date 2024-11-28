from peewee import Model, CharField
from .db_utils import db

class BaseModel(Model):
    class Meta:
        database = db

class Prof(BaseModel):
    name = CharField()

