from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate

from exts import db
from models import UserModel, StockModel, SubscriptionModel, NewsModel
from blueprints.auth import bp as auth_bp

import config
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

db.init_app(app)

app.register_blueprint(auth_bp)

migrate = Migrate(app, db)


# 测试数据库连接,验证是否连接成功
# @app.route('/')
# def hello():
#     engine=db.get_engine()
#     conn=engine.connect()
#     conn.close()
#     return "hello world!"

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/detail')
def detail():
    return render_template('details.html')

@app.route('/test')
def test():
    return render_template('login.html')

@app.route('/test1')
def test1():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
