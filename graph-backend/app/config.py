class Config:
    # Neo4j配置
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "12345678"
    NEO4J_DATABASE = "neo4j"
    NEO4J_BOLT_PORT = 7687
    NEO4J_HTTP_PORT = 7474
    
    # 实体类型配置
    ENTITY_TYPES = {
        "Disease": "疾病",
        "Symptom": "症状",
        "Drug": "药物",
        "Food": "食物",
        "Check": "检查",
        "Department": "科室",
        "Producer": "生产商",
        "CureWay": "治疗方式",
        "DrugDetail": "药品详情"
    }
    
    # 关系类型配置
    RELATION_TYPES = {
        "HAS_SYMPTOM": "症状",
        "ACOMPANY_WITH": "并发症",
        "BELONGS_TO": "所属科室",
        "CURE_WAY": "治疗方式",
        "NEED_CHECK": "诊断检查",
        "COMMON_DRUG": "常用药品",
        "RECOMMAND_DRUG": "推荐药品",
        "RECOMMAND_EAT": "推荐食谱",
        "DO_EAT": "宜吃",
        "NO_EAT": "忌吃",
        "DRUGS_OF": "生产药品"
    }
    
    # 数据处理配置
    DATA_DIR = "data"
    RAW_DATA_DIR = "data/raw"
    PROCESSED_DATA_DIR = "data/processed"
    
    # 模型配置
    MODEL_PATH = "app/models/bert_bilstm_crf"