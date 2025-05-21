from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes import statistics
from app.services.neo4j_service import Neo4jService

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    
    # 注册蓝图
    app.register_blueprint(statistics.bp)
    
    # 初始化Neo4j服务
    neo4j_service = Neo4jService()
    
    @app.route('/')
    def index():
        return {
            'status': 'success',
            'message': '医药知识图谱系统API服务已启动',
            'version': '1.0.0'
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
