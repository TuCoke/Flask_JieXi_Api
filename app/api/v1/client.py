# encoding: utf-8
from flask import request

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import ClientTypeError, Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    """
    注册
    登录
    参数, 校验 接收参数
    :return:
    """
    data = request.json
    form = ClientForm().validate_for_api()  # json格式的需要data=
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email,  # email  100
        ClientTypeEnum.USER_WXApp: __register_user_by_wxapp  # 小程序请求登录 105
    }
    promise[form.type.data]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm()
    if form.validate():
        User.register_by_email(form.nickname.data, form.account.data, form.secret.data)


def __register_user_by_wxapp():
    form = UserEmailForm()
    if form.validate():
        User.register_by_email(form.nickname.data, form.account.data, form.secret.data)
