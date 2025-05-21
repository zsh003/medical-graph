from app.config import Config

class DataValidator:
    def __init__(self):
        self.entity_types = Config.ENTITY_TYPES
        self.relation_types = Config.RELATION_TYPES

    def validate_entity_data(self, data):
        """验证实体数据"""
        # 检查必要字段
        required_fields = ['type', 'properties']
        if not all(field in data for field in required_fields):
            return False

        # 检查实体类型是否有效
        if data['type'] not in self.entity_types:
            return False

        # 检查属性是否包含必要字段
        if 'name' not in data['properties']:
            return False

        return True

    def validate_relation_data(self, data):
        """验证关系数据"""
        # 检查必要字段
        required_fields = ['source_id', 'target_id', 'type', 'properties']
        if not all(field in data for field in required_fields):
            return False

        # 检查关系类型是否有效
        if data['type'] not in self.relation_types:
            return False

        return True

    def validate_entity_update(self, data):
        """验证实体更新数据"""
        # 检查必要字段
        required_fields = ['id', 'properties']
        if not all(field in data for field in required_fields):
            return False

        return True

    def validate_relation_update(self, data):
        """验证关系更新数据"""
        # 检查必要字段
        required_fields = ['source_id', 'target_id', 'type', 'properties']
        if not all(field in data for field in required_fields):
            return False

        # 检查关系类型是否有效
        if data['type'] not in self.relation_types:
            return False

        return True 