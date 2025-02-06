# !/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import string
import time
from pprint import pprint
from random import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import ValidationError
# 导入邮箱信息模块
from flask_mail import Message
# 导入绑定模块
from flask_migrate import Migrate
# 导入备用数据库文件
from flask_sqlalchemy import SQLAlchemy

import business
from business import FaceCompare, FaceFeature, FaceDesc, HandWriting, General, WebITR, ItrTeach, mail, mysql, \
    LoginForm, RegisterForm, tts_api_get_result, download_audio, Ws_Param
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, abort, g, \
    send_from_directory

# 文件存放路径
UPLOAD_FOLDER = r'E:\\Temp\\Face\\static\\images\\upload\\'
# 人脸特征图片文件名
UPLOAD_FEATURE_IMAGE = 'compare2.jpg'
# 人脸比对图片一的文件名
UPLOAD_COMPARE_ONE_IMAGE = 'compare1.jpg'
# 人脸比对图片二的文件名
UPLOAD_COMPARE_TWO_IMAGE = 'compare2.jpg'
# 手写文字图片文件名
UPLOAD_HAND_IMAGE = 'ocr.jpg'
# 印刷文字图像路径
UPLOAD_GENERAL_IMAGE = 'general.jpg'
# 速算图片文件名
UPLOAD_ITR_IMAGE = 'itr.jpg'
# 速算识别结果文件名
SHOW_ITR_IMAGE = 'itr_result.jpg'
# 公式识别图片文件名
UPLOAD_ITR_TEACH_IMAGE = 'itrteach.jpg'
# 公式识别结果文件名
SHOW_ITR_TEACH_IMAGE = 'itrteach_result.jpg'

# 创建程序实例
app = Flask(__name__)
app.config.from_object(business.compares.config)
# 人脸特征分析图像路径
app.config['UPLOAD_FEATURE_IMAGE'] = UPLOAD_FOLDER + UPLOAD_FEATURE_IMAGE
# 人脸比对图片一的文件路径
app.config['UPLOAD_COMPARE_ONE_IMAGE'] = UPLOAD_FOLDER + UPLOAD_COMPARE_ONE_IMAGE
# 人脸比对图片二的文件路径
app.config['UPLOAD_COMPARE_TWO_IMAGE'] = UPLOAD_FOLDER + UPLOAD_COMPARE_TWO_IMAGE
# 手写文字图像总路径
app.config['UPLOAD_HAND_IMAGE'] = UPLOAD_FOLDER + UPLOAD_HAND_IMAGE
# 印刷文字图像总路径
app.config['UPLOAD_GENERAL_IMAGE'] = UPLOAD_FOLDER + UPLOAD_GENERAL_IMAGE
# 速算文字图像路径
app.config['UPLOAD_ITR_IMAGE'] = UPLOAD_FOLDER + UPLOAD_ITR_IMAGE
# 速算识别结果图像路径
app.config['SHOW_ITR_IMAGE'] = UPLOAD_FOLDER + SHOW_ITR_IMAGE
# 公式识别图像路径
app.config['UPLOAD_ITR_TEACH_IMAGE'] = UPLOAD_FOLDER + UPLOAD_ITR_TEACH_IMAGE
# 公式识别结果图像路径
app.config['SHOW_ITR_TEACH_IMAGE'] = UPLOAD_FOLDER + SHOW_ITR_TEACH_IMAGE
"""

:return
"""

# 初始化邮箱功能
mail.init_app(app)
# 初始化绑定S
db = SQLAlchemy()
from app import db

migrate = Migrate(app, db)


def clear_pic(file_path):
    """
    清空图片
    :param file_path:
    :return:
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def clear_hand_writing_pic(file_path=None):
    """

    :return:
    """
    clear_pic(app.config['UPLOAD_HAND_IMAGE'])


def clear_general_pic(file_path=None):  # put application's code here
    """

    :return:
    """
    # send_file('face/home.html')
    clear_pic(app.config['UPLOAD_GENERAL_IMAGE'])


def clear_itr_pic(file_path=None):
    """

    :return:
    """
    # 如果存在上传文字，则删除
    clear_pic(app.config['UPLOAD_ITR_IMAGE'])
    clear_pic(app.config['SHOW_ITR_IMAGE'])


def clear_itr_teach_pic(file_path=None):
    """

    :return:
    """
    # 如果存在上传文字，则删除
    clear_pic(app.config['UPLOAD_ITR_TEACH_IMAGE'])
    clear_pic(app.config['SHOW_ITR_TEACH_IMAGE'])


def clear_feature_pic(file_path=None):
    """
    清空人脸特征图片
    :param file_path:
    :return:
    """
    # 如果存在上传文件，则删除
    clear_pic(app.config['UPLOAD_FEATURE_IMAGE'])


def clear_compare_one_pic(file_path=None):
    """
    清空人脸特征图片
    :param file_path:
    :return:
    """
    # 如果存在上传文件，则删除
    clear_pic(app.config['UPLOAD_COMPARE_ONE_IMAGE'])


def clear_compare_two_pic(file_path=None):
    """
    清空人脸特征图片
    :param file_path:
    :return:
    """
    # 如果存在上传文件，则删除
    clear_pic(app.config['UPLOAD_COMPARE_TWO_IMAGE'])


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """

    :return:
    """
    return render_template('face/home.html')


@app.route('/feature', methods=['GET', 'POST'])
def feature():
    """
    人脸分析页面
    :return:
    """
    # 刷新页面时，清除之前上传的文件
    clear_feature_pic()
    return render_template('face/feature_analysis.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    上传图片
    :return:
    """
    # 定义一个空 path
    path = ''
    # 获取文件内容
    img = request.files.get('upfile')
    print(img.filename)
    print(str(img))
    # 获取文件类型
    type = request.form.get('type')
    print(type)

    if type == 'feature':
        path = app.config['UPLOAD_FEATURE_IMAGE']
        clear_feature_pic()
    elif type == 'compare1':
        path = app.config['UPLOAD_COMPARE_ONE_IMAGE']
        clear_compare_one_pic()
    elif type == 'hand':
        path = app.config['UPLOAD_HAND_IMAGE']
        # 删除文件
        clear_hand_writing_pic()
    elif type == 'general':
        path = app.config['UPLOAD_GENERAL_IMAGE']
        clear_general_pic()
    elif type == 'itr':
        path = app.config['UPLOAD_ITR_IMAGE']
        clear_itr_pic()
    elif type == 'compare2':
        path = app.config['UPLOAD_COMPARE_TWO_IMAGE']
        clear_compare_two_pic()
    elif type == 'itrteach':
        path = app.config['UPLOAD_ITR_TEACH_IMAGE']
        clear_itr_teach_pic()
    else:
        print('Wheres your type?')

    # 如果存在图像文件，则进行删除
    clear_pic(path)
    # 保存文件
    img.save(path)
    # 打印文件路径
    print(path)

    return ""


@app.route('/feature_analysis', methods=['POST'])
def feature_analysis():
    """

    :return:
    """
    res = {}
    # Todo: 判断是否存在待分析图片
    if not os.path.exists(app.config['UPLOAD_FEATURE_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传图片'
    else:
        res['flag'] = 'true'
        API_ID = "b8c48d36"
        API_Key = "6ce64e56ef4ae318f1b1ff9327872b99"

        # Todo: 调用人脸特征类 获取分析结果
        data = FaceFeature(
            API_ID=API_ID,
            API_Key=API_Key,
            Path=app.config['UPLOAD_FEATURE_IMAGE'],
        ).face_local_analysis()
        res['data'] = data
        pprint(res)
    return json.dumps(res)


@app.route('/compare', methods=['GET', 'POST'])
def compare():
    """

    :return:
    """
    clear_compare_one_pic()
    clear_compare_two_pic()
    return render_template('face/feature_compare.html')


@app.route('/feature_compare', methods=['POST'])
def feature_compare():
    """

    :return:
    """
    res = {}
    # Todo: 判断是否存在待分析的图片
    if not os.path.exists(app.config['UPLOAD_COMPARE_ONE_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传左边的图片'
    elif not os.path.exists(app.config['UPLOAD_COMPARE_TWO_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传右边的图片'
    else:
        res['flag'] = 'true'
        API_ID = "b8c48d36"
        API_Key = "19172b9bd8b5478be422927c2cf065c8"
        API_Secret = "NWM5OTgwYzMyNDlkNTQxZWMzZGVlOWY5"
        # Todo: 调用人脸比对类型获取分析结果
        data = FaceCompare(
            API_ID=API_ID,
            API_Key=API_Key,
            API_Secret=API_Secret,
            One_Path=app.config["UPLOAD_COMPARE_ONE_IMAGE"],
            Two_Path=app.config["UPLOAD_COMPARE_TWO_IMAGE"],
        ).run()
        res['data'] = data
    return json.dumps(res)


@app.route('/hand_writing')
def hand_writing():
    """

    :return:
    """
    return render_template('ocr/handwriting.html')


@app.route('/hand_writing_api', methods=['POST'])
def hand_API():
    res = {}
    # Todo: 判断是否存在待分析图片
    if not os.path.exists(app.config['UPLOAD_HAND_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传图片'
    else:
        res['flag'] = 'true'
        # 应用ID
        API_ID = "b8c48d36"
        # 接口密钥
        API_Key = "668b45a83d15ae7ff4511be82ca1fb14"
        # Todo: 调用手写文字识别类型获取分析结果
        ocr_data = HandWriting(
            API_ID=API_ID,
            API_Key=API_Key,
            Path=app.config['UPLOAD_HAND_IMAGE']
        ).handwriting_analysis()
        print(ocr_data)
        res['data'] = ocr_data
        print(res)
    return json.dumps(res)


@app.route('/general', methods=['GET', 'POST'])
def general():
    """
    印刷文字页面
    :return:
    """
    # 刷新页面时，将清楚之前上传过的文件
    clear_general_pic()
    # send_file('index.html')
    return render_template('ocr/general.html')


@app.route('/general_api', methods=['GET', 'POST'])
def general_API():
    """

    :return:
    """
    res = {}
    # Todo: 判断是都存在待分析图片
    if not os.path.exists(app.config['UPLOAD_GENERAL_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传图片'
    else:
        res['flag'] = 'true'
        # 应用ID
        API_ID = "b8c48d36"
        # 接口密钥
        API_Key = "668b45a83d15ae7ff4511be82ca1fb14"
        # Todo: 调用手写文字识别类型获取分析结果
        ocr_data = General(
            API_ID=API_ID,
            API_Key=API_Key,
            Path=app.config['UPLOAD_GENERAL_IMAGE'],
        ).general_analysis()
        res['data'] = ocr_data
        print(res)
    return json.dumps(res)


@app.route('/itr')
def itr():
    """

    :return:
    """
    # 刷新页面时，清除之前上传的文件
    clear_itr_pic()
    # send_file('index.html')
    return render_template('ocr/itr.html')


@app.route('/itr_api', methods=['post'])
def itr_API():
    """

    :return:
    """
    # Todo: 判断是都存在待分析图片
    res = {}
    if not os.path.exists(app.config['UPLOAD_ITR_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传图片'
    else:
        API_ID = "b8c48d36"
        API_Secret = "NWM5OTgwYzMyNDlkNTQxZWMzZGVlOWY5"
        API_Key = "19172b9bd8b5478be422927c2cf065c8"
        host = "rest-api.xfyun.cn"
        # Todo: 调用拍照速算识别类获取分析结果
        data = WebITR(
            API_ID=API_ID,
            API_Secret=API_Secret,
            API_Key=API_Key,
            host=host,
            In_Path=app.config['UPLOAD_ITR_IMAGE'],
            Out_Path=app.config['SHOW_ITR_IMAGE'],
        ).itr_analysis()
        res = data
        res['path'] = app.config['SHOW_ITR_IMAGE']
        print(res['path'])
    return json.dumps(res)


@app.route('/itr_teach')
def itr_teach():
    """

    :return:
    """
    return render_template('ocr/itr_teach.html')


@app.route('/itr_teach_api', methods=['POST'])
def itr_teach_API():
    """

    :return:
    """
    res = {}
    if not os.path.exists(app.config['UPLOAD_ITR_TEACH_IMAGE']):
        res['flag'] = 'false'
        res['msg'] = '请上传图片'
    else:
        API_ID = "b8c48d36"
        API_Key = "19172b9bd8b5478be422927c2cf065c8"
        API_Secret = "NWM5OTgwYzMyNDlkNTQxZWMzZGVlOWY5"
        host = "rest-api.xfyun.cn"
        data = ItrTeach(
            API_ID=API_ID,
            API_Secret=API_Secret,
            API_Key=API_Key,
            host=host,
            In_Path=app.config['UPLOAD_ITR_TEACH_IMAGE'],
            Out_Path=app.config['SHOW_ITR_TEACH_IMAGE'],
        ).itr_teach_analysis()
        res = data
        res['path'] = app.config['SHOW_ITR_TEACH_IMAGE']
    return json.dumps(res)


# 忘记密码页面
@app.route('/forget', methods=['GET', 'POST'])
def forget():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.cursor()
        sql = "DELETE FROM pythonflask.users WHERE email=%s AND password"
        cur.execute(sql, email)
        flash("已为您的邮箱发送新密码，请查看登录后进行更改密码")
        return redirect(url_for('login'))
    return render_template(
        'page/forget.html',
        title="忘记密码 | 学生宿舍系统",
        year=datetime.now().year,
        message='Your application Forget Password Page.'
    )


# 错误界面（异常处理404）
@app.errorhandler(404)
def not_found(e):
    return render_template(
        "page/404.html",
        title="哎呀，找不到页面了"
    )


from models import UserModel, EmailCaptchaModel


# 登录界面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # print(request.form)
        return render_template(
            'page/login.html',
            title="登录 | 智能实践",
            year=datetime.now().year
        )
    else:
        form = LoginForm(request.form)
        print(request.form)
        # print(form)

        # if form.validate():
        if form:
            # if form.validate_on_submit():

            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            # print(user)

            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('index'))

            else:
                flash("邮箱和密码不匹配！")
                return redirect(url_for('login', _flash=True))

        else:
            flash("邮箱或密码格式错误！")
            return redirect(url_for('login', _flash=True))


# 用户注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        print(request.form)

        return render_template(
            'page/register.html',
            title="注册 | 智能实践",
            year=datetime.now().year,
            message='Your application Register Page.')
    else:
        form = RegisterForm(request.form)
        print(request.form)
        # print(form.recaptcha)

        # if form.validate():
        if form:
            try:
                # 调用验证码验证
                form.validate_captcha(form.recaptcha)
                print(form.validate_captcha(form.recaptcha))
                # 调用邮箱验证
                form.validate_email(form.email)
                print(form.validate_email(form.email))

                # 如果验证通过，创建用户并进行其他操作
                username = form.username.data
                email = form.email.data
                password = form.password.data
                # confirm_password = form.confirm_password.data
                # MD5加密     # md(123456)  ==>  "fiberglassFUYEF"
                hash_password = generate_password_hash(password)
                user = UserModel(username=username, email=email, password=hash_password)
                print(user.username, user.email, user.password)
                db.session.add(user)
                db.session.commit()

                flash('注册成功！请登录。', 'success')
                return redirect(url_for('login'))
            except ValidationError as e:
                # 处理验证错误
                flash(str(e), 'error')

        return render_template(
            'page/register.html',
            title="注册 | 智能实践",
            year=datetime.now().year,
            form=form,
            message='Your application Register Page.'
        )


# 用户注销页面
@app.route("/logout")
def logout():
    # 清除session中所有的数据
    session.clear()
    return redirect(url_for('index'))


# 忘记密码界面
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template(
        'page/forget.html',
        title="忘记密码 | 智能实践",
        year=datetime.now().year,
    )


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return render_template(
        'page/reset_password.html',
        title="重置密码 | 智能实践",
        year=datetime.now().year
    )


@app.route('/reset_email', methods=['GET', 'POST'])
def reset_email():
    return render_template(
        'page/reset_email.html',
        title="重置邮箱 | 智能实践",
        year=datetime.now().year
    )


# 邮箱验证码接口
@app.route('/captcha', methods=['POST'])
def get_captcha():
    name = request.args.get('name')
    email = request.args.get('email')
    my_string = string.ascii_letters + string.digits
    captcha = "".join(random.sample(my_string, 4))
    if email:
        message = Message(
            subject='验证你的 智能实践 账号',
            recipients=[email],
            body=f"""
亲爱的{name}!\n 
    非常感谢您的访问，欢迎来到 学生宿舍管理系统，在完成 账号注册 之前，我们需要验证一下您的邮箱哦~\n 
        您的验证码为：{captcha}!\n
    如果在您没有注册的情况下接受到此验证码，请不要管他；并且不要将此验证码告诉他人!\n
最后，感谢您的访问，祝您使用愉快！
            """
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print("验证码为：" + captcha)
        return jsonify({'code': 200, 'success': True, 'message': "验证码发送成功！" + "您的验证码为：" + captcha})
    else:
        return jsonify({'code': 400, 'success': False, 'message': "请先输入邮箱后再获取验证码！"})


# memcached/redis/db
# 邮箱测试
@app.route('/mail')
def send_mail():
    message = Message(
        subject='Test',
        recipients=['hst1368@outlook.com'],
        body=f"【测试邮件】"
    )
    mail.send(message)
    return "测试发送成功"


# @app.route('/listen', methods=['GET', 'POST'])
# def select(request):
#     context = {}
#     try:
#         if request.method == 'POST':
#             student_id = request.POST.get('student_id')
#             try:
#                 student_data = StudentInfoModel.objects.get(student_id=student_id)
#                 print(student_data)
#
#                 dicts = {}
#
#                 context = {
#                     'student_id': student_data.student_id,
#                     'student_name': student_data.student_name,
#                     'student_phone': student_data.student_phone,
#                     'student_address': student_data.student_address,
#                     'student_faculty': student_data.student_faculty,
#                     'student_major': student_data.student_major,
#                     'course_data': dicts,
#                     'msg': True,
#                 }
#                 print(context)
#
#                 tts_file = 'static/text_to_speech.mp3'
#                 Text = '该学生的学号是{student_id}, 姓名是{student_name},电话是{student_phone},地址是{student_address},' \
#                        '院系是{student_faculty}, 专业是{student_major}.'.format(**context)
#                 tts_api_get_result(API_ID, APIKey, APISecret, Text, tts_file)
#
#                 # 音频文件的URL，请替换为你想要下载的音频链接   todo:会极大影响页面的加载速度
#                 audio_url = 'https://vits.ayya.top/voice/bert-vits2?text=' \
#                             '{}' \
#                             '&id=0&format=mp3&length=1.2&noise=0.45&noisew=0.53&segment_size=36&streaming=true&sdp_ratio=0.3&length_zh=1.2&length_ja=1&length_en=1&emotion=4'.format(Text)
#                 # 自定义保存的文件名，包括路径和扩展名
#                 custom_filename = 'static/vits_ayya_speaker.mp3'  # 你想保存的文件名
#                 # 调用函数下载音频文件并指定文件名
#                 file_path = download_audio(audio_url, custom_filename)
#
#                 return render_template(request, 'StudentManagement/select.html', context=context)
#
#             except StudentInfoModel.DoesNotExist:
#                 context = {
#                     'error': "Not Found student id: " + str(student_id),
#                 }
#                 return render_template(request, 'StudentManagement/select.html', context=context)
#         else:
#             root_information = request.session.get('user_name')
#             if root_information:
#                 user_id = root_information['user_id']
#                 user_data = StudentInfoModel.objects.filter(user_id=user_id).first()
#                 context = {
#                     "student_id": user_data.student_id if user_data else None,
#                 }
#             return render_template(request, "StudentManagement/select.html", context=context)
#     except Exception as e:
#         context = {
#             'error': str(e),
#         }
#         return render_template(request, 'StudentManagement/select.html', context=context)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3168)
