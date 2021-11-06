# encoding: utf-8
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp

from app.libs.enums import ClientTypeEnum, PlatformTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form


class ClientForm(Form):
    account = StringField(validators=[DataRequired(), length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])  # 必填项目

    # 自定义验证器
    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators={
        DataRequired()
        # Regexp(r'^[A-Za-z0-9_*&$@]{6,22}$')
    })
    nickname = StringField(validators=[DataRequired(), length(min=2, max=22)])

    # 验证用户是否注册过 Email
    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValueError()


class JexForm(Form):
    requestUrl = StringField(validators=[DataRequired("解析url不能为null")])
