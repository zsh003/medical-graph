from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import os
import requests
from app.config import Config
from app.routes import statistics
from app.api import entity_recognition, relation_extraction, knowledge_update
from app.services.neo4j_service import Neo4jService

def setup_logger(app):
    """配置日志记录器"""
    if not os.path.exists('logs'):
        os.mkdir('logs')
        
    # 文件处理器
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    console_handler.setLevel(logging.DEBUG)
    
    # 配置应用日志
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('医药知识图谱系统启动')

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    
    # 设置日志
    setup_logger(app)
    
    # 注册蓝图
    app.register_blueprint(statistics.bp)
    app.register_blueprint(entity_recognition.bp, url_prefix='/api/entity')
    app.register_blueprint(relation_extraction.bp, url_prefix='/api/relation')
    app.register_blueprint(knowledge_update.bp, url_prefix='/api/knowledge')
    
    # 初始化Neo4j服务
    neo4j_service = Neo4jService()
    
    @app.route('/')
    def index():
        return jsonify({
            'status': 'success',
            'message': '医药知识图谱系统API服务已启动',
            'version': '1.0.0',
            'endpoints': {
                'statistics': '/api/statistics',
                'entity_recognition': '/api/entity',
                'relation_extraction': '/api/relation',
                'knowledge_update': '/api/knowledge'
            }
        })
    
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f'Page not found: {request.url}')
        return jsonify({
            'status': 'error',
            'message': '请求的资源不存在',
            'error': str(error)
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return jsonify({
            'status': 'error',
            'message': '服务器内部错误',
            'error': str(error)
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
