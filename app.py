import warnings

from flask import Flask, session, g, redirect, url_for
from flask_migrate import Migrate

import config
from blueprints.auth import bp as auth_bp
from blueprints.personal import bp as public_bp
from exts import db
from models import UserModel

warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(public_bp)

migrate = Migrate(app, db)


# 测试数据库连接,验证是否连接成功
# @app.route('/')
# def hello():
#     engine=db.get_engine()
#     conn=engine.connect()
#     conn.close()
#     return "hello world!"

@app.route('/')
def hello():
    return redirect(url_for("auth.login"))



#hook
@app.before_request
def my_before_request():
    userId = session.get("userId")
    if userId:
        user = UserModel.query.get(userId)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


# 上下文处理器
@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run(debug=True)
