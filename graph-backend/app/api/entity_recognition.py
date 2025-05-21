from flask import Blueprint, jsonify, request, current_app
from app.services.neo4j_service import Neo4jService
from app.utils.text_processor import TextProcessor
import traceback

bp = Blueprint('entity_recognition', __name__)
neo4j_service = Neo4jService()
text_processor = TextProcessor()

@bp.route('/recognize', methods=['POST'])
def recognize_entities():
    """识别文本中的医疗实体"""
    try:
        current_app.logger.info('开始实体识别请求')
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            current_app.logger.warning('实体识别请求缺少文本内容')
            return jsonify({'error': '请提供文本内容'}), 400
            
        current_app.logger.debug(f'待识别文本: {text[:100]}...')
        
        # 使用TextProcessor进行实体识别
        entities = text_processor.extract_entities(text)
        current_app.logger.info(f'识别到 {len(entities)} 个实体')
        
        # 从Neo4j中获取实体详细信息
        enriched_entities = []
        for entity in entities:
            current_app.logger.debug(f'处理实体: {entity["name"]} ({entity["type"]})')
            entity_info = neo4j_service.get_entity_info(entity['name'], entity['type'])
            if entity_info:
                enriched_entities.append({
                    'name': entity['name'],
                    'type': entity['type'],
                    'info': entity_info
                })
                current_app.logger.debug(f'实体 {entity["name"]} 已找到详细信息')
            else:
                current_app.logger.warning(f'实体 {entity["name"]} 未找到详细信息')
        
        current_app.logger.info(f'成功处理 {len(enriched_entities)} 个实体')
        return jsonify({
            'success': True,
            'entities': enriched_entities
        })
        
    except Exception as e:
        current_app.logger.error(f'实体识别失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@bp.route('/entities', methods=['GET'])
def get_all_entities():
    """获取所有实体类型及其数量"""
    try:
        current_app.logger.info('开始获取所有实体统计信息')
        entity_stats = neo4j_service.get_entity_statistics()
        current_app.logger.info(f'成功获取实体统计信息: {entity_stats}')
        return jsonify({
            'success': True,
            'statistics': entity_stats
        })
    except Exception as e:
        current_app.logger.error(f'获取实体统计信息失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@bp.route('/entities/<entity_type>', methods=['GET'])
def get_entities_by_type(entity_type):
    """获取指定类型的所有实体"""
    try:
        current_app.logger.info(f'开始获取 {entity_type} 类型的实体')
        entities = neo4j_service.get_entities_by_type(entity_type)
        current_app.logger.info(f'成功获取 {len(entities)} 个 {entity_type} 类型实体')
        return jsonify({
            'success': True,
            'entities': entities
        })
    except Exception as e:
        current_app.logger.error(f'获取 {entity_type} 类型实体失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500 