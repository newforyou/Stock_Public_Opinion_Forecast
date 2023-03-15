from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .forms import RegisterForm, LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db
from blueprints import personal

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(userMail=email, userName=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            flash("注册失败！请检查信息是否正确！")
            return redirect(url_for("auth.register"))


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(userMail=email).first()
            if not user:
                print("邮箱不存在！")
                flash("邮箱不存在！")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                session['userId'] = user.userId
                return redirect(url_for("personal.index"))
            else:
                print("密码错误！")
                flash("密码错误！")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))
