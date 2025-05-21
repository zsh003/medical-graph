from flask import Blueprint, jsonify, request
from app.services.neo4j_service import Neo4jService
from app.utils.text_processor import TextProcessor
from app.utils.validator import DataValidator

bp = Blueprint('knowledge_update', __name__)
neo4j_service = Neo4jService()
text_processor = TextProcessor()
validator = DataValidator()

@bp.route('/update/entity', methods=['POST'])
def update_entity():
    """更新实体信息"""
    try:
        data = request.get_json()
        
        # 验证数据
        if not validator.validate_entity_data(data):
            return jsonify({'error': '数据格式不正确'}), 400
            
        # 更新实体
        result = neo4j_service.update_entity(
            entity_id=data['id'],
            properties=data['properties']
        )
        
        return jsonify({
            'success': True,
            'message': '实体更新成功',
            'result': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/update/relation', methods=['POST'])
def update_relation():
    """更新关系信息"""
    try:
        data = request.get_json()
        
        # 验证数据
        if not validator.validate_relation_data(data):
            return jsonify({'error': '数据格式不正确'}), 400
            
        # 更新关系
        result = neo4j_service.update_relation(
            source_id=data['source_id'],
            target_id=data['target_id'],
            relation_type=data['type'],
            properties=data['properties']
        )
        
        return jsonify({
            'success': True,
            'message': '关系更新成功',
            'result': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/add/entity', methods=['POST'])
def add_entity():
    """添加新实体"""
    try:
        data = request.get_json()
        
        # 验证数据
        if not validator.validate_entity_data(data):
            return jsonify({'error': '数据格式不正确'}), 400
            
        # 添加实体
        result = neo4j_service.add_entity(
            entity_type=data['type'],
            properties=data['properties']
        )
        
        return jsonify({
            'success': True,
            'message': '实体添加成功',
            'result': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/add/relation', methods=['POST'])
def add_relation():
    """添加新关系"""
    try:
        data = request.get_json()
        
        # 验证数据
        if not validator.validate_relation_data(data):
            return jsonify({'error': '数据格式不正确'}), 400
            
        # 添加关系
        result = neo4j_service.add_relation(
            source_id=data['source_id'],
            target_id=data['target_id'],
            relation_type=data['type'],
            properties=data['properties']
        )
        
        return jsonify({
            'success': True,
            'message': '关系添加成功',
            'result': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/delete/entity/<entity_id>', methods=['DELETE'])
def delete_entity(entity_id):
    """删除实体"""
    try:
        result = neo4j_service.delete_entity(entity_id)
        return jsonify({
            'success': True,
            'message': '实体删除成功',
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/delete/relation', methods=['DELETE'])
def delete_relation():
    """删除关系"""
    try:
        data = request.get_json()
        result = neo4j_service.delete_relation(
            source_id=data['source_id'],
            target_id=data['target_id'],
            relation_type=data['type']
        )
        return jsonify({
            'success': True,
            'message': '关系删除成功',
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 