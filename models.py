from datetime import datetime
# 导入备用数据库文件
from flask_sqlalchemy import SQLAlchemy
# from .face import db
# from app import db
db = SQLAlchemy()


# 创建验证码类
class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

# Create your models here.
# 学生信息表
# class StudentInfoModel(db.Model):
#     user_id = db.IntegerField(primary_key=True, verbose_name='用户UID')
#     student_id = db.CharField(max_length=15, verbose_name='学生ID')
#     student_name = db.CharField(max_length=30, verbose_name='学生姓名')
#     student_phone = db.CharField(max_length=20, verbose_name='学生电话')
#     student_address = db.CharField(max_length=50, verbose_name='学生所处地址')
#     student_faculty = db.CharField(max_length=20, verbose_name='学生所属院系')
#     student_major = db.CharField(max_length=30, verbose_name='学生所属专业')
#     create_time = db.DateTimeField(auto_now_add=True, verbose_name='创建信息时间', null=True)
#     update_time = db.DateTimeField(auto_now=True, verbose_name='最后修改时间', null=True)
#     time_test = db.DateTimeField(default=datetime.now)
#
#     # 取消外部链接
#     # student_course = models.ForeignKey('CourseModel', on_delete=True)
#     class Meta:
#         db_table = 'New_StudentInfo'
#
#
# # 学生账户表
# class StudentUserModel(db.Model):
#     user_id = db.AutoField(primary_key=True)
#     user_name = db.CharField(max_length=30, verbose_name='用户名')
#     user_password = db.CharField(max_length=20, verbose_name='密码')
#     create_time = db.DateTimeField(auto_now_add=True, verbose_name='用户创建时间', null=True)
#     update_time = db.DateTimeField(auto_now=True, verbose_name='最后修改时间', null=True)
#     time_test = db.DateTimeField(default=datetime.now)
#
#     #
#     class Meta:
#         db_table = 'New_StudentUserModel'
