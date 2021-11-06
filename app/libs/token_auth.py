# encoding: utf-8
from flask import current_app, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from sqlalchemy.util import namedtuple

from app.libs.error_code import AuthFailed

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'scope'])


@auth.verify_password
def verify_password(token, password):
    user_info = verif_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
    return True


# 验证token是否有效 过期
def verif_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(
                         )
    except SignatureExpired:
        raise AuthFailed(
                         )
    uid = data['uid']
    ac_type = data['type']
    return User(uid, ac_type, '')
