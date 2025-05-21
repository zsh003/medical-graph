from flask import Blueprint, jsonify, request, current_app
from app.services.neo4j_service import Neo4jService
from app.utils.text_processor import TextProcessor
from app.utils.validator import DataValidator
import traceback

bp = Blueprint('knowledge_update', __name__)
neo4j_service = Neo4jService()
text_processor = TextProcessor()
validator = DataValidator()

@bp.route('/update/entity', methods=['POST'])
def update_entity():
    """更新实体信息"""
    try:
        current_app.logger.info('开始更新实体请求')
        data = request.get_json()
        current_app.logger.debug(f'更新实体数据: {data}')
        
        # 验证数据
        if not validator.validate_entity_data(data):
            current_app.logger.warning('实体数据验证失败')
            return jsonify({'error': '数据格式不正确'}), 400
            
        # 更新实体
        result = neo4j_service.update_entity(
            entity_id=data['id'],
            properties=data['properties']
        )
        
        current_app.logger.info(f'实体更新成功: {result}')
        return jsonify({
            'success': True,
            'message': '实体更新成功',
            'result': result
        })
        
    except Exception as e:
        current_app.logger.error(f'实体更新失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@bp.route('/update/relation', methods=['POST'])
def update_relation():
    """更新关系信息"""
    try:
        current_app.logger.info('开始更新关系请求')
        data = request.get_json()
        current_app.logger.debug(f'更新关系数据: {data}')
        
        # 验证数据
        if not validator.validate_relation_data(data):
            current_app.logger.warning('关系数据验证失败')
            return jsonify({'error': '数据格式不正确'}), 400
            
        # 更新关系
        result = neo4j_service.update_relation(
            source_id=data['source_id'],
            target_id=data['target_id'],
            relation_type=data['type'],
            properties=data['properties']
        )
        
        current_app.logger.info(f'关系更新成功: {result}')
        return jsonify({
            'success': True,
            'message': '关系更新成功',
            'result': result
        })
        
    except Exception as e:
        current_app.logger.error(f'关系更新失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@bp.route('/add/entity', methods=['POST'])
def add_entity():
    """添加新实体"""
    try:
        current_app.logger.info('开始添加实体请求')
        data = request.get_json()
        current_app.logger.debug(f'添加实体数据: {data}')
        
        # 验证数据
        if not validator.validate_entity_data(data):
            current_app.logger.warning('实体数据验证失败')
            return jsonify({'error': '数据格式不正确'}), 400
            
        # 添加实体
        result = neo4j_service.add_entity(
            entity_type=data['type'],
            properties=data['properties']
        )
        
        current_app.logger.info(f'实体添加成功: {result}')
        return jsonify({
            'success': True,
            'message': '实体添加成功',
            'result': result
        })
        
    except Exception as e:
        current_app.logger.error(f'实体添加失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@bp.route('/add/relation', methods=['POST'])
def add_relation():
    """添加新关系"""
    try:
        current_app.logger.info('开始添加关系请求')
        data = request.get_json()
        current_app.logger.debug(f'添加关系数据: {data}')
        
        # 验证数据
        if not validator.validate_relation_data(data):
            current_app.logger.warning('关系数据验证失败')
            return jsonify({'error': '数据格式不正确'}), 400
            
        # 添加关系
        result = neo4j_service.add_relation(
            source_id=data['source_id'],
            target_id=data['target_id'],
            relation_type=data['type'],
            properties=data['properties']
        )
        
        current_app.logger.info(f'关系添加成功: {result}')
        return jsonify({
            'success': True,
            'message': '关系添加成功',
            'result': result
        })
        
    except Exception as e:
        current_app.logger.error(f'关系添加失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@bp.route('/delete/entity/<entity_id>', methods=['DELETE'])
def delete_entity(entity_id):
    """删除实体"""
    try:
        current_app.logger.info(f'开始删除实体请求: {entity_id}')
        result = neo4j_service.delete_entity(entity_id)
        current_app.logger.info(f'实体删除成功: {entity_id}')
        return jsonify({
            'success': True,
            'message': '实体删除成功',
            'result': result
        })
    except Exception as e:
        current_app.logger.error(f'实体删除失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@bp.route('/delete/relation', methods=['DELETE'])
def delete_relation():
    """删除关系"""
    try:
        current_app.logger.info('开始删除关系请求')
        data = request.get_json()
        current_app.logger.debug(f'删除关系数据: {data}')
        
        result = neo4j_service.delete_relation(
            source_id=data['source_id'],
            target_id=data['target_id'],
            relation_type=data['type']
        )
        
        current_app.logger.info('关系删除成功')
        return jsonify({
            'success': True,
            'message': '关系删除成功',
            'result': result
        })
    except Exception as e:
        current_app.logger.error(f'关系删除失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500 