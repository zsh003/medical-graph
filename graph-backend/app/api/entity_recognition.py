from flask import Blueprint, jsonify, request
from app.services.neo4j_service import Neo4jService
from app.utils.text_processor import TextProcessor

bp = Blueprint('entity_recognition', __name__)
neo4j_service = Neo4jService()
text_processor = TextProcessor()

@bp.route('/recognize', methods=['POST'])
def recognize_entities():
    """识别文本中的医疗实体"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': '请提供文本内容'}), 400
            
        # 使用TextProcessor进行实体识别
        entities = text_processor.extract_entities(text)
        
        # 从Neo4j中获取实体详细信息
        enriched_entities = []
        for entity in entities:
            entity_info = neo4j_service.get_entity_info(entity['name'], entity['type'])
            if entity_info:
                enriched_entities.append({
                    'name': entity['name'],
                    'type': entity['type'],
                    'info': entity_info
                })
        
        return jsonify({
            'success': True,
            'entities': enriched_entities
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/entities', methods=['GET'])
def get_all_entities():
    """获取所有实体类型及其数量"""
    try:
        entity_stats = neo4j_service.get_entity_statistics()
        return jsonify({
            'success': True,
            'statistics': entity_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/entities/<entity_type>', methods=['GET'])
def get_entities_by_type(entity_type):
    """获取指定类型的所有实体"""
    try:
        entities = neo4j_service.get_entities_by_type(entity_type)
        return jsonify({
            'success': True,
            'entities': entities
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 