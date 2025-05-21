// 实体类型配置
export const entityTypes = {
  Disease: {
    name: '疾病',
    color: 'red'
  },
  Symptom: {
    name: '症状',
    color: 'orange'
  },
  Drug: {
    name: '药品',
    color: 'green'
  },
  Food: {
    name: '食物',
    color: 'blue'
  },
  Check: {
    name: '检查',
    color: 'purple'
  },
  Department: {
    name: '科室',
    color: 'cyan'
  },
  Producer: {
    name: '生产商',
    color: 'magenta'
  }
}

// 关系类型配置
export const relationTypes = {
  belongs_to: {
    name: '属于',
    color: 'blue',
    sourceType: ['Disease'],
    targetType: ['Department']
  },
  has_symptom: {
    name: '有症状',
    color: 'orange',
    sourceType: ['Disease'],
    targetType: ['Symptom']
  },
  has_drug: {
    name: '有药品',
    color: 'green',
    sourceType: ['Disease'],
    targetType: ['Drug']
  },
  has_food: {
    name: '有食物',
    color: 'cyan',
    sourceType: ['Disease'],
    targetType: ['Food']
  },
  has_check: {
    name: '有检查',
    color: 'purple',
    sourceType: ['Disease'],
    targetType: ['Check']
  },
  produced_by: {
    name: '生产商',
    color: 'magenta',
    sourceType: ['Drug'],
    targetType: ['Producer']
  },
  drugs_of: {
    name: '治疗',
    color: 'green',
    sourceType: ['Drug'],
    targetType: ['Disease']
  },
  recommand_drug: {
    name: '推荐用药',
    color: 'green',
    sourceType: ['Disease'],
    targetType: ['Drug']
  },
  recommand_eat: {
    name: '推荐食用',
    color: 'cyan',
    sourceType: ['Disease'],
    targetType: ['Food']
  },
  need_check: {
    name: '需要检查',
    color: 'purple',
    sourceType: ['Disease'],
    targetType: ['Check']
  },
  no_eat: {
    name: '忌食',
    color: 'red',
    sourceType: ['Disease'],
    targetType: ['Food']
  },
  do_eat: {
    name: '宜食',
    color: 'green',
    sourceType: ['Disease'],
    targetType: ['Food']
  },
  common_drug: {
    name: '常用药',
    color: 'green',
    sourceType: ['Disease'],
    targetType: ['Drug']
  },
  acompany_with: {
    name: '并发',
    color: 'orange',
    sourceType: ['Disease'],
    targetType: ['Disease']
  }
}

// 获取实体类型名称
export const getEntityTypeName = (type) => {
  return entityTypes[type]?.name || type
}

// 获取实体类型颜色
export const getEntityTypeColor = (type) => {
  return entityTypes[type]?.color || 'default'
}

// 获取关系类型名称
export const getRelationTypeName = (type) => {
  return relationTypes[type]?.name || type
}

// 获取关系类型颜色
export const getRelationTypeColor = (type) => {
  return relationTypes[type]?.color || 'default'
}

// 获取关系类型的源实体类型
export const getRelationSourceTypes = (type) => {
  return relationTypes[type]?.sourceType || []
}

// 获取关系类型的目标实体类型
export const getRelationTargetTypes = (type) => {
  return relationTypes[type]?.targetType || []
} 