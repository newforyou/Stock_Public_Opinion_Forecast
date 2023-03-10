from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify,g
from .forms import RegisterForm, LoginForm,UpdatePersonalForm,UpdatePasswordForm
from models import UserModel,StockModel,SubscriptionModel
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db
from blueprints import personal
from flask_paginate import Pagination, get_page_args

bp = Blueprint("personal", __name__, url_prefix="/personal")

@bp.route("/index",methods=['GET','POST'])
def index():
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page
    stocks = StockModel.query.order_by(StockModel.stockId).offset(offset).limit(per_page).all()
    pagination = Pagination(page=page, per_page=per_page, total=StockModel.query.count(), css_framework='bootstrap4')
    return render_template("index.html",stocks=stocks,pagination=pagination)

@bp.route('/profile',methods=['GET','POST'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    else:
        form1 = UpdatePersonalForm(request.form)
        if form1.validate():
            g.user.nickname = form1.nickname.data
            g.user.age = form1.age.data
            g.user.userMail = form1.userMail.data
            g.user.signature=form1.signature.data
            db.session.merge(g.user)
            db.session.commit()
            print("修改个人信息成功")
            return render_template('profile.html')
        else:
            form2 = UpdatePasswordForm(request.form)
            if form2.validate():
                g.user.password = generate_password_hash(form2.newpwd.data)
                db.session.merge(g.user)
                db.session.commit()
                print("修改密码成功")
                return redirect("/")
            else:
                print(form2.errors)
                return render_template('profile.html')
            print(form1.errors)
            return render_template('profile.html')

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@bp.route("/subscribe",methods=['POST'])
def subscribe():
    data = request.get_json()
    ts_code = data['ts_code']
    print(ts_code)
    return redirect(url_for('personal.index'))

@bp.route('/detail')
def detail():
    return render_template('details.html')

