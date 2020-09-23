from app import views


def register_bps(app, bps):
    for item in bps:
        app.register_blueprint(item.get('bp'), url_prefix=item.get('url_prefix'))


# 蓝图注册
blueprints = [
    {'bp': views.demo.bp, 'url_prefix': '/api'},
]
