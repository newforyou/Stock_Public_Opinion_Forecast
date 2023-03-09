from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .forms import RegisterForm, LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db
from blueprints import personal

bp = Blueprint("personal", __name__, url_prefix="/personal")
@bp.route("/index",methods=['GET','POST'])
def index():
    #questions = StockModel.query.order_by(StockModel.create_time.desc()).all()
    return render_template("index.html")

