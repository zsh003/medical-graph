from flask import Flask
from app.routes import statistics, graph

def create_app():
    app = Flask(__name__)
    
    # 注册蓝图
    app.register_blueprint(statistics.bp)
    app.register_blueprint(graph.bp)
    
    # ... existing code ...
    
    return app 