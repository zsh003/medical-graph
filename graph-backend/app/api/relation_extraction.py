from flask import Blueprint, jsonify, request
from app.services.neo4j_service import Neo4jService
from app.utils.text_processor import TextProcessor

bp = Blueprint('relation_extraction', __name__)
neo4j_service = Neo4jService()
text_processor = TextProcessor()

@bp.route('/extract', methods=['POST'])
def extract_relations():
    """从文本中抽取实体关系"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': '请提供文本内容'}), 400
            
        # 使用TextProcessor进行关系抽取
        relations = text_processor.extract_relations(text)
        
        # 从Neo4j中获取关系详细信息
        enriched_relations = []
        for relation in relations:
            relation_info = neo4j_service.get_relation_info(
                relation['source'],
                relation['target'],
                relation['type']
            )
            if relation_info:
                enriched_relations.append({
                    'source': relation['source'],
                    'target': relation['target'],
                    'type': relation['type'],
                    'info': relation_info
                })
        
        return jsonify({
            'success': True,
            'relations': enriched_relations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/relations', methods=['GET'])
def get_all_relations():
    """获取所有关系类型及其数量"""
    try:
        relation_stats = neo4j_service.get_relation_statistics()
        return jsonify({
            'success': True,
            'statistics': relation_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/relations/<relation_type>', methods=['GET'])
def get_relations_by_type(relation_type):
    """获取指定类型的所有关系"""
    try:
        relations = neo4j_service.get_relations_by_type(relation_type)
        return jsonify({
            'success': True,
            'relations': relations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 