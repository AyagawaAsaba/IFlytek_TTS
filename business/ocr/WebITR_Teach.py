#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
from pprint import pprint
from IFlytek_API import *
# import time
import base64
import hashlib
import json
import requests
import cv2
import hmac
import matplotlib

import matplotlib.pyplot as plt

# 隐藏显示图片
matplotlib.use('Agg')
# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False


class ItrTeach(object):
    def __init__(self, API_ID, API_Secret, API_Key, host, In_Path, Out_Path):
        """

        :param API_ID: 应用ID
        :param API_Secret: API Secret
        :param API_Key: API密钥
        :param host: API Host (Url 接入地址)
        :param In_Path:
        :param Out_Path:
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

        # 设置当前时间
        curTime_UTC = datetime.utcnow()
        self.Date = self.HttpDate(curTime_UTC)

        # 设置测试图片文件
        self.OutPath = Out_Path
        self.AudioPath = In_Path
        self.BusinessArgs = {
            "ent": "teach-photo-print",
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
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month - 1]
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

    def Get_body(self):
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

    def Get_data(self):
        if self.API_ID == '' or self.API_Key == '' or self.API_Secret == '':
            return ''
        else:
            # 调用 __get_body 方法完成图片二进制的读取
            data = self.Get_body()
            # 调用 __get_header 方法完成图的头域的设置
            headers = self.Init_Header(data)
            # 调用 __response_url 方法从服务器获取数据
            result = self.__response_url(data, headers)
            return result

    def Process_result(self, respData):
        pprint(respData)
        print('-' * 20)
        # 以下仅用于调试
        code = str(respData['code'])
        print(code)
        if code == '0':
            data = respData['data']['region'][0]['recog']['content']
            result = {
                "flag": 'true',
                "msg": data,
            }
        else:
            result = {
                "flag": 'false',
                "msg": '请前往https://www.xfyun.cn/document/error-code?code=' + code,
            }

        return result

    def Process_latex(self, raw):
        raw = raw.replace(' ifly-latex-begin ', '$')
        raw = raw.replace(' ifly-latex-end ', '$')
        print(raw)
        result = ''
        flag = True
        while flag:
            index = 0
            while index < 80:
                index = raw.find('$\\', index + 1)
                if index == -1:
                    index = len(raw) + 1
                    flag = False
                    break
            result = result + raw[:index] + '\n'
            raw = raw[index:]
        # 去掉 X轴
        plt.xticks([])
        # 去掉 Y轴
        plt.yticks([])
        # 去掉坐标轴
        plt.axis('off')
        plt.text(-0.1, 0.8, result, ha='center', va='center', rotation='vertical', fontsize=18, style='oblique', color='black')
        plt.savefig(self.OutPath)
        plt.clf()

    def itr_teach_analysis(self):
        """
        :param Process_data_Loading: 隐性局部数据
        :param self:
        :return:
        """
        Process_data_Loading = {}
        # 调用 get_data 方法获取从服务器请求的数据
        request_data = self.Get_data()

        if request_data != '':
            # 调用 process_data 方法将数据进行解析
            Process_data_Loading = self.Process_result(request_data)
            # 调用 draw 方法根据坐标绘制错误区域
            self.Process_latex(Process_data_Loading['msg'])
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
    res = ItrTeach(
        API_ID=API_ID,
        API_Secret=API_Secret,
        API_Key=API_Key,
        host=Host,
        In_Path=r'..//..//static//images//upload//itrteach.jpg',
        Out_Path=r'..//..//static//images//upload//itrteach_result.jpg'
    ).itr_teach_analysis()
    pprint(res)
