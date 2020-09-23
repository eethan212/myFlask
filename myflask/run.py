from flask import Flask
from flask.helpers import get_env

from app.configs import conf_map
from app.router import blueprints, register_bps
from myflask.exts import init_exts


def create_app(env=None):
    app = Flask(__name__, instance_relative_config=True)

    # 配置
    config_obj = conf_map.get(env) or get_env()
    app.config.from_object(config_obj)

    # 配置exts
    init_exts(app)

    # bp
    register_bps(app, blueprints)

    return app
