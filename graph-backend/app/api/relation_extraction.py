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
        
        # 处理关系数据，确保与前端配置一致
        processed_relations = []
        for relation in relations:
            # 确保关系类型与前端配置一致
            relation_type = relation['type'].lower()
            # if relation_type not in text_processor.relation_types:
            #     continue
                
            # 构建符合前端展示格式的关系数据
            processed_relation = {
                'source': {
                    'name': relation['source']['name'],
                    'type': relation['source']['type'],
                    'info': relation['source']['info']
                },
                'target': {
                    'name': relation['target']['name'],
                    'type': relation['target']['type'],
                    'info': relation['target']['info']
                },
                'type': relation_type,
                'properties': relation['properties']
            }
            processed_relations.append(processed_relation)
        
        current_app.logger.info(f'成功处理 {len(processed_relations)} 个关系')
        return jsonify({
            'success': True,
            'relations': processed_relations
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