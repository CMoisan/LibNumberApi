import os

class Config:
    DEFAULT_COUNTRY_CODE = "FR"
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
    "test": TestingConfig
}

CONFIG_NAME = os.getenv("FLASK_ENV", "dev")