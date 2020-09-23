from app.configs.default import Config


class ProductionConfig(Config):
    """生产环境"""
    DEBUG = True

    db_info = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": '127.0.0.1',
        "PORT": 3306,
        "NAME": "test_db"
    }
