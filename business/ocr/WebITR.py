#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
from pprint import pprint
from IFlytek_API import *
import base64
import hashlib
import json
import requests
import time
import cv2
import hmac


# def process_data(data):
#     """
#     :param self:
#     :param data:
#     :return:
#     """
#     pprint(data)
#     print("-" * 10)
#     process_result = []
#     # 分析获得的数据 code
#     code = data['code']
#     if code == '0':
#         # 分析 data 中的数据
#         result = data['data']['block']
#         for item in result:
#             if item['type'] == 'text':
#                 line = item['line']
#                 for words in line:
#                     msg = ''
#                     word = words['word']
#                     for content in word:
#                         msg += content['content'] + " "
#
#                     process_result.append(msg)
#         return process_result

class WebITR(object):
    def __init__(self, API_ID, API_Secret, API_Key, host, In_Path, Out_Path):
        """
        :param API_ID:
        :param API_Key:
        :param API_Secret:
        :param Path:
        """
        # 应用ID
        self.API_ID = API_ID
        # API密钥
        self.API_Key = API_Key
        # API Secret    todo:通用文字识别需调用 Secret，但手写识别不需要调用
        self.API_Secret = API_Secret
        # API Host (Url 接入地址)
        self.host = host
        # RequestUri (Url 接入后缀)
        self.RequestUri = "/v2/itr"
        # 接口地址
        self.url = "https://" + host + self.RequestUri
        # 访问类型
        self.HttpMethod = "POST"
        # 访问编码
        self.Algorithm = "hmac-sha256"
        # Http 类型
        self.HttpProto = "HTTP/1.1"
        # 语种设置
        # self.language = 'cn|en'
        # 是否返回文本位置信息
        # self.location = 'false'
        # # 图片的存放路径
        # self.Path = Path

        # 设置当前时间
        curTime_UTC = datetime.utcnow()
        self.Date = self.HttpDate(curTime_UTC)

        # 设置测试图片文件
        self.OutPath = Out_Path
        self.AudioPath = In_Path
        self.BusinessArgs = {
            "ent": "math-arith",
            "aue": "raw",
        }

    def ImgRead(self, path):
        with open(path, 'rb') as fo:
            return fo.read()

    def HashLib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def HttpDate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.

        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month, dt.year, dt.hour, dt.minute, dt.second)

    def GenerateSignature(self, digest):
        signatureStr = "host: " + self.host + "\n"
        signatureStr += "date: " + self.Date + "\n"
        signatureStr += self.HttpMethod + " " + self.RequestUri + " " + self.HttpProto + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.API_Secret.encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def Init_Header(self, data):
        digest = self.HashLib_256(data)
        # print(digest)
        sign = self.GenerateSignature(digest)
        authHeader = 'API_Key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.API_Key, self.Algorithm, sign)
        # print(AuthHeader)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def get_body(self):
        audioData = self.ImgRead(self.AudioPath)
        content = base64.b64encode(audioData).decode(encoding='utf-8')
        Post_data = {
            "common": {"API_ID": self.API_ID},
            "business": self.BusinessArgs,
            "data": {
                "image": content,
            }
        }
        body = json.dumps(Post_data)
        # print(body)
        return body

    def __response_url(self, data, headers):
        """

        :param data:
        :param headers:
        :return:
        """
        result = requests.post(self.url, data=data, headers=headers, timeout=8)
        result = json.loads(result.content)
        # result = str(req.content, "UTF-8")
        return result

    def get_data(self):
        if self.API_ID == '' or self.API_Key == '' or self.API_Secret == '':
            return ''
        else:
            # 调用 __get_body 方法完成图片二进制的读取
            data = self.get_body()
            # 调用 __get_header 方法完成图的头域的设置
            headers = self.Init_Header(data)
            # 调用 __response_url 方法从服务器获取数据
            result = self.__response_url(data, headers)
            return result

    def process_result(self, respData):
        pprint(respData)
        print('-' * 20)
        itr_Result = {
            'right': 0,
            'wrong': 0,
            'flag': 'true',
        }
        points = []
        # 以下仅用于调试
        code = str(respData['code'])
        print(code)
        if code == '0':
            data = respData['data']
            for line_info in data['ITRResult']['multi_line_info']['imp_line_info']:
                if line_info['total_score'] == 0:

                    imp_line_rect = line_info['imp_line_rect']
                    points.append(
                        {
                            'x1': imp_line_rect['left_up_point_x'],
                            'y1': imp_line_rect['left_up_point_y'],
                            'x2': imp_line_rect['right_down_point_x'],
                            'y2': imp_line_rect['right_down_point_y'],
                        }
                    )
                    itr_Result['wrong'] = itr_Result['wrong'] + 1
                else:
                    itr_Result['right'] = itr_Result['right'] + 1
        else:
            itr_Result['flag'] = 'false'
            itr_Result['msg'] = '请前往https://www.xfyun.cn/document/error-code?code=' + code

        return points, itr_Result

    def draw(self, points):
        image = cv2.imread(self.AudioPath)
        for point in points:
            first_point = (point['x1'], point['y1'])
            last_point = (point['x2'], point['y2'])
            cv2.rectangle(image, first_point, last_point, (0, 0, 255), 2)
        cv2.imwrite(self.OutPath, image)

    def itr_analysis(self):
        """
        :param self:
        :return:
        """
        Process_data_Loading = {}
        # 调用 get_data 方法获取从服务器请求的数据
        request_data = self.get_data()

        if request_data != '':
            # 调用 process_data 方法将数据进行解析
            points, Process_data_Loading = self.process_result(request_data)
            # 调用 draw 方法根据坐标绘制错误区域
            self.draw(points)
        else:
            process_data = {
                'flag': 'false',
                'msg': 'API_ID 或 API_Key 或 API_Secret 为空！请打开 demo 代码，填入相关信息'
            }
        return Process_data_Loading


if __name__ == "__main__":
    # 接口域名
    Host = "rest-api.xfyun.cn"
    # 初始化类
    res = WebITR(
        API_ID=API_ID,
        API_Secret=API_Secret,
        API_Key=API_Key,
        host=Host,
        In_Path=r'..//..//static//images//upload//itr.jpg',
        Out_Path='..//..//static//images//upload//itr_result.jpg'
    ).itr_analysis()
    print(res)
