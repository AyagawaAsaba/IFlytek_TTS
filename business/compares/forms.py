# 导入表单模块
# import wtforms
import wtforms as forms
from wtforms.validators import length, email, EqualTo, ValidationError, DataRequired
# 导入模型
from models import EmailCaptchaModel, UserModel


class LoginForm(forms.Form):
    email = forms.StringField(validators=[email(), DataRequired()])
    password = forms.PasswordField(validators=[length(min=8, max=20), DataRequired()])


class RegisterForm(forms.Form):
    username = forms.StringField(validators=[length(min=3, max=20), DataRequired()])
    email = forms.StringField(validators=[email(), DataRequired()])
    recaptcha = forms.StringField(validators=[length(min=4, max=4), DataRequired()])
    password = forms.PasswordField(validators=[length(min=8, max=20), DataRequired()])
    confirm_password = forms.PasswordField(validators=[EqualTo('password'), DataRequired()])

    # 验证码验证
    def validate_captcha(self, field):
        # 获取验证码信息
        captcha = field.data
        print("Debug - captcha:", captcha)

        # 获取邮箱信息
        email = self.email.data
        print("Debug - emails:", email)

        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        print("Debug - captcha_model:", captcha_model)

        if not captcha_model or not captcha_model.captcha or not captcha_model.captcha.lower() == captcha.lower():
            raise ValidationError('邮箱验证码错误')

    # 邮箱验证
    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()

        print("Debug - user_model:", user_model)  # 添加这行
        if user_model:
            raise ValidationError('邮箱已经存在，请返回登录界面进行登录')
