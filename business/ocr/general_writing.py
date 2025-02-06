# -*- coding: utf-8 -*-
# !/usr/bin/python
from pprint import pprint
from IFlytek_API import *
import base64
import hashlib
import json
import requests
import time
import cv2


def process_data(data):
    """
    :param self:
    :param data:
    :return:
    """
    pprint(data)
    print("-" * 10)
    process_result = []
    # 分析获得的数据 code
    code = data['code']
    if code == '0':
        # 分析 data 中的数据
        result = data['data']['block']
        for item in result:
            if item['type'] == 'text':
                line = item['line']
                for words in line:
                    msg = ''
                    word = words['word']
                    for content in word:
                        msg += content['content'] + " "

                    process_result.append(msg)
        return process_result


class General:
    def __init__(self, API_ID, API_Key, Path):
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
        # self.API_Secret = API_Secret
        # 接口地址
        self.url = "http://webapi.xfyun.cn/v1/service/v1/ocr/general"
        # 语种设置
        self.language = 'cn|en'
        # 是否返回文本位置信息
        self.location = 'false'
        # 图片的存放路径
        self.Path = Path

    def __get_headers(self):
        curTime = str(int(time.time()))
        param = "{\"language\":\"" + self.language + "\",\"location\":\"" + self.location + "\"}"
        paramBase64 = base64.b64encode(param.encode("utf-8"))

        m2 = hashlib.md5()
        str1 = self.API_Key + curTime + str(paramBase64, "utf-8")
        m2.update(str1.encode("utf-8"))
        checkSum = m2.hexdigest()
        # 组装 Https 请求头
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-API_ID': self.API_ID,
            'X-CheckSum': checkSum,
            'Content-Type': "application/x-www-form-urlencoded; charset=utf-8",
        }
        return header

    def __get_body(self):
        """
        图片二进制数据
        :param self:
        :return:
        """
        with open(self.Path, 'rb') as f:
            img_file = f.read()
        data = {
            'image': str(base64.b64encode(img_file), "utf-8"),
        }
        # f.close()
        return data

    def __response_url(self, data, headers):
        """
        :param self:
        :param data:
        :param headers:
        :return:
        """
        result = requests.post(self.url, data=data, headers=headers)
        result = json.loads(result.content)
        # result = str(req.content, "UTF-8")
        return result

    def get_data(self):
        """
        :param self:
           :return:
           """
        # 调用 __get_body 方法完成图片二进制的读取
        data = self.__get_body()
        # 调用 __get_header 方法完成图片的头域设置
        headers = self.__get_headers()
        # 调用 __response_url 从服务器获取数据
        result = self.__response_url(data, headers)
        return result

    def general_analysis(self):
        """
        :param self:
        :return:
        """
        # 调用 get_data 方法获取从服务器请求的数据
        request_data = self.get_data()
        # 调用 process_data 方法将数据进行解析
        process_data_Loading = process_data(request_data)
        return process_data_Loading


if __name__ == "__main__":
    res = General(API_ID=API_ID, API_Key=API_Key, Path=r'..//..//static//images//upload//ocr.jpg').general_analysis()
