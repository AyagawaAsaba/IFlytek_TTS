# !/usr/bin/python
# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import time as t
from pprint import pprint
from IFlytek_API import *
import requests


class FaceDesc:
    def __init__(self, label):
        self.label = label

    def Concert_age(self):
        age = int(self.label)

        if age == 0:
            result = '0-1'

        elif age == 1:
            result = '2-5'

        elif age == 2:
            result = '6-10'

        elif age == 3:
            result = '11-15'

        elif age == 4:
            result = '16-20'

        elif age == 5:
            result = '21-25'

        elif age == 6:
            result = '31-40'

        elif age == 7:
            result = '41-50'

        elif age == 8:
            result = '51-60'

        elif age == 9:
            result = '61-80'

        elif age == 10:
            result = '80以上'

        elif age == 11:
            result = '其他'

        else:
            result = "图片文件有误，或者格式不支持（Gif 图不支持）"

        return result

    def Concert_score(self):
        score = int(self.label)

        if score == 0:
            result = '漂亮'

        elif score == 1:
            result = "好看"

        elif score == 2:
            result = "普通"

        elif score == 3:
            result = "难看"

        elif score == 4:
            result = "其他"

        elif score == 5:
            result = "半人脸"

        elif score == 6:
            result = "多人"

        else:
            result = "图片文件错误，或者格式不支持（Gif 图不支持）"

        return result

    def Concert_sex(self):
        sex = int(self.label)

        if sex == 0:
            result = "男人"

        elif sex == 1:
            result = "女人"

        elif sex == 2:
            result = "难以分辨"

        else:
            result = "图片文件错误，或者格式不支持（Gif 图不支持）"

        return result

    def Concert_expression(self):
        expression = int(self.label)

        if expression == 0:
            result = "其他（非人脸表情图片）"

        elif expression == 1:
            result = "其他表情"

        elif expression == 2:
            result = "喜悦"

        elif expression == 3:
            result = "愤怒"

        elif expression == 4:
            result = "悲伤"

        elif expression == 5:
            result = "惊恐"

        elif expression == 6:
            result = "厌恶"

        elif expression == 7:
            result = "中性"

        else:
            result = "图片文件错误，或者格式不支持（Gif 图不支持）"

        return result


class FaceFeature:
    def __init__(self, API_ID, API_Key, Path):
        """

        :param API_ID:
        :param API_Key:
        :param Path:
        """
        # 接口ID
        self.API_ID = API_ID
        # 接口密钥
        self.API_Key = API_Key
        # 基础 Url
        self.base_url = "http://tupapi.xfyun.cn/v1/"
        # 图片路径
        self.Image_Path = Path
        # 图片路径模式    Todo: 0-本地图片; 1-网络图片
        self.mode = 0

    def __get_headers(self):
        """

        :return:
        """
        # 根据图片路径模式， 构建 Param
        # 本地图片
        if self.mode == 0:
            param = "{\"image_name\":\"" + self.Image_Path + "\"}"

        # 网络图片
        else:
            image_name = 'img.jpg'
            param = "{\"image_name\":\"" + image_name + "\",\"image_url\":\"" + self.Image_Path + "\"}"

        # 构建头域中的 X-Param
        curTime = str(int(t.time()))
        # 构建头域中的 X-CheckSum
        paramBase64 = base64.b64encode(param.encode("utf-8"))
        # 构建头域中的 X-CheckSum
        tmp = str(paramBase64, "utf-8")
        m2 = hashlib.md5()
        m2.update((self.API_Key + curTime + tmp).encode("utf-8"))
        checksum = m2.hexdigest()
        # 头域
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-API_ID': self.API_ID,
            'X-CheckSum': checksum,
        }
        return header

    def __get_body(self):
        """

        :return:
        """
        bin_file = open(self.Image_Path, 'rb')
        data = bin_file.read()
        bin_file.close()
        return data

    def __get_data_by_type(self, type, headers, data=None):
        """

        :param type:
        :param headers:
        :param data:
        :return:
        """
        try:
            result = requests.post(self.base_url + type, headers=headers, data=data)
            result = json.loads(result.content)
            code = result['code']
            if code == 0:
                label = result['data']['fileList'][0]['label']
            else:
                label = result['desc']

        except Exception as e:
            code = -1
            label = '检验类型%s是否正确' % type
            print(str(e))

        return code, label

    def Get_data(self):
        """

        :return:
        """
        res = []
        # 调用 __get_body 方法完成图片二进制读取
        data = self.__get_body()
        # 调用 __get_header 方法完成头域的设置
        headers = self.__get_headers()
        # 调用完成年龄接口的请求， 接口类型: type -> age
        code, age = self.__get_data_by_type(type='age', headers=headers, data=data)
        res.append({
            'type': 'age',
            'code': code,
            'value': age,
        })
        # 调用完成研制接口请求， 接口类型: type -> face_score
        code, face_score = self.__get_data_by_type(type='face_score', headers=headers, data=data)
        res.append({
            'type': 'face_score',
            'code': code,
            'value': face_score,
        })
        # 调用完成性别接口请求， 接口类型: type -> sex
        code, sex = self.__get_data_by_type(type='sex', headers=headers, data=data)
        res.append({
            'type': 'sex',
            'code': code,
            'value': sex,
        })
        # 调用完成表情接口请求， 接口类型: type -> expression
        code, expression = self.__get_data_by_type(type='expression', headers=headers, data=data)
        res.append({
            'type': 'expression',
            'code': code,
            'value': expression,
        })
        return res

    def Process_Data(self, res):
        """

        :param res:
        :return:
        """
        process_result = []
        for item in res:
            if item['type'] == 'age':
                # 调用 Convert_age 方法解析结果
                if item['code'] == 0:
                    item['value'] = FaceDesc(item['value']).Concert_age()
                process_result.append({
                    'type': '年龄',
                    'desc': item['value'],
                })
            elif item['type'] == 'face_score':
                # 调用 Convert_score 方法解析结果
                if item['code'] == 0:
                    item['value'] = FaceDesc(item['value']).Concert_score()
                process_result.append({
                    'type': '颜值',
                    'desc': item['value'],
                })

            elif item['type'] == 'sex':
                # 调用 Convert_sex 方法解析结果
                if item['code'] == 0:
                    item['value'] = FaceDesc(item['value']).Concert_sex()
                process_result.append({
                    'type': '性别',
                    'desc': item['value'],
                })

            else:
                # 调用 Convert_expression 方法解析结果
                if item['code'] == 0:
                    item['value'] = FaceDesc(item['value']).Concert_expression()
                process_result.append({
                    'type': '表情',
                    'desc': item['value'],
                })

        return process_result

    # def face_web_analysis(self, res):
    #     """
    #
    #     :param res:
    #     :return:
    #     """
    #     # 网络图片: 人脸分析
    #     self.mode = 1
    #     # 调用 __get_header 方法完成图片的头域设置
    #     headers = self.__get_headers()
    #     code, age = self.__get_data_by_type('age', headers)
    #
    #     if code == 0:
    #         age = FaceDesc(age).Concert_age()
    #     code, face_score = self.__get_data_by_type('face_score', headers)
    #     if code == 0:
    #         face_score = FaceDesc(face_score).Concert_score()
    #     code, sex = self.__get_data_by_type('sex', headers)
    #     if code == 0:
    #         sex = FaceDesc(sex).Concert_sex()
    #     code, expression = self.__get_data_by_type('expression', headers)
    #     if code == 0:
    #         expression = FaceDesc(expression).Concert_expression()
    #
    #     print(self.msg % (age, face_score, sex, expression))

    def face_local_analysis(self):
        """

        :return:
        """
        self.mode = 0
        # 调用 Get_data 方法获取从服务器请求的数据
        request_data = self.Get_data()
        print(request_data)
        # 调研 Process_data 方法将数据进行解析
        process_data = self.Process_Data(request_data)
        print(process_data)

        return process_data


if __name__ == '__main__':
    # print(r'..\\..\\static\\images\\upload\\compare1.jpg')
    res = FaceFeature(
        API_ID=API_ID,
        API_Key=API_Key,
        Path=r'..\\..\\static\\images\\upload\\compare2.jpg'
    ).face_local_analysis()
    pprint(res)
    # url = 'http://hbimg.b0,upaiyun.com/a09289289df694cd6157f997ffa017cc44d4ca9e288fb-OehMYA_fw658'
    # FaceFeature(url).face_web_analysis()
