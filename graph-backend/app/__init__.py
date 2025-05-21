from app.routes import statistics

def create_app():
    app = Flask(__name__)
    
    # 注册蓝图
    app.register_blueprint(statistics.bp)
    
    # ... existing code ...
    
    return app 