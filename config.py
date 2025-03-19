import os
import yaml

# Chargement de la configuration depuis le fichier YAML
with open("config.yaml", "r", encoding="utf-8") as file:
    CONFIG_DATA = yaml.safe_load(file)

class Config:
    DEBUG = False
    TESTING = False
    COUNTRY_CONFIG = CONFIG_DATA["countries"]  # Chargement des pays depuis le YAML

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
