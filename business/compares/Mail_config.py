# 导入主库文件
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

# 配置邮箱项
mail = Mail()

# 邮箱配置：Outlook邮箱配置
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True  # 当开启 TLS 时，请勿开启 SSL 服务，防止服务商发送错误
app.config['MAIL_USE_SSL'] = False  # 当开启 SSL 时，请勿开启 TLS 服务，防止服务商发送错误
app.config['MAIL_DEBUG'] = False
app.config['MAIL_USERNAME'] = 'Example@outlook.com'
# noinspection SpellCheckingInspection
app.config['MAIL_PASSWORD'] = 'Example_password'
app.config['MAIL_DEFAULT_SENDER'] = 'Example@outlook.com'

# 邮箱配置：QQ邮箱配置——TLS
# app.config['MAIL_SERVER'] = "smtp.qq.com"
# app.config['MAIL_PORT'] = '587'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEBUG'] = True
# app.config['MAIL_USERNAME'] = "example@qq.com"
# app.config['MAIL_PASSWORD'] = "example_password"
# app.config['MAIL_DEFAULT_SENDER'] = "example@qq.com"

# 邮箱配置：QQ邮箱配置——SSL
# app.config['MAIL_SERVER'] = "smtp.qq.com"
# app.config['MAIL_PORT'] = '465'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_DEBUG'] = True
# app.config['MAIL_USERNAME'] = "example@qq.com"
# app.config['MAIL_PASSWORD'] = "example_password"
# app.config['MAIL_DEFAULT_SENDER'] = "example@qq.com"


