from app.configs.default import Config


class DevelopmentConfig(Config):
    """生产环境"""
    DEBUG = True

    db_info = {
        "ENGINE": "sqlite",
        "DRIVER": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": '',
        "PORT": '',
        "NAME": "sqlite.db"
    }

    # SQLALCHEMY_DATABASE_URI = get_db_uri(db_info)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'
