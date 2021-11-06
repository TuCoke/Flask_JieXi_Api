# encoding: utf-8
from sqlalchemy import Column, Integer, String, SmallInteger, Text

from app.models.base import Base, db

"""
 解析的原始地址和去水印后的url
"""


class JieXi(Base):
    Id = Column(Integer, primary_key=True)
    _videoPlatform = Column(String(255))  # 区分视频平台
    videoTitle = Column(String(255))  # 视频的标题
    requestUrl = Column(Text(), unique=True, index=True)  # 请求的url
    request301Url = Column(Text(), unique=True, index=True)  # 重定向后url
    responseUrl = Column(Text(), index=True)  # 解析后的url
    photoId = Column(String(255))  # 视频id

    @staticmethod  # 静态方法
    def register_by_jx(_videoPlatform, requestUrl, photoId, videoTitle, request301Url, responseUrl):
        with db.auto_commit():
            jx = JieXi()
            jx._videoPlatform = _videoPlatform
            jx.photoId = photoId
            jx.videoTitle = videoTitle
            jx.requestUrl = requestUrl
            jx.request301Url = request301Url
            jx.responseUrl = responseUrl
            db.session.add(jx)
    # @property
    # def videoPlatform(self):
    #     return self._videoPlatform
    #
    # @videoPlatform.setter
    # def videoPlatform(self, raw):
    #     self._videoPlatform =
