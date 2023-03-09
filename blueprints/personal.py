from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from .forms import RegisterForm, LoginForm
from models import UserModel,StockModel,SubscriptionModel
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db
from blueprints import personal
from flask_paginate import Pagination, get_page_args

bp = Blueprint("personal", __name__, url_prefix="/personal")
@bp.route("/index",methods=['GET','POST'])
def index():
    # page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    # stocks = StockModel.query.order_by(StockModel.create_time.asc()).offset(offset).limit(per_page).all()
    # pagination = Pagination(page=page, per_page=per_page, total=StockModel.query.count(), css_framework='bootstrap4')
    return render_template("index.html")

@bp.route('/profile')
def profile():
    return render_template('profile.html')
@bp.route('/profile/<int:user_id>',methods=['GET','POST'])
def update_profile(user_id):
    userinfo = UserModel.query.get(user_id)
    if request.method == 'GET':
        return render_template('profile.html', user_info=userinfo)
    else:
        if userinfo:
            # 读取表单数据
            nickname = request.form.get('usernick')
            age = request.form.get('userage')
            mail = request.form.get('usermail')

            userinfo.nickname = nickname
            userinfo.age = age
            userinfo.userMail = mail
            db.session.commit()

            return render_template('profile.html', user_info=userinfo)
        else:
            return jsonify({'status': 'error', 'message': '用户信息不存在'})


@bp.route('/detail')
def detail():
    return render_template('details.html')

