# encoding: utf-8
from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db


class User(Base):
    Id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    # auth = Column(SmallInteger, default=1)
    _password = Column('password', String(255))

    # 重写 序列化对象 为json
    def keys(self):
        return ['Id', 'email', 'nickname']

    # 设置password get set 值
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod  # 静态方法
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        return {'uid': user.Id}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
