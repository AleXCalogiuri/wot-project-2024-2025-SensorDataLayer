import sqlite3
from ..settings.settings import DATABASE_CONFIG
class Database:

    @staticmethod
    def connect():
        connection = sqlite3.connect(DATABASE_CONFIG["NAME"])
        return connection

