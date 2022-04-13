#此為上傳AWS之設定檔
import os
from datetime import timedelta
class Config_AWS(object):
    DEBUG = False
    JSON_AS_ASCII=False
    TEMPLATES_AUTO_RELOAD=True
    JSON_SORT_KEYS=False
    JWT_SECRET_KEY=os.urandom(8)
    JWT_TOKEN_LOCATION=["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
    SECRET_KEY=os.urandom(8)


# class ProductionConfig(Config):
#     DEBUG = False


# class StagingConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class DevelopmentConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class TestingConfig(Config):
#     TESTING = True