# encoding: utf-8
from enum import Enum


class ClientTypeEnum(Enum):
    USER_EMAIL = 100  # email 注册  登录
    USER_MOBILE = 101  #
    USER_WXApp = 105  # 微信小程序
    USER_OTHER = 107  # 其他


# 短视频枚举
class PlatformTypeEnum(Enum):
    KS_URL = 100
    DY_URL = 200
