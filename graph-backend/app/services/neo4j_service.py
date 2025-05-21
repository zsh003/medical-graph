from py2neo import Graph, Node, Relationship
from app.config import Config

class Neo4jService:
    def __init__(self):
        self.graph = Graph(
            uri=f"bolt://127.0.0.1:{Config.NEO4J_BOLT_PORT}",
            auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD),
            name=Config.NEO4J_DATABASE
        )

    def get_entity_info(self, name, entity_type):
        """获取实体信息"""
        query = f"""
        MATCH (n:{entity_type} {{name: $name}})
        RETURN n
        """
        result = self.graph.run(query, name=name).data()
        return result[0]['n'] if result else None

    def get_entity_statistics(self):
        """获取实体统计信息"""
        stats = {}
        for entity_type in Config.ENTITY_TYPES.keys():
            query = f"""
            MATCH (n:{entity_type})
            RETURN count(n) as count
            """
            result = self.graph.run(query).data()
            stats[entity_type] = result[0]['count']
        return stats

    def get_entities_by_type(self, entity_type):
        """获取指定类型的所有实体"""
        query = f"""
        MATCH (n:{entity_type})
        RETURN n
        """
        result = self.graph.run(query).data()
        return [record['n'] for record in result]

    def get_relation_info(self, source_name, target_name, relation_type):
        """获取关系信息"""
        query = f"""
        MATCH (source)-[r:{relation_type}]->(target)
        WHERE source.name = $source_name AND target.name = $target_name
        RETURN r
        """
        result = self.graph.run(query, source_name=source_name, target_name=target_name).data()
        return result[0]['r'] if result else None

    def get_relation_statistics(self):
        """获取关系统计信息"""
        stats = {}
        for relation_type in Config.RELATION_TYPES.keys():
            query = f"""
            MATCH ()-[r:{relation_type}]->()
            RETURN count(r) as count
            """
            result = self.graph.run(query).data()
            stats[relation_type] = result[0]['count']
        return stats

    def get_relations_by_type(self, relation_type):
        """获取指定类型的所有关系"""
        query = f"""
        MATCH (source)-[r:{relation_type}]->(target)
        RETURN source, r, target
        """
        result = self.graph.run(query).data()
        return [{
            'source': record['source'],
            'relation': record['r'],
            'target': record['target']
        } for record in result]

    def update_entity(self, entity_id, properties):
        """更新实体属性"""
        query = f"""
        MATCH (n) WHERE id(n) = $entity_id
        SET n += $properties
        RETURN n
        """
        result = self.graph.run(query, entity_id=entity_id, properties=properties).data()
        return result[0]['n'] if result else None

    def update_relation(self, source_id, target_id, relation_type, properties):
        """更新关系属性"""
        query = f"""
        MATCH (source)-[r:{relation_type}]->(target)
        WHERE id(source) = $source_id AND id(target) = $target_id
        SET r += $properties
        RETURN r
        """
        result = self.graph.run(query, source_id=source_id, target_id=target_id, properties=properties).data()
        return result[0]['r'] if result else None

    def add_entity(self, entity_type, properties):
        """添加新实体"""
        node = Node(entity_type, **properties)
        self.graph.create(node)
        return node

    def add_relation(self, source_id, target_id, relation_type, properties):
        """添加新关系"""
        query = f"""
        MATCH (source), (target)
        WHERE id(source) = $source_id AND id(target) = $target_id
        CREATE (source)-[r:{relation_type} $properties]->(target)
        RETURN r
        """
        result = self.graph.run(query, source_id=source_id, target_id=target_id, properties=properties).data()
        return result[0]['r'] if result else None

    def delete_entity(self, entity_id):
        """删除实体"""
        query = """
        MATCH (n) WHERE id(n) = $entity_id
        DETACH DELETE n
        """
        self.graph.run(query, entity_id=entity_id)
        return True

    def delete_relation(self, source_id, target_id, relation_type):
        """删除关系"""
        query = f"""
        MATCH (source)-[r:{relation_type}]->(target)
        WHERE id(source) = $source_id AND id(target) = $target_id
        DELETE r
        """
        self.graph.run(query, source_id=source_id, target_id=target_id)
        return True

    def get_entity_count(self):
        """获取实体总数"""
        query = """
        MATCH (n)
        RETURN count(n) as count
        """
        result = self.graph.run(query).data()
        return result[0]['count'] if result else 0

    def get_relation_count(self):
        """获取关系总数"""
        query = """
        MATCH ()-[r]->()
        RETURN count(r) as count
        """
        result = self.graph.run(query).data()
        return result[0]['count'] if result else 0

    def get_entity_count_by_type(self, entity_type):
        """获取指定类型的实体数量"""
        query = """
        MATCH (n {type: $type})
        RETURN count(n) as count
        """
        result = self.graph.run(query, type=entity_type).data()
        return result[0]['count'] if result else 0

    def get_recent_entities(self, limit=5):
        """获取最近的实体更新"""
        query = """
        MATCH (n)
        WHERE n.update_time IS NOT NULL
        RETURN n
        ORDER BY n.update_time DESC
        LIMIT $limit
        """
        result = self.graph.run(query, limit=limit).data()
        return [dict(node['n']) for node in result]

    def get_recent_relations(self, limit=5):
        """获取最近的关系更新"""
        query = """
        MATCH (source)-[r]->(target)
        WHERE r.update_time IS NOT NULL
        RETURN source, r, target
        ORDER BY r.update_time DESC
        LIMIT $limit
        """
        result = self.graph.run(query, limit=limit).data()
        return [{
            'source': dict(node['source']),
            'type': node['r'].type,
            'target': dict(node['target']),
            'update_time': node['r'].get('update_time')
        } for node in result] 