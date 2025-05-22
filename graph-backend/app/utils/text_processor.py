import jieba
import re
from app.config import Config
from app.services.neo4j_service import Neo4jService

class TextProcessor:
    def __init__(self):
        self.entity_types = Config.ENTITY_TYPES
        self.relation_types = Config.RELATION_TYPES
        self.neo4j_service = Neo4jService()
        self._init_jieba()

    def _init_jieba(self):
        """初始化结巴分词"""
        # 从Neo4j中获取所有实体名称并添加到结巴分词词典
        for entity_type in self.entity_types.keys():
            entities = self.neo4j_service.get_entities_by_type(entity_type)
            for entity in entities:
                if 'name' in entity:
                    jieba.add_word(entity['name'])

    def extract_entities(self, text):
        """从文本中提取实体"""
        entities = []
        
        # 使用结巴分词进行分词
        words = jieba.lcut(text)
        
        # 对每个词进行实体类型判断
        for word in words:
            if len(word.strip()) < 2:  # 过滤掉单字词
                continue
                
            # 在Neo4j中查找实体
            for entity_type in self.entity_types.keys():
                entity_info = self.neo4j_service.get_entity_info(word, entity_type)
                if entity_info:
                    entities.append({
                        'name': word,
                        'type': entity_type,
                        'info': entity_info
                    })
                    break  # 找到一个匹配就停止继续查找
            
        return entities

    def extract_relations(self, text):
        """从文本中提取关系"""
        relations = []
        
        # 首先提取文本中的实体
        entities = self.extract_entities(text)
        if len(entities) < 2:
            return relations
            
        # 对每对实体检查是否存在关系
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                source = entities[i]
                target = entities[j]
                
                # 先查找源实体的所有关系
                query = """
                MATCH (source {name: $source_name})-[r]->(target)
                RETURN source, r, target
                """
                result = self.neo4j_service.graph.run(
                    query,
                    source_name=source['name']
                ).data()
                
                # 在关系中查找目标实体
                for rel in result:
                    if rel['target']['name'] == target['name']:
                        relations.append({
                            'source': {
                                'name': source['name'],
                                'type': source['type'],
                                'info': source['info']
                            },
                            'target': {
                                'name': target['name'],
                                'type': target['type'],
                                'info': target['info']
                            },
                            'type': type(rel['r']).__name__,
                            'properties': rel['r']
                        })
                        break
                
                # 查找目标实体的所有关系
                query = """
                MATCH (source {name: $source_name})-[r]->(target)
                RETURN source, r, target
                """
                result = self.neo4j_service.graph.run(
                    query,
                    source_name=target['name']
                ).data()
                
                # 在关系中查找源实体
                for rel in result:
                    if rel['target']['name'] == source['name']:
                        relations.append({
                            'source': {
                                'name': target['name'],
                                'type': target['type'],
                                'info': target['info']
                            },
                            'target': {
                                'name': source['name'],
                                'type': source['type'],
                                'info': source['info']
                            },
                            'type': type(rel['r']).__name__,
                            'properties': rel['r']
                        })
                        break
            
        return relations

    def _is_entity(self, word):
        """判断一个词是否是实体"""
        for entity_type in self.entity_types.keys():
            entity_info = self.neo4j_service.get_entity_info(word, entity_type)
            if entity_info:
                return True
        return False

    def _get_entity_type(self, word):
        """获取实体的类型"""
        for entity_type in self.entity_types.keys():
            entity_info = self.neo4j_service.get_entity_info(word, entity_type)
            if entity_info:
                return entity_type
        return None

    def _extract_relation_pattern(self, text):
        """使用规则模式提取关系"""
        # 这里需要实现基于规则的关系抽取逻辑
        pass

    def _extract_relation_ml(self, text):
        """使用机器学习模型提取关系"""
        # 这里需要实现基于机器学习的关系抽取逻辑
        pass 