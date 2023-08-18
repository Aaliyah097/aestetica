import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DB_NAME = "db.sqlite3"
DB_URL = "sqlite:///" + os.path.join(BASE_DIR, DB_NAME)
