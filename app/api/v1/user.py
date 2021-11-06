# encoding: utf-8
from flask import Blueprint, jsonify

from app.libs.redprint import Redprint
from app.libs.token_auth import auth

# user = Blueprint('user', __name__)
from app.models.user import User

api = Redprint('user')


# @api.route('/get')
# def get_user():
#     return 'python 解析测试'


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def create_user(uid):
    """
    :return:
    """
    user = User.query.get_or_404(uid)
    return jsonify(user)


@api.route('', methods=['GET'])
def test_user():
    return "api创建成功"
