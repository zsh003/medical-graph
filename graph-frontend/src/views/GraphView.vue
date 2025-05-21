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
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { message } from 'ant-design-vue'
import axios from 'axios'
import * as d3 from 'd3'

// 状态变量
const searchText = ref('')
const nodeLimit = ref(100)  // 默认限制100个节点
const graphContainer = ref(null)
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
    .attr('stroke', '#999')
    .attr('stroke-opacity', 0.6)
    .attr('stroke-width', 1)

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

  // 添加节点圆圈
  nodes.append('circle')
    .attr('r', 20)
    .attr('fill', d => getNodeColor(d.type))
    .attr('stroke', '#fff')
    .attr('stroke-width', 2)

  // 添加节点文本
  nodes.append('text')
    .text(d => d.name)
    .attr('text-anchor', 'middle')
    .attr('dy', 4)
    .attr('fill', '#fff')
    .style('font-size', '12px')
    .style('pointer-events', 'none')

  // 添加关系标签
  svg.select('g')
    .selectAll('text.relation')
    .data(data.links)
    .enter()
    .append('text')
    .attr('class', 'relation')
    .text(d => d.type)
    .attr('text-anchor', 'middle')
    .attr('fill', '#666')
    .style('font-size', '12px')
    .style('pointer-events', 'none')

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
  const colorMap = {
    'Disease': '#ff7875',
    'Symptom': '#73d13d',
    'Drug': '#40a9ff',
    'Food': '#ffc069',
    'Check': '#b37feb',
    'Department': '#36cfc9',
    'Producer': '#ff85c0'
  }
  return colorMap[type] || '#d9d9d9'
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
}

.search-container {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.graph-container {
  width: 100%;
  height: calc(100vh - 200px);
  background-color: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
}

:deep(circle) {
  cursor: pointer;
  transition: all 0.3s;
}

:deep(circle:hover) {
  stroke: #1890ff;
  stroke-width: 3px;
  filter: drop-shadow(0 0 4px rgba(24, 144, 255, 0.5));
}
</style> 