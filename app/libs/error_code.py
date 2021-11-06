# encoding: utf-8
from werkzeug.exceptions import HTTPException

from app.libs.error import APIException


class Success(APIException):
    code = 200
    msg = 'ok'
    error_code = 0


# 返回解析后的url
class Detect(Success):
    videoTitle = ''
    responseUrl = ''


class ServerError(APIException):
    code = 500
    msg = 'ok'
    error_code = 0


class ClientTypeError(APIException):
    """
    # 400 参数错误
    # 401 未授权
    # 403 禁止访问
    # 404  未找到

    # 500 服务器错误

    # 200 成功
    # 201 创建成功
    # 204 删除成功

    # 301 302 重定向
    """
    code = 400
    msg = "client is 存在"
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = '参数错误'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not_found'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    msg = 'the resource are not_found'
    error_code = 1004
