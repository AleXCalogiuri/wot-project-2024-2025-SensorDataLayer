import sqlite3
from app.settings.settings import DATABASE_CONFIG
class Database:

    @staticmethod
    def connect(self):
        connection = sqlite3.connect(DATABASE_CONFIG["NAME"])
        return connection

