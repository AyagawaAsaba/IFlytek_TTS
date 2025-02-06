# !/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from pprint import pprint
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from IFlytek_API import *
import base64
import hashlib
import hmac
import json
import requests


class AssembleHeaderException(Exception):
    def __init__(self, message):
        self.message = message


class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema
        pass


def Process_Data(resp_data):
    # 对获取的 Json 进行换行处理
    compare_result = {}
    if 'header' not in resp_data:
        compare_result['score'] = "0"
        compare_result['desc'] = "Invalid response, missing 'header'"
        return compare_result

    code = resp_data['header']['code']

    if code > 0:
        compare_result['score'] = "0"
        compare_result['desc'] = str(code) + resp_data['header']['message']
    else:
        result = base64.b64decode(resp_data['payload']['face_compare_result']['text']).decode()
        score = float(json.loads(result)['score'])
        compare_result['score'] = "%.2f%%" % (score * 100)

        if score < 0.67:
            compare_result['desc'] = "同一个人的可能性极低"
        else:
            compare_result['desc'] = "可能是同一个人"

    return compare_result


class FaceCompare:
    def __init__(self, API_ID, API_Key, API_Secret, One_Path, Two_Path, Server_ID='s67c9c78c'):
        # 从控制台获取 API_ID, API_Key, API_Secret 以及要对比的图片路径
        # 接口ID
        self.API_ID = API_ID
        # 接口密钥
        self.API_Key = API_Key
        # 接口Secret
        self.API_Secret = API_Secret
        # 服务器ID
        self.Sever_ID = Server_ID
        # 基础 URL
        self.base_url = 'http://api.xf-yun.com/v1/private/{}'
        # 比对图像1
        self.Image_Path_One = One_Path
        # 比对图像2
        self.Image_Path_Two = Two_Path

    def __parse_url(self, request_url):
        """

        :param request_url:
        :return:
        """
        stidx = request_url.index("://")
        host = request_url[stidx + 3:]
        schema = request_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise AssembleHeaderException("invalid request url:" + request_url)
        path = host[edidx:]
        host = host[:edidx]
        u = Url(host, path, schema)
        return u

    def __assemble_ws_auth_url(self, request_url, method="GET"):
        u = self.__parse_url(request_url)
        host = u.host
        path = u.path
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        print(date)
        # date = "Thu, 12 Dec 2019 01:57:27 GMT"
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
        print(signature_origin)
        signature_sha = hmac.new(self.API_Secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = "API_Key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.API_Key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        print(authorization_origin)
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }

        return request_url + "?" + urlencode(values)

    def __gen_body(self):
        """

        :return:
        """
        with open(self.Image_Path_One, 'rb') as f:
            img1_data = f.read()
        with open(self.Image_Path_Two, 'rb') as f:
            img2_data = f.read()
        body = {
            "header": {
                "API_ID": self.API_ID,
                "status": 3
            },
            "parameter": {
                self.Sever_ID: {
                    "service_kind": "face_compare",
                    "face_compare_result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "input1": {
                    "encoding": "jpg",
                    "status": 3,
                    "image": str(base64.b64encode(img1_data), 'utf-8')
                },
                "input2": {
                    "encoding": "jpg",
                    "status": 3,
                    "image": str(base64.b64encode(img2_data), 'utf-8')
                }
            }
        }
        return json.dumps(body)

    def Get_Data(self):
        """

        :return:
        """
        # 获取人脸比对接口
        url = self.base_url.format(self.Sever_ID)
        request_url = self.__assemble_ws_auth_url(url, "POST")
        headers = {
            'content-type': 'application/json',
            'host': 'api.xf-yun.com',
            'API_ID': self.API_ID,
        }
        response = requests.post(request_url, headers=headers, data=self.__gen_body())
        print(response.status_code)
        print(response.headers)
        print(response.content.decode('utf-8'))  # 打印完整的响应内容
        resp_data = json.loads(response.content.decode('utf-8'))
        # print(resp_data)
        return resp_data

    def run(self):
        """

        :return:
        """
        # 调用 Get_data 方法从服务器请求的数据
        resp_data = self.Get_Data()
        pprint(resp_data)
        # 调用 Process_Data 方法将护具进行解析
        compare_result = Process_Data(resp_data)

        return compare_result


if __name__ == '__main__':
    One_Image_path = r'..\\..\\static\\images\\upload\\compare1.jpg'
    Two_Image_path = r'..\\..\\static\\images\\upload\\compare2.jpg'

    res = FaceCompare(
        API_ID=API_ID,
        API_Key=API_Key,
        API_Secret=API_Secret,
        One_Path=One_Image_path,
        Two_Path=Two_Image_path,
    ).run()
    pprint(res)
