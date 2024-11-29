from peewee import Model, CharField, ForeignKeyField, TextField
from .db_utils import db

class BaseModel(Model):
    class Meta:
        database = db


class Prof(BaseModel):
    name = CharField()


class Course(BaseModel):
    name = CharField(max_length=256)


class Comment(BaseModel):
    prof = ForeignKeyField(Prof, backref='comments')
    course = ForeignKeyField(Course, backref='comments')
    text = TextField()
    user = CharField(max_length=64) # This is the appropriate length for the SHA-256 hash algorithm
