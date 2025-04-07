from flask import Flask, jsonify, Blueprint
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)