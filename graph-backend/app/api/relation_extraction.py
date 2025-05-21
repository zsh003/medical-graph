from flask import Blueprint, jsonify, request, current_app
from app.services.neo4j_service import Neo4jService
from app.utils.text_processor import TextProcessor
import traceback

bp = Blueprint('relation_extraction', __name__)
neo4j_service = Neo4jService()
text_processor = TextProcessor()

@bp.route('/extract', methods=['POST'])
def extract_relations():
    """从文本中抽取实体关系"""
    try:
        current_app.logger.info('开始关系抽取请求')
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            current_app.logger.warning('关系抽取请求缺少文本内容')
            return jsonify({'error': '请提供文本内容'}), 400
            
        current_app.logger.debug(f'待抽取关系文本: {text[:100]}...')
        
        # 使用TextProcessor进行关系抽取
        relations = text_processor.extract_relations(text)
        current_app.logger.info(f'识别到 {len(relations)} 个关系')
        
        # 从Neo4j中获取关系详细信息
        enriched_relations = []
        for relation in relations:
            current_app.logger.debug(f'处理关系: {relation["source"]} - {relation["type"]} - {relation["target"]}')
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
                current_app.logger.debug(f'关系已找到详细信息')
            else:
                current_app.logger.warning(f'关系未找到详细信息')
        
        current_app.logger.info(f'成功处理 {len(enriched_relations)} 个关系')
        return jsonify({
            'success': True,
            'relations': enriched_relations
        })
        
    except Exception as e:
        current_app.logger.error(f'关系抽取失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@bp.route('/relations', methods=['GET'])
def get_all_relations():
    """获取所有关系类型及其数量"""
    try:
        current_app.logger.info('开始获取所有关系统计信息')
        relation_stats = neo4j_service.get_relation_statistics()
        current_app.logger.info(f'成功获取关系统计信息: {relation_stats}')
        return jsonify({
            'success': True,
            'statistics': relation_stats
        })
    except Exception as e:
        current_app.logger.error(f'获取关系统计信息失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@bp.route('/relations/<relation_type>', methods=['GET'])
def get_relations_by_type(relation_type):
    """获取指定类型的所有关系"""
    try:
        current_app.logger.info(f'开始获取 {relation_type} 类型的关系')
        relations = neo4j_service.get_relations_by_type(relation_type)
        current_app.logger.info(f'成功获取 {len(relations)} 个 {relation_type} 类型关系')
        return jsonify({
            'success': True,
            'relations': relations
        })
    except Exception as e:
        current_app.logger.error(f'获取 {relation_type} 类型关系失败: {str(e)}')
        current_app.logger.error(f'错误详情: {traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500 