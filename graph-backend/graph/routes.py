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

    if not name or not group or not node_type:
        return jsonify({"error": "Missing required fields"}), 400

    query = """
    CREATE (n:{group} {name: $name, type: $type})
    """.format(group=group)

    with driver.session() as session:
        session.run(query, {"name": name, "type": node_type})
    return jsonify({"message": "Node added successfully"}), 201


# 添加关系的接口
@graph.route('/add_relation', methods=['POST'])
def add_relation():
    data = request.get_json()
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