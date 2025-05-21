from flask import Flask
from flask_cors import CORS

from auth.models import db
from app.config import Config
from auth.routes import auth
from graph.routes import graph

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# 导入蓝图

#注册蓝图
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(graph, url_prefix='/graph')

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
