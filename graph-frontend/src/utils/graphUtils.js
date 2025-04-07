// 节点颜色映射
export const nodeColors = {
  1: '#ff7875', // 药品 - 红色
  2: '#73d13d', // 症状 - 绿色
  3: '#40a9ff'  // 疾病 - 蓝色
}

// 获取节点颜色
export const getNodeColor = (group) => nodeColors[group]

// 获取节点半径
export const getNodeRadius = (id) => id.length * 5 + 10

// 获取节点关系数据
export const getNodeRelations = (node, links) => {
  return {
    incoming: links
      .filter(link => link.target.id === node.id)
      .map(link => ({
        id: `${link.source.id}-${link.target.id}`,
        source: link.source.id,
        relation: link.relation
      })),
    outgoing: links
      .filter(link => link.source.id === node.id)
      .map(link => ({
        id: `${link.source.id}-${link.target.id}`,
        target: link.target.id,
        relation: link.relation
      }))
  }
} 