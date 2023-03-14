#数据库表模型，需要时调用此模块
from exts import db
from datetime import datetime

"""
用户表，字段为：
用户id（主键），若要设置为自增，则加入autoincrement=True
用户名称
登陆密码
昵称
头像
年龄
个性签名
"""
class UserModel(db.Model):
    __tablename__="user"
    userId=db.Column(db.Integer,primary_key=True,autoincrement=True)
    userName=db.Column(db.String(16),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    userMail=db.Column(db.String(30),nullable=False)
    nickname=db.Column(db.String(20),default='请自定义昵称')
    profilePhoto=db.Column(db.String(256),default='./static/assets/images/popular-01.jpg')
    age=db.Column(db.String(5))
    signature=db.Column(db.String(50))

"""
股票信息表，字段为：
股票id（主键）
交易日期
开盘价
最高价
最低价
昨收价
涨跌额
涨跌幅
成交量
成交额

"""
class StockModel(db.Model):
    __tablename__ = "stock"
    stockId = db.Column(db.String(20), primary_key=True)
    ts_code=db.Column(db.String(20),nullable=False)
    name=db.Column(db.String(20),nullable=False)
    industry=db.Column(db.String(20),nullable=False)
    list_date=db.Column(db.String(20),nullable=False)
    area=db.Column(db.String(20),nullable=False)
    predict= db.Column(db.String(600), nullable=False)
    real = db.Column(db.String(600), nullable=False)

"""
新闻表，字段为：
新闻id（主键），如果后期设为自增，可加autoincrement=True
新闻标题
出版日期
来源网站
"""
class NewsModel(db.Model):
    __tablename__ = "news"
    newsId = db.Column(db.Integer, primary_key=True)
    newsTitle=db.Column(db.String(100),nullable=False)
    publicDate=db.Column(db.String(50),nullable=False)
    sourceWebsite = db.Column(db.String(200), nullable=False)

"""
订阅信息表，字段为:
用户id（主键，也为外键）
订阅股票id（外键）
"""
class SubscriptionModel(db.Model):
    __tablename__ = "subscription"
    sub_userId = db.Column(db.Integer,db.ForeignKey("user.userId"), primary_key=True)
    sub_stockId=db.Column(db.String(20),db.ForeignKey("stock.stockId"),primary_key=True)
    # 关系
    subscription=db.relationship(UserModel,backref="stocks")