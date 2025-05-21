from neo4j import GraphDatabase

# Neo4j 连接配置
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "123456"

# 初始化驱动
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def batch_import_data(tx):
    # 1. 批量创建药品节点
    drugs = [
        {"name": "阿司匹林", "group": 1, "type": "药品"},
        {"name": "布洛芬", "group": 1, "type": "药品"},
        {"name": "奥美拉唑", "group": 1, "type": "药品"},
        {"name": "辛伐他汀", "group": 1, "type": "药品"},
        {"name": "二甲双胍", "group": 1, "type": "药品"},
        {"name": "氯雷他定", "group": 1, "type": "药品"},
        {"name": "甲硝唑", "group": 1, "type": "药品"},
        {"name": "硝苯地平", "group": 1, "type": "药品"},
        {"name": "维生素C", "group": 1, "type": "药品"},
        {"name": "布地奈德", "group": 1, "type": "药品"}
    ]
    tx.run("""
    UNWIND $drugs AS drug
    CREATE (d:药品 {name: drug.name, group: drug.group, type: drug.type})
    """, drugs=drugs)

    # 2. 批量创建症状节点
    symptoms = [
        {"name": "发热", "group": 2, "type": "症状"},
        {"name": "头痛", "group": 2, "type": "症状"},
        {"name": "胃痛", "group": 2, "type": "症状"},
        {"name": "关节疼痛", "group": 2, "type": "症状"},
        {"name": "胃酸过多", "group": 2, "type": "症状"},
        {"name": "高血压", "group": 2, "type": "症状"},
        {"name": "高血糖", "group": 2, "type": "症状"},
        {"name": "过敏", "group": 2, "type": "症状"},
        {"name": "皮疹", "group": 2, "type": "症状"},
        {"name": "咳嗽", "group": 2, "type": "症状"},
        {"name": "鼻塞", "group": 2, "type": "症状"},
        {"name": "腹泻", "group": 2, "type": "症状"},
        {"name": "乏力", "group": 2, "type": "症状"},
        {"name": "眩晕", "group": 2, "type": "症状"}
    ]
    tx.run("""
    UNWIND $symptoms AS symptom
    CREATE (s:症状 {name: symptom.name, group: symptom.group, type: symptom.type})
    """, symptoms=symptoms)

    # 3. 批量创建疾病节点
    diseases = [
        {"name": "心脑血管疾病", "group": 3, "type": "疾病"},
        {"name": "高血脂", "group": 3, "type": "疾病"},
        {"name": "糖尿病", "group": 3, "type": "疾病"},
        {"name": "胃溃疡", "group": 3, "type": "疾病"},
        {"name": "关节炎", "group": 3, "type": "疾病"},
        {"name": "过敏性鼻炎", "group": 3, "type": "疾病"},
        {"name": "支气管炎", "group": 3, "type": "疾病"},
        {"name": "细菌感染", "group": 3, "type": "疾病"},
        {"name": "病毒感染", "group": 3, "type": "疾病"},
        {"name": "哮喘", "group": 3, "type": "疾病"}
    ]
    tx.run("""
    UNWIND $diseases AS disease
    CREATE (dis:疾病 {name: disease.name, group: disease.group, type: disease.type})
    """, diseases=diseases)

    # 4. 批量创建药品->症状关系（可缓解）
    drug_symptom_rels = [
        {"source": "阿司匹林", "target": "发热", "value": 1},
        {"source": "阿司匹林", "target": "头痛", "value": 1},
        {"source": "布洛芬", "target": "发热", "value": 1},
        {"source": "布洛芬", "target": "关节疼痛", "value": 1},
        {"source": "布洛芬", "target": "头痛", "value": 1},
        {"source": "奥美拉唑", "target": "胃痛", "value": 1},
        {"source": "奥美拉唑", "target": "胃酸过多", "value": 1},
        {"source": "硝苯地平", "target": "高血压", "value": 1},
        {"source": "氯雷他定", "target": "过敏", "value": 1},
        {"source": "氯雷他定", "target": "皮疹", "value": 1},
        {"source": "甲硝唑", "target": "腹泻", "value": 1},
        {"source": "维生素C", "target": "乏力", "value": 1},
        {"source": "布地奈德", "target": "咳嗽", "value": 1}
    ]
    tx.run("""
    UNWIND $rels AS rel
    MATCH (d:药品 {name: rel.source}), (s:症状 {name: rel.target})
    CREATE (d)-[:可缓解 {value: rel.value}]->(s)
    """, rels=drug_symptom_rels)

    # 5. 批量创建药品->疾病关系（用于治疗）
    drug_disease_rels = [
        {"source": "阿司匹林", "target": "心脑血管疾病", "value": 2},
        {"source": "布洛芬", "target": "关节炎", "value": 2},
        {"source": "奥美拉唑", "target": "胃溃疡", "value": 2},
        {"source": "辛伐他汀", "target": "高血脂", "value": 2},
        {"source": "辛伐他汀", "target": "心脑血管疾病", "value": 2},
        {"source": "二甲双胍", "target": "糖尿病", "value": 2},
        {"source": "氯雷他定", "target": "过敏性鼻炎", "value": 2},
        {"source": "甲硝唑", "target": "细菌感染", "value": 2},
        {"source": "硝苯地平", "target": "心脑血管疾病", "value": 2},
        {"source": "维生素C", "target": "病毒感染", "value": 2},
        {"source": "布地奈德", "target": "哮喘", "value": 2},
        {"source": "布地奈德", "target": "支气管炎", "value": 2}
    ]
    tx.run("""
    UNWIND $rels AS rel
    MATCH (d:药品 {name: rel.source}), (dis:疾病 {name: rel.target})
    CREATE (d)-[:用于治疗 {value: rel.value}]->(dis)
    """, rels=drug_disease_rels)

    # 6. 批量创建疾病->症状关系（表现为）
    disease_symptom_rels = [
        {"source": "心脑血管疾病", "target": "高血压", "value": 1},
        {"source": "心脑血管疾病", "target": "眩晕", "value": 1},
        {"source": "关节炎", "target": "关节疼痛", "value": 1},
        {"source": "胃溃疡", "target": "胃痛", "value": 1},
        {"source": "胃溃疡", "target": "胃酸过多", "value": 1},
        {"source": "糖尿病", "target": "高血糖", "value": 1},
        {"source": "过敏性鼻炎", "target": "鼻塞", "value": 1},
        {"source": "过敏性鼻炎", "target": "过敏", "value": 1},
        {"source": "支气管炎", "target": "咳嗽", "value": 1},
        {"source": "哮喘", "target": "咳嗽", "value": 1},
        {"source": "细菌感染", "target": "发热", "value": 1},
        {"source": "病毒感染", "target": "乏力", "value": 1},
        {"source": "病毒感染", "target": "发热", "value": 1}
    ]
    tx.run("""
    UNWIND $rels AS rel
    MATCH (dis:疾病 {name: rel.source}), (s:症状 {name: rel.target})
    CREATE (dis)-[:表现为 {value: rel.value}]->(s)
    """, rels=disease_symptom_rels)


def main():
    # 执行数据导入
    with driver.session() as session:
        session.execute_write(batch_import_data)
        print("数据导入完成！")

    # 关闭驱动
    driver.close()


if __name__ == "__main__":
    main()