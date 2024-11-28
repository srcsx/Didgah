from playhouse.db_url import connect
from config.init import DATABASE_URL

db = connect(DATABASE_URL)

def connectDb():
    if db.is_closed():
        db.connect()

def closeDb():
    if not db.is_closed():
        db.close()

def migrateDb():
    connectDb()
    from .models import BaseModel
    db.create_tables(BaseModel.__subclasses__())
    closeDb()