# encoding: utf-8
from flask import Blueprint, jsonify, request
import requests
from app.libs.enums import PlatformTypeEnum
from app.libs.error_code import Detect, NotFound
from app.libs.redprint import Redprint
import re

from app.models.JieXi import JieXi
from app.validators.forms import JexForm

api = Redprint('Jiexi')


# @api.route('/get')
# def get_user():
#     return 'python 解析测试'
@api.route('/Jx', methods=['POST', 'GET'])
def create_jiexi():
    """
    :return:
    """
    name = request.form.get('name')
    print(name)
    form = JexForm().validate_for_api()
    url = ''
    promise = {
        PlatformTypeEnum.KS_URL: __request_by_ks,  # 快手平台
        PlatformTypeEnum.DY_URL: __request_by_dy  # 抖音
    }
    detect = detect_url(form.requestUrl.data)  # 确定平台
    r = validate_url(detect['type'])
    pt = promise[r](url=detect['url'])  # 调用 对应平台解析的url
    # print(pt)
    return Detect(msg=pt, )


# 检测去水印的url 来源地址  返回枚举类型
def validate_url(value):
    try:
        jx = PlatformTypeEnum(value)
        return jx
    except ValueError as e:
        raise e


# 检测请求地址
def detect_url(url):
    try:
        purls = re.findall(r"(http:\/\/|https:\/\/)((\w|=|\?|\.|\/|&|-)+)", url)[0]
        pisurl = purls[0] + purls[1]
        ks = re.compile(r"(http|https):(.*?kuaishou).(com|cn)")
        urls = ks.search(pisurl)
        if urls:
            ksu = {
                "type": 100,
                "url": url
            }
            return ksu

        dy = re.compile(r"(http|https):(.*?douyin).(com|cn)")
        dys = dy.search(pisurl)
        if dys:
            dyu = {
                "type": 200,
                "url": url
            }
            return dyu
    except Exception as e:
        raise "解析地址出现错误,请重新复制"
    pass


# 快手短视频
def __request_by_ks(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        r = requests.get(url=url, headers=headers)

        photoIds = re.compile(f"short-video/(.*?)\\?fid=")
        photoId = photoIds.search(r.url)
        # print(f"photoId", photoId)
        # 详情页的 参数
        data = {"operationName": "visionShortVideoReco",
                "variables": {"utmSource": "app_share",
                              "utmMedium": "app_share",
                              "page": "detail",
                              "photoId": "",
                              "utmCampaign": "app_share"},
                "query": "query visionShortVideoReco($semKeyword: String, $semCrowd: String, $utmSource: String, $utmMedium: String, $page: String, $photoId: String, $utmCampaign: String) {\n  visionShortVideoReco(semKeyword: $semKeyword, semCrowd: $semCrowd, utmSource: $utmSource, utmMedium: $utmMedium, page: $page, photoId: $photoId, utmCampaign: $utmCampaign) {\n    llsid\n    feeds {\n      type\n      author {\n        id\n        name\n        following\n        headerUrl\n        __typename\n      }\n      photo {\n        id\n        duration\n        caption\n        likeCount\n        realLikeCount\n        coverUrl\n        photoUrl\n        expTag\n        timestamp\n        liked\n        videoRatio\n        stereoType\n        __typename\n      }\n      tags {\n        type\n        name\n        __typename\n      }\n      canAddComment\n      __typename\n    }\n    __typename\n  }\n}\n"}
        # 设置视频的 photoId 参数
        data['variables']['photoId'] = photoId
        # 设置post 请求 返回无水印视频
        dei_url = "https://www.kuaishou.com/graphql"
        dei_response = requests.post(url=dei_url, headers=headers, data=data)
        # json 中匹配无水印视频url
        dei_json = dei_response.json()
        dei_title = dei_json['data']['visionShortVideoReco']['feeds'][0]['photo']['caption']
        dei_urls = dei_json['data']['visionShortVideoReco']['feeds'][0]['photo']['photoUrl']
        JieXi.register_by_jx("快手", url, photoId, dei_title, r.url, dei_urls)
        return dei_urls
    except NotFound as e:
        raise NotFound(msg='解析失败')


# 抖音短视频
def __request_by_dy(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        r = requests.get(url=url, headers=headers)
        # print(f"重定向后的url", r.url)
        photoIds = re.compile(f"[1-9]\\d*\\.?\\d*")
        photoId = photoIds.search(r.url)[0]
        print(photoId)
        del_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={}".format(photoId)
        del_json = requests.get(url=del_url, headers=headers)
        data = del_json.json()
        play_title = data["item_list"][0]["share_info"]['share_weibo_desc']
        play_url = data["item_list"][0]["video"]["play_addr"]["url_list"][0]
        JieXi.register_by_jx("抖音", str(url), photoId, str(play_title), str(r.url), str(play_url))
        return play_url
    except Exception as e:
        raise NotFound(msg="抖音解析失败")
