from flask import Blueprint, jsonify
from app.services.neo4j_service import Neo4jService

bp = Blueprint('statistics', __name__)
neo4j_service = Neo4jService()

@bp.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        # 获取实体总数
        entity_count = neo4j_service.get_entity_count()
        
        # 获取关系总数
        relation_count = neo4j_service.get_relation_count()
        
        # 获取疾病数量
        disease_count = neo4j_service.get_entity_count_by_type('Disease')
        
        # 获取药品数量
        drug_count = neo4j_service.get_entity_count_by_type('Drug')
        
        return jsonify({
            'success': True,
            'statistics': {
                'entityCount': entity_count,
                'relationCount': relation_count,
                'diseaseCount': disease_count,
                'drugCount': drug_count
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/updates/recent', methods=['GET'])
def get_recent_updates():
    try:
        # 获取最近的实体更新
        recent_entities = neo4j_service.get_recent_entities(limit=5)
        
        # 获取最近的关系更新
        recent_relations = neo4j_service.get_recent_relations(limit=5)
        
        # 合并并排序更新记录
        updates = []
        
        # 处理实体更新
        for entity in recent_entities:
            updates.append({
                'title': f'更新实体：{entity["name"]}',
                'description': f'类型：{entity["type"]}',
                'time': entity.get('update_time', ''),
                'icon': entity['type'][0],
                'color': get_entity_type_color(entity['type'])
            })
        
        # 处理关系更新
        for relation in recent_relations:
            updates.append({
                'title': f'更新关系：{relation["source"]["name"]} - {relation["type"]} - {relation["target"]["name"]}',
                'description': f'关系类型：{relation["type"]}',
                'time': relation.get('update_time', ''),
                'icon': 'R',
                'color': get_relation_type_color(relation['type'])
            })
        
        # 按时间排序
        updates.sort(key=lambda x: x['time'], reverse=True)
        
        return jsonify({
            'success': True,
            'updates': updates[:5]  # 只返回最新的5条记录
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_entity_type_color(type):
    color_map = {
        'Disease': '#f5222d',
        'Symptom': '#fa8c16',
        'Drug': '#52c41a',
        'Food': '#1890ff',
        'Check': '#722ed1',
        'Department': '#13c2c2',
        'Producer': '#eb2f96'
    }
    return color_map.get(type, '#d9d9d9')

def get_relation_type_color(type):
    color_map = {
        'belongs_to': '#722ed1',
        'has_symptom': '#fa8c16',
        'has_drug': '#52c41a',
        'has_food': '#1890ff',
        'has_check': '#13c2c2',
        'produced_by': '#eb2f96'
    }
    return color_map.get(type, '#d9d9d9') 