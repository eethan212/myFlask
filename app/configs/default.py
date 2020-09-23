import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_db_uri(db_info):
    """
    e.g. 'mysql+pymysql://root:123456@127.0.0.1:3306/test_db'
    """
    engine = db_info.get('ENGINE') or 'sqlite'
    driver = db_info.get('DRIVER') or ''
    user = db_info.get('USER') or ''
    password = db_info.get('PASSWORD') or ''
    host = db_info.get('HOST') or ''
    port = db_info.get('PORT') or ''
    db_name = db_info.get('NAME') or ''

    return f"{engine}+{driver}://{user}:{password}@{host}:{port}/{db_name}"


class Config(object):
    DEBUG = False

    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    db_info = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": '127.0.0.1',
        "PORT": 3306,
        "NAME": "test_db"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(db_info)
