# encoding: utf-8
# 蓝图注册
# book = Blueprint('book', __name__)
# redprint 红图注册
from app.libs.redprint import Redprint

api = Redprint('book')


@api.route('', methods=['GET'])
def get_book():
    return 'python 解析测试2'


@api.route('', methods=['POST'])
def create_book():
    return 'create 解析测试2'
