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
                
                # 获取源节点和目标节点的标签
                source_labels = list(source.labels)
                target_labels = list(target.labels)
                
                relation = {
                    'id': f"{source.identity}-{target.identity}",
                    'source': {
                        'id': source.identity,
                        'name': source.get('name', ''),
                        'type': source_labels[0] if source_labels else 'Unknown'
                    },
                    'target': {
                        'id': target.identity,
                        'name': target.get('name', ''),
                        'type': target_labels[0] if target_labels else 'Unknown'
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

@bp.route('/api/entity/<int:entity_id>', methods=['PUT'])
def update_entity(entity_id):
    """更新实体信息"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '无效的请求数据'
            }), 400

        # 处理属性值
        properties = {}
        for key, value in data.items():
            if isinstance(value, (str, int, float, bool)):
                properties[key] = value
            elif isinstance(value, list):
                # 确保列表中的元素都是基本类型
                properties[key] = [str(item) for item in value]
            elif value is None:
                properties[key] = None
            else:
                # 将其他类型转换为字符串
                properties[key] = str(value)

        # 更新实体   ==============================================
        query = """
        MATCH (n)
        WHERE id(n) = $entity_id
        SET n += $properties
        RETURN n
        """
        result = neo4j_service.graph.run(query, entity_id=entity_id, properties=properties).data()
        
        if not result:
            return jsonify({
                'success': False,
                'error': '实体不存在'
            }), 404

        return jsonify({
            'success': True,
            'message': '更新成功',
            'entity': dict(result[0]['n'])
        })
    except Exception as e:
        print(f"更新实体时出错: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/entity/<int:entity_id>', methods=['DELETE'])
def delete_entity(entity_id):
    """删除实体"""
    try:
        # 删除实体及其关系
        query = """
        MATCH (n)
        WHERE id(n) = $entity_id
        DETACH DELETE n
        """
        neo4j_service.graph.run(query, entity_id=entity_id)
        
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
    except Exception as e:
        print(f"删除实体时出错: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/relation/<path:relation_id>', methods=['PUT'])
def update_relation(relation_id):
    """更新关系信息"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '无效的请求数据'
            }), 400

        # 处理属性值
        properties = {}
        for key, value in data.items():
            if isinstance(value, (str, int, float, bool)):
                properties[key] = value
            elif isinstance(value, list):
                # 确保列表中的元素都是基本类型
                properties[key] = [str(item) for item in value]
            elif value is None:
                properties[key] = None
            else:
                # 将其他类型转换为字符串
                properties[key] = str(value)

        # 解析关系ID
        source_id, target_id = map(int, relation_id.split('-'))
        
        # 更新关系
        query = """
        MATCH (source)-[r]->(target)
        WHERE id(source) = $source_id AND id(target) = $target_id
        SET r += $properties
        RETURN r, source, target
        """
        result = neo4j_service.graph.run(query, source_id=source_id, target_id=target_id, properties=properties).data()
        
        if not result:
            return jsonify({
                'success': False,
                'error': '关系不存在'
            }), 404

        # 格式化返回结果
        rel = result[0]['r']
        source = result[0]['source']
        target = result[0]['target']
        
        return jsonify({
            'success': True,
            'message': '更新成功',
            'relation': {
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
        })
    except Exception as e:
        print(f"更新关系时出错: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/relation/<path:relation_id>', methods=['DELETE'])
def delete_relation(relation_id):
    """删除关系"""
    try:
        # 解析关系ID
        source_id, target_id = map(int, relation_id.split('-'))
        
        # 删除关系
        query = """
        MATCH (source)-[r]->(target)
        WHERE id(source) = $source_id AND id(target) = $target_id
        DELETE r
        """
        neo4j_service.graph.run(query, source_id=source_id, target_id=target_id)
        
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
    except Exception as e:
        print(f"删除关系时出错: {str(e)}")
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