import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel
from flask import g


# Form： 主要是用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=14, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致")])

    # 自定义验证
    # 1.邮箱是否已经被注册
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(userMail=email).first()
        if user:
            raise wtforms.ValidationError(message="邮箱已经被注册！")

    # 2.用户名是否被注册
    def validate_username(self, field):
        username = field.data
        user = UserModel.query.filter_by(userName=username).first()
        if user:
            raise wtforms.ValidationError(message="用户名已经被注册！")


class UpdatePersonalForm(wtforms.Form):
    nickname = wtforms.StringField(validators=[Length(min=1, max=14, message="昵称格式错误！")])
    age = wtforms.StringField(validators=[Length(min=1, max=3, message="年龄格式错误！")])
    userMail = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    signature = wtforms.StringField(validators=[Length(min=1, max=50, message="个性签名格式错误！")])


class UpdatePasswordForm(wtforms.Form):
    originpwd = wtforms.StringField(validators=[Length(min=1, max=14, message="不可用！")])
    newpwd = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    verifypwd = wtforms.StringField(validators=[EqualTo("newpwd", message="两次密码不一致")])


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
