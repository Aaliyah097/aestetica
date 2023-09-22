import uuid


class Config:
    DEBUG = False
    SECRET_KEY = uuid.uuid4().hex
    JSON_AS_ASCII = False
