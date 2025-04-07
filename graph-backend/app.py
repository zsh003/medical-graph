from flask import Flask
from flask_cors import CORS

from auth.models import db
from config import Config
from auth.routes import auth
from graph.routes import graph

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)
with app.app_context():
    db.create_all()

# 导入蓝图

#注册蓝图
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(graph, url_prefix='/graph')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
