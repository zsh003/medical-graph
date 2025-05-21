from flask import Blueprint, jsonify, request
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

@bp.route('/api/entity/list', methods=['GET'])
def get_entity_list():
    """获取实体列表"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))
        search = request.args.get('search', '')
        
        # 计算分页偏移量
        skip = (page - 1) * page_size
        
        # 构建查询
        query = """
        MATCH (n)
        WHERE n.name IS NOT NULL
        AND ($search = '' OR n.name CONTAINS $search)
        RETURN n
        SKIP $skip
        LIMIT $limit
        """
        
        # 获取总数
        count_query = """
        MATCH (n)
        WHERE n.name IS NOT NULL
        AND ($search = '' OR n.name CONTAINS $search)
        RETURN count(n) as total
        """
        
        # 执行查询
        result = neo4j_service.graph.run(query, search=search, skip=skip, limit=page_size).data()
        total = neo4j_service.graph.run(count_query, search=search).data()[0]['total']
        
        # 格式化结果
        entities = []
        for record in result:
            try:
                node = record['n']
                entity = {
                    'id': node.identity,
                    'name': node.get('name', ''),
                    'type': list(node.labels)[0] if node.labels else 'Unknown',
                    'properties': dict(node)
                }
                entities.append(entity)
            except Exception as e:
                print(f"处理实体时出错: {str(e)}")
                continue
        
        return jsonify({
            'success': True,
            'entities': entities,
            'total': total
        })
    except Exception as e:
        print(f"获取实体列表时出错: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/relation/list', methods=['GET'])
def get_relation_list():
    """获取关系列表"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))
        search = request.args.get('search', '')
        
        # 计算分页偏移量
        skip = (page - 1) * page_size
        
        # 构建查询
        query = """
        MATCH (source)-[r]->(target)
        WHERE source.name IS NOT NULL AND target.name IS NOT NULL
        AND ($search = '' OR source.name CONTAINS $search OR target.name CONTAINS $search)
        RETURN source, r, target
        SKIP $skip
        LIMIT $limit
        """
        
        # 获取总数
        count_query = """
        MATCH (source)-[r]->(target)
        WHERE source.name IS NOT NULL AND target.name IS NOT NULL
        AND ($search = '' OR source.name CONTAINS $search OR target.name CONTAINS $search)
        RETURN count(r) as total
        """
        
        # 执行查询
        result = neo4j_service.graph.run(query, search=search, skip=skip, limit=page_size).data()
        total = neo4j_service.graph.run(count_query, search=search).data()[0]['total']
        
        # 格式化结果
        relations = []
        for record in result:
            try:
                source = record['source']
                target = record['target']
                rel = record['r']
                relation = {
                    'id': f"{source.identity}-{target.identity}",
                    'source': {
                        'id': source.identity,
                        'name': source.get('name', ''),
                        'type': list(source.labels)[0] if source.labels else 'Unknown'
                    },
                    'target': {
                        'id': target.identity,
                        'name': target.get('name', ''),
                        'type': list(target.labels)[0] if target.labels else 'Unknown'
                    },
                    'type': type(rel).__name__,
                    'properties': dict(rel)
                }
                relations.append(relation)
            except Exception as e:
                print(f"处理关系时出错: {str(e)}")
                continue
        
        return jsonify({
            'success': True,
            'relations': relations,
            'total': total
        })
    except Exception as e:
        print(f"获取关系列表时出错: {str(e)}")
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