# encoding: utf-8
from .app import Flask
from flask_cors import CORS


# 注册蓝图
def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


# 注册插件
def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():  # 使用数据库上下文
        db.create_all()


def create_app():
    app = Flask(__name__)
    CORS(app, resource=r"/*")
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    # 调用蓝图
    print(app.url_map)
    register_blueprints(app)
    register_plugin(app)  # 注册数据库上下文
    return app
