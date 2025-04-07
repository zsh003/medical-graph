from flask import Flask
from flask_cors import CORS

from auth.models import db
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)
with app.app_context():
    db.create_all()

# 导入蓝图
from auth.routes import auth

#注册蓝图
app.register_blueprint(auth, url_prefix='/auth')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
