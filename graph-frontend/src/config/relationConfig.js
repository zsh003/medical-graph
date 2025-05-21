// 关系类型中文名称映射
export const relationTypeMap = {
  'belongs_to': '属于',
  'has_symptom': '有症状',
  'has_drug': '有药品',
  'has_food': '有食物',
  'has_check': '有检查',
  'produced_by': '生产商',
  'drugs_of': '对应通用名',
  'recommand_drug': '推荐用药',
  'recommand_eat': '推荐食用',
  'need_check': '需要检查',
  'no_eat': '忌食',
  'do_eat': '宜食',
  'common_drug': '常用药',
  'acompany_with': '并发'
}

// 关系类型颜色映射
export const relationColorMap = {
  'belongs_to': 'purple',
  'has_symptom': 'orange',
  'has_drug': 'green',
  'has_food': 'blue',
  'has_check': 'cyan',
  'produced_by': 'magenta',
  'drugs_of': 'red',
  'recommand_drug': 'volcano',
  'recommand_eat': 'lime',
  'need_check': 'geekblue',
  'no_eat': 'red',
  'do_eat': 'green',
  'common_drug': 'gold',
  'acompany_with': 'purple'
}

// 关系类型选项列表
export const relationTypeOptions = Object.entries(relationTypeMap).map(([value, label]) => ({
  label,
  value
}))

// 获取关系类型中文名称
export const getRelationTypeName = (type) => {
  return relationTypeMap[type] || type
}

// 获取关系类型颜色
export const getRelationTypeColor = (type) => {
  return relationColorMap[type] || 'default'
} 