export const fetchGraphData = async () => {
  return {
    nodes: [
      // 药品节点 (group 1)
      { id: "阿司匹林", group: 1, type: "药品" },
      { id: "布洛芬", group: 1, type: "药品" },
      { id: "奥美拉唑", group: 1, type: "药品" },
      { id: "辛伐他汀", group: 1, type: "药品" },
      { id: "二甲双胍", group: 1, type: "药品" },
      { id: "氯雷他定", group: 1, type: "药品" },
      { id: "甲硝唑", group: 1, type: "药品" },
      { id: "硝苯地平", group: 1, type: "药品" },
      { id: "维生素C", group: 1, type: "药品" },
      { id: "布地奈德", group: 1, type: "药品" },

      // 症状节点 (group 2)
      { id: "发热", group: 2, type: "症状" },
      { id: "头痛", group: 2, type: "症状" },
      { id: "胃痛", group: 2, type: "症状" },
      { id: "关节疼痛", group: 2, type: "症状" },
      { id: "胃酸过多", group: 2, type: "症状" },
      { id: "高血压", group: 2, type: "症状" },
      { id: "高血糖", group: 2, type: "症状" },
      { id: "过敏", group: 2, type: "症状" },
      { id: "皮疹", group: 2, type: "症状" },
      { id: "咳嗽", group: 2, type: "症状" },
      { id: "鼻塞", group: 2, type: "症状" },
      { id: "腹泻", group: 2, type: "症状" },
      { id: "乏力", group: 2, type: "症状" },
      { id: "眩晕", group: 2, type: "症状" },

      // 疾病节点 (group 3)
      { id: "心脑血管疾病", group: 3, type: "疾病" },
      { id: "高血脂", group: 3, type: "疾病" },
      { id: "糖尿病", group: 3, type: "疾病" },
      { id: "胃溃疡", group: 3, type: "疾病" },
      { id: "关节炎", group: 3, type: "疾病" },
      { id: "过敏性鼻炎", group: 3, type: "疾病" },
      { id: "支气管炎", group: 3, type: "疾病" },
      { id: "细菌感染", group: 3, type: "疾病" },
      { id: "病毒感染", group: 3, type: "疾病" },
      { id: "哮喘", group: 3, type: "疾病" }
    ],
    links: [
      // 药品 -> 症状（治疗）
      { source: "阿司匹林", target: "发热", relation: "可缓解", value: 1 },
      { source: "阿司匹林", target: "头痛", relation: "可缓解", value: 1 },
      { source: "布洛芬", target: "发热", relation: "可缓解", value: 1 },
      { source: "布洛芬", target: "关节疼痛", relation: "可缓解", value: 1 },
      { source: "布洛芬", target: "头痛", relation: "可缓解", value: 1 },
      { source: "奥美拉唑", target: "胃痛", relation: "可缓解", value: 1 },
      { source: "奥美拉唑", target: "胃酸过多", relation: "可缓解", value: 1 },
      { source: "硝苯地平", target: "高血压", relation: "可缓解", value: 1 },
      { source: "氯雷他定", target: "过敏", relation: "可缓解", value: 1 },
      { source: "氯雷他定", target: "皮疹", relation: "可缓解", value: 1 },
      { source: "甲硝唑", target: "腹泻", relation: "可缓解", value: 1 },
      { source: "维生素C", target: "乏力", relation: "可缓解", value: 1 },
      { source: "布地奈德", target: "咳嗽", relation: "可缓解", value: 1 },

      // 药品 -> 疾病（治疗）
      { source: "阿司匹林", target: "心脑血管疾病", relation: "用于治疗", value: 2 },
      { source: "布洛芬", target: "关节炎", relation: "用于治疗", value: 2 },
      { source: "奥美拉唑", target: "胃溃疡", relation: "用于治疗", value: 2 },
      { source: "辛伐他汀", target: "高血脂", relation: "用于治疗", value: 2 },
      { source: "辛伐他汀", target: "心脑血管疾病", relation: "用于治疗", value: 2 },
      { source: "二甲双胍", target: "糖尿病", relation: "用于治疗", value: 2 },
      { source: "氯雷他定", target: "过敏性鼻炎", relation: "用于治疗", value: 2 },
      { source: "甲硝唑", target: "细菌感染", relation: "用于治疗", value: 2 },
      { source: "硝苯地平", target: "心脑血管疾病", relation: "用于治疗", value: 2 },
      { source: "维生素C", target: "病毒感染", relation: "用于治疗", value: 2 },
      { source: "布地奈德", target: "哮喘", relation: "用于治疗", value: 2 },
      { source: "布地奈德", target: "支气管炎", relation: "用于治疗", value: 2 },

      // 疾病 -> 症状（表现为）
      { source: "心脑血管疾病", target: "高血压", relation: "表现为", value: 1 },
      { source: "心脑血管疾病", target: "眩晕", relation: "表现为", value: 1 },
      { source: "关节炎", target: "关节疼痛", relation: "表现为", value: 1 },
      { source: "胃溃疡", target: "胃痛", relation: "表现为", value: 1 },
      { source: "胃溃疡", target: "胃酸过多", relation: "表现为", value: 1 },
      { source: "糖尿病", target: "高血糖", relation: "表现为", value: 1 },
      { source: "过敏性鼻炎", target: "鼻塞", relation: "表现为", value: 1 },
      { source: "过敏性鼻炎", target: "过敏", relation: "表现为", value: 1 },
      { source: "支气管炎", target: "咳嗽", relation: "表现为", value: 1 },
      { source: "哮喘", target: "咳嗽", relation: "表现为", value: 1 },
      { source: "细菌感染", target: "发热", relation: "表现为", value: 1 },
      { source: "病毒感染", target: "乏力", relation: "表现为", value: 1 },
      { source: "病毒感染", target: "发热", relation: "表现为", value: 1 }
    ]
  }
}