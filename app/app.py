# encoding: utf-8
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder


from app.libs.error_code import ServerError
from datetime import date


class JSONEncoder(_JSONEncoder):
    """重写json 支持序列化对象"""

    def default(self, o):
        # 不能访问类里面的变量  o.__dict__
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()


class Flask(_Flask):
    """替换为自己的json序列号"""
    json_encoder = JSONEncoder


