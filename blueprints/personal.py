from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .forms import RegisterForm, LoginForm
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

@bp.route('/profile')
def profile():
    return render_template('profile.html')


@bp.route('/detail')
def detail():
    return render_template('details.html')

