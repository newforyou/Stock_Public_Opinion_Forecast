from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
