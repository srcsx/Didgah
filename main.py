from database.db_utils import migrateDb
from app.bot_utils import run

def init():
    migrateDb()
    run()

init()