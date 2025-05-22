<template>
  <div class="graph-view">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card title="知识图谱" :bordered="false">
          <div class="search-container">
            <a-input-search
              v-model:value="searchText"
              placeholder="输入关键词搜索..."
              style="width: 300px"
              @search="handleSearch"
            />
            <a-input-number
              v-model:value="nodeLimit"
              :min="1"
              :max="1000"
              placeholder="节点数量限制"
              style="width: 150px; margin-left: 16px"
            />
          </div>
          <div ref="graphContainer" class="graph-container"></div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 添加节点详情组件 -->
    <NodeDetail
      v-if="selectedNode"
      :node="selectedNode"
      :relations="nodeRelations"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { message } from 'ant-design-vue'
import axios from 'axios'
import * as d3 from 'd3'
import NodeDetail from '../components/NodeDetail.vue'
import { getEntityTypeName, getEntityTypeColor, getRelationTypeName } from '../config/entityConfig'

// 状态变量
const searchText = ref('')
const nodeLimit = ref(100)  // 默认限制100个节点
const graphContainer = ref(null)
const selectedNode = ref(null)
const nodeRelations = ref({ incoming: [], outgoing: [] })
const isNodeFixed = ref(false)  // 添加节点固定状态
let simulation = null
let svg = null
let nodes = null
let links = null

// 初始化图形
const initGraph = () => {
  const width = graphContainer.value.clientWidth
  const height = window.innerHeight - 200

  // 创建SVG
  svg = d3.select(graphContainer.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)

  // 创建缩放行为
  const zoom = d3.zoom()
    .scaleExtent([0.1, 4])
    .on('zoom', (event) => {
      svg.select('g').attr('transform', event.transform)
    })

  svg.call(zoom)

  // 创建主容器
  svg.append('g')

  // 创建力导向图
  simulation = d3.forceSimulation()
    .force('link', d3.forceLink().id(d => d.id).distance(100))
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(50))
}

// 更新图形
const updateGraph = (data) => {
  if (!data || !data.nodes || !data.links) return

  // 清除现有图形
  svg.select('g').selectAll('*').remove()

  // 创建连接线
  links = svg.select('g')
    .selectAll('line')
    .data(data.links)
    .enter()
    .append('line')
    .attr('stroke', '#666')
    .attr('stroke-opacity', 0.8)
    .attr('stroke-width', 1.5)

  // 创建节点组
  nodes = svg.select('g')
    .selectAll('g')
    .data(data.nodes)
    .enter()
    .append('g')
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended))
    .on('click', handleNodeClick)  // 添加点击事件

  // 添加节点圆圈
  nodes.append('circle')
    .attr('r', 20)
    .attr('fill', d => getNodeColor(d.type))
    .attr('stroke', '#fff')
    .attr('stroke-width', 2)
    .style('filter', 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))')
    .style('cursor', 'pointer')  // 添加指针样式

  // 添加节点文本
  nodes.append('text')
    .text(d => d.name)
    .attr('text-anchor', 'middle')
    .attr('dy', 4)
    .attr('fill', '#fff')
    .style('font-size', '12px')
    .style('font-weight', 'bold')
    .style('pointer-events', 'none')
    .style('text-shadow', '0 1px 2px rgba(0,0,0,0.3)')

  // 添加关系标签
  svg.select('g')
    .selectAll('text.relation')
    .data(data.links)
    .enter()
    .append('text')
    .attr('class', 'relation')
    .text(d => getRelationTypeName(d.type))
    .attr('text-anchor', 'middle')
    .attr('fill', '#333')
    .style('font-size', '12px')
    .style('font-weight', '500')
    .style('pointer-events', 'none')
    .style('text-shadow', '0 1px 1px rgba(255,255,255,0.8)')
    .style('background-color', 'rgba(255,255,255,0.8)')  // 添加背景色
    .style('padding', '2px 4px')  // 添加内边距
    .style('border-radius', '4px')  // 添加圆角

  // 添加鼠标悬停事件
  nodes.on('mouseover', handleNodeMouseover)
      .on('mouseout', handleNodeMouseout)

  // 更新力导向图
  simulation.nodes(data.nodes)
  simulation.force('link').links(data.links)
  simulation.alpha(1).restart()

  // 更新位置
  simulation.on('tick', () => {
    links
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)

    nodes.attr('transform', d => `translate(${d.x},${d.y})`)

    svg.selectAll('text.relation')
      .attr('x', d => (d.source.x + d.target.x) / 2)
      .attr('y', d => (d.source.y + d.target.y) / 2)
  })
}

// 处理节点鼠标悬停
const handleNodeMouseover = (event, d) => {
  if (!isNodeFixed.value) {  // 只有在节点未固定时才显示悬停效果
    selectedNode.value = d
    // 获取节点关系
    nodeRelations.value = {
      incoming: simulation.force('link').links().filter(link => link.target.id === d.id),
      outgoing: simulation.force('link').links().filter(link => link.source.id === d.id)
    }
    
    // 高亮相关节点和连接
    highlightRelatedNodes(d)
  }
}

// 处理节点鼠标移出
const handleNodeMouseout = () => {
  if (!isNodeFixed.value) {  // 只有在节点未固定时才隐藏悬停效果
    selectedNode.value = null
    nodeRelations.value = { incoming: [], outgoing: [] }
    
    // 重置所有节点样式
    resetNodeStyles()
  }
}

// 处理节点点击
const handleNodeClick = (event, d) => {
  if (isNodeFixed.value && selectedNode.value && selectedNode.value.id === d.id) {
    // 如果点击的是当前固定节点，则取消固定
    isNodeFixed.value = false
    selectedNode.value = null
    nodeRelations.value = { incoming: [], outgoing: [] }
    resetNodeStyles()
  } else {
    // 固定新节点
    isNodeFixed.value = true
    selectedNode.value = d
    nodeRelations.value = {
      incoming: simulation.force('link').links().filter(link => link.target.id === d.id),
      outgoing: simulation.force('link').links().filter(link => link.source.id === d.id)
    }
    highlightRelatedNodes(d)
  }
}

// 重置节点样式
const resetNodeStyles = () => {
  nodes.selectAll('circle')
    .attr('fill', d => getNodeColor(d.type))
    .attr('stroke', '#fff')
    .attr('stroke-width', 2)
    .style('filter', 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))')

  links
    .attr('stroke', '#666')
    .attr('stroke-opacity', 0.8)
    .attr('stroke-width', 1.5)
}

// 高亮相关节点
const highlightRelatedNodes = (targetNode) => {
  // 高亮目标节点
  nodes.selectAll('circle')
    .attr('fill', d => {
      if (d.id === targetNode.id) return '#1890ff'
      return getNodeColor(d.type)
    })
    .attr('stroke', d => {
      if (d.id === targetNode.id) return '#fff'
      return '#fff'
    })
    .attr('stroke-width', d => {
      if (d.id === targetNode.id) return 3
      return 2
    })
    .style('filter', d => {
      if (d.id === targetNode.id) return 'drop-shadow(0 0 8px rgba(24, 144, 255, 0.6))'
      return 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))'
    })

  // 找到相关的连接
  const relatedLinks = simulation.force('link').links().filter(d =>
    d.source.id === targetNode.id || d.target.id === targetNode.id
  )

  // 高亮相关连接
  links
    .attr('stroke', d => {
      if (d.source.id === targetNode.id || d.target.id === targetNode.id) {
        return '#1890ff'
      }
      return '#666'
    })
    .attr('stroke-opacity', d => {
      if (d.source.id === targetNode.id || d.target.id === targetNode.id) {
        return 1
      }
      return 0.4
    })
    .attr('stroke-width', d => {
      if (d.source.id === targetNode.id || d.target.id === targetNode.id) {
        return 2
      }
      return 1.5
    })

  // 高亮相关节点文本
  nodes.selectAll('text')
    .attr('opacity', d => {
      if (d.id === targetNode.id || relatedLinks.some(link => 
        link.source.id === d.id || link.target.id === d.id)) {
        return 1
      }
      return 0.4
    })
}

// 处理搜索
const handleSearch = async () => {
  if (!searchText.value) {
    message.warning('请输入搜索关键词')
    return
  }

  try {
    const response = await axios.get('/api/graph/search', {
      params: { 
        keyword: searchText.value,
        limit: nodeLimit.value
      }
    })
    if (response.data.success) {
      updateGraph(response.data.data)
    }
  } catch (error) {
    message.error('搜索失败：' + error.message)
  }
}

// 拖拽相关函数
const dragstarted = (event, d) => {
  if (!event.active) simulation.alphaTarget(0.3).restart()
  d.fx = d.x
  d.fy = d.y
}

const dragged = (event, d) => {
  d.fx = event.x
  d.fy = event.y
}

const dragended = (event, d) => {
  if (!event.active) simulation.alphaTarget(0)
  d.fx = null
  d.fy = null
}

// 获取节点颜色
const getNodeColor = (type) => {
  return getEntityTypeColor(type)
}

// 生命周期钩子
onMounted(() => {
  initGraph()
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    if (graphContainer.value) {
      const width = graphContainer.value.clientWidth
      const height = window.innerHeight - 200
      svg.attr('width', width).attr('height', height)
      simulation.force('center', d3.forceCenter(width / 2, height / 2))
      simulation.alpha(0.3).restart()
    }
  })
})

onBeforeUnmount(() => {
  if (simulation) {
    simulation.stop()
  }
  window.removeEventListener('resize', () => {})
})
</script>

<style scoped>
.graph-view {
  padding: 24px;
  background-color: #f0f7f0;  /* 添加浅绿色背景 */
}

.search-container {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  background: rgba(255, 255, 255, 0.9);  /* 添加半透明背景 */
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.graph-container {
  width: 100%;
  height: calc(100vh - 200px);
  background-color: #c6e7c8;  /* 保持浅绿色背景 */
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);  /* 添加阴影效果 */
}

:deep(circle) {
  cursor: pointer;
  transition: all 0.3s;
}

:deep(circle:hover) {
  stroke: #1890ff;
  stroke-width: 3px;
  filter: drop-shadow(0 0 8px rgba(24, 144, 255, 0.6));
}

:deep(.ant-card) {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

:deep(.ant-input-search) {
  background: white;
}

:deep(.ant-input-number) {
  background: white;
}
</style> 