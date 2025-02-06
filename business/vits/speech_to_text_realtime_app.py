#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 语音听写(即为 语音识别): 用于1分钟内的即时语音转文字的技术，支持实时返回识别结果
# 从而达到一边上传音频一边获得识别文本的效果

# 导入 tts_api_get_result到此文件中
from tts_to_speech_app import tts_api_get_result
# 导入 Flask Web 所依赖的框架
from flask import Flask, render_template, request, redirect, url_for
import time
from IFlytek_API import *


# 文件存放地址
# text_file = 'D:/Document/Class/Chinese_Medication/Doctor_AnHui_China-Python_Creative_Project/Origin/'
# 用于存储听写后的文本
# text_file = 'speech.txt'
# 创建程序实例
app = Flask(__name__)


@app.route('/listen', methods=['GET', 'POST'])
def speech_to_text():
    if request.method == 'GET':
        return render_template('home.html', result={})

    Text = request.form['text']
    if len(Text) == 0:
        return render_template('home.html', result={})

    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    # 获取页面上传的音频文件
    # file = request.files['file']
    # if not file:
    #     return render_template('home.html', result={})
    # file_name = r"D:/Document/Class/Chinese_Medication/Doctor_AnHui_China-Python_Creative_Project/Origin/"
    # 获取文件名
    file_name = 'static/' + now_time + r'_Vits.mp3'
    tts_file_post = now_time + r'_Vits.mp3'
    # 文件写入磁盘
    # file.save(file_name)
    # 调用听写模块并将结果保存到 txt文件中

    tts_api_get_result(API_ID, API_Key, API_Secret, TEXT=Text, tts_file=file_name)

    # 读取 txt文件内容获取听写结果
    # with open(text_file, 'r') as f:
    #     text = f.readlines()
    # result = ''.join(text)

    return render_template('home.html', result=tts_file_post)


if __name__ == '__main__':
    app.run(debug=True, port=6633)


