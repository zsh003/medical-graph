from flask import Blueprint, jsonify, request
from app.services.neo4j_service import Neo4jService

bp = Blueprint('graph', __name__)

neo4j_service=Neo4jService()

@bp.route('/search', methods=['GET'])
def search_graph():
    """搜索知识图谱"""
    try:
        keyword = request.args.get('keyword', '')
        limit = request.args.get('limit', type=int)  # 获取节点数量限制参数
        
        if not keyword:
            return jsonify({
                'success': False,
                'error': '请输入搜索关键词'
            }), 400

        # 查询包含关键词的节点及其关系
        query = """
        MATCH (n)-[r]-(m)
        WHERE n.name CONTAINS $keyword OR m.name CONTAINS $keyword
        WITH n, r, m
        LIMIT $limit
        RETURN n, r, m
        """
        result = neo4j_service.graph.run(query, keyword=keyword, limit=limit).data()
        
        # 格式化结果
        nodes = []
        links = []
        node_set = set()  # 用于去重
        
        for record in result:
            source = record['n']
            target = record['m']
            rel = record['r']
            
            # 添加源节点
            if source.identity not in node_set:
                nodes.append({
                    'id': source.identity,
                    'name': source.get('name', ''),
                    'type': list(source.labels)[0] if source.labels else 'Unknown',
                    'properties': dict(source)
                })
                node_set.add(source.identity)
            
            # 添加目标节点
            if target.identity not in node_set:
                nodes.append({
                    'id': target.identity,
                    'name': target.get('name', ''),
                    'type': list(target.labels)[0] if target.labels else 'Unknown',
                    'properties': dict(target)
                })
                node_set.add(target.identity)
            
            # 添加关系
            links.append({
                'source': source.identity,
                'target': target.identity,
                'type': type(rel).__name__,
                'properties': dict(rel)
            })
        
        return jsonify({
            'success': True,
            'data': {
                'nodes': nodes,
                'links': links
            }
        })
    except Exception as e:
        print(f"搜索知识图谱时出错: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/node/<int:node_id>', methods=['GET'])
def get_node_relations(node_id):
    """获取节点的关系"""
    try:
        # 查询节点的所有关系
        query = """
        MATCH (n)-[r]-(m)
        WHERE id(n) = $node_id
        RETURN n, r, m
        """
        result = neo4j_service.graph.run(query, node_id=node_id).data()
        
        # 格式化结果
        nodes = []
        links = []
        node_set = set()
        
        for record in result:
            source = record['n']
            target = record['m']
            rel = record['r']
            
            # 添加源节点
            if source.identity not in node_set:
                nodes.append({
                    'id': source.identity,
                    'name': source.get('name', ''),
                    'type': list(source.labels)[0] if source.labels else 'Unknown',
                    'properties': dict(source)
                })
                node_set.add(source.identity)
            
            # 添加目标节点
            if target.identity not in node_set:
                nodes.append({
                    'id': target.identity,
                    'name': target.get('name', ''),
                    'type': list(target.labels)[0] if target.labels else 'Unknown',
                    'properties': dict(target)
                })
                node_set.add(target.identity)
            
            # 添加关系
            links.append({
                'source': source.identity,
                'target': target.identity,
                'type': type(rel).__name__,
                'properties': dict(rel)
            })
        
        return jsonify({
            'success': True,
            'data': {
                'nodes': nodes,
                'links': links
            }
        })
    except Exception as e:
        print(f"获取节点关系时出错: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 