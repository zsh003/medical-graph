from flask import Flask, jsonify, Blueprint, request
from neo4j import GraphDatabase
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# Neo4j 配置
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "123456"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
graph = Blueprint('graph', __name__)


def get_graph_data(tx):
    # 查询所有节点和关系
    query = """
    MATCH (n)
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n, r, m
    """
    result = tx.run(query)

    nodes = []
    links = []
    node_ids = set()  # 用于去重

    for record in result:
        # 处理节点
        node = record["n"]
        if node.id not in node_ids:
            nodes.append({
                "id": node["name"],
                "group": node["group"],
                "type": node["type"]
            })
            node_ids.add(node.id)

        # 处理目标节点
        target_node = record["m"]
        if target_node and target_node.id not in node_ids:
            nodes.append({
                "id": target_node["name"],
                "group": target_node["group"],
                "type": target_node["type"]
            })
            node_ids.add(target_node.id)

        # 处理关系
        relation = record["r"]
        if relation:
            links.append({
                "source": node["name"],
                "target": target_node["name"],
                "relation": type(relation).__name__,
                "value": relation["value"]
            })

    return {"nodes": nodes, "links": links}


@graph.route('/data', methods=['GET'])
def graph_data():
    with driver.session() as session:
        data = session.execute_read(get_graph_data)
    return jsonify(data), 200


# 添加节点的接口
@graph.route('/add_node', methods=['POST'])
def add_node():
    data = request.get_json()
    name = data.get('name')
    group = data.get('group')
    node_type = data.get('type')

    print(data)
    if not all([name, group, node_type]):
        return jsonify({"error": "Missing required fields"}), 400

    # 使用参数化查询以防止注入攻击
    query = """
    CREATE (n:%s {name: $name, group: $group, type: $type})
    """

    with driver.session() as session:
        try:
            session.run(query % node_type, {"name": name,"group": group, "type": node_type})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Node added successfully"}), 201


from flask import request, jsonify

from flask import request, jsonify


@graph.route('/<path:name>', methods=['DELETE'])
def delete_node(name):
    if not name:
        return jsonify({"error": "Missing required field 'name'"}), 400

    # Cypher查询，用于删除指定名称的节点
    query = """
    MATCH (n {name: $name})
    DETACH DELETE n
    """

    with driver.session() as session:
        try:
            result = session.run(query, {"name": name})
            summary = result.consume()
            # 检查是否实际删除了节点
            if summary.counters.nodes_deleted == 0:
                return jsonify({"message": "No node found with the given name."}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Node deleted successfully"}), 200


# 添加关系的接口
@graph.route('/add_relation', methods=['POST'])
def add_relation():
    data = request.get_json()
    print(data)
    start_node_name = data.get('start_node_name')
    end_node_name = data.get('end_node_name')
    relation_type = data.get('relation_type')

    if not start_node_name or not end_node_name or not relation_type:
        return jsonify({"error": "Missing required fields"}), 400

    query = """
    MATCH (a),(b) WHERE a.name = $start AND b.name = $end CREATE (a)-[r:%s]->(b)
    """ % relation_type

    with driver.session() as session:
        session.run(query, {"start": start_node_name, "end": end_node_name})
    return jsonify({"message": "Relation added successfully"}), 201