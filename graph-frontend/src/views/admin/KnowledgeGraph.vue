<template>
  <div class="knowledge-graph">
    <SearchBox
      v-model="searchText"
      @search="handleSearch"
    />

    <NodeDetail
      v-if="selectedNode"
      :node="selectedNode"
      :relations="nodeRelations"
    />

    <svg ref="svgContainer"></svg>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import SearchBox from '../../components/SearchBox.vue'
import NodeDetail from '../../components/NodeDetail.vue'
import { GraphRenderer } from '../../services/graphRenderService.js'
import { fetchGraphData } from '../../services/graphService.js'
import { getNodeRelations } from '../../utils/graphUtils.js'
import { getEntityTypeColor } from '../../config/entityConfig.js'

export default {
  name: 'KnowledgeGraph',
  components: {
    SearchBox,
    NodeDetail
  },
  setup() {
    const svgContainer = ref(null)
    const searchText = ref('')
    let currentSimulation = null
    let currentNodes = null
    let currentLinks = null
    let svg = null
    let isSpacePressed = false
    let zoom = null
    const selectedNode = ref(null)
    const nodeRelations = ref({ incoming: [], outgoing: [] })
    const isCtrlPressed = ref(false)

    // 处理键盘事件
    const handleKeyDown = (event) => {
      if (event.code === 'Space' && !isSpacePressed) {
        event.preventDefault()
        isSpacePressed = true
        svg.style('cursor', 'grab')
      }
      if (event.ctrlKey || event.metaKey) {
        isCtrlPressed.value = true
        updateNodeHoverStyle()
      }
    }

    const handleKeyUp = (event) => {
      if (event.code === 'Space') {
        isSpacePressed = false
        svg.style('cursor', 'default')
      }
      if (!event.ctrlKey && !event.metaKey) {
        isCtrlPressed.value = false
        updateNodeHoverStyle()
      }
    }

    // 获取节点颜色
    const getNodeColor = (group) => {
      return getEntityTypeColor(group)
    }

    // 获取节点半径
    const getNodeRadius = (id) => {
      return id.length * 5 + 10
    }

    // 高亮相关节点
    const highlightRelatedNodes = (targetNode) => {
      // 高亮目标节点
      currentNodes.selectAll('circle')
        .attr('fill', d => {
          if (d.id === targetNode.id) return '#1890ff'
          return getNodeColor(d.group)
        })
        .attr('r', d => {
          if (d.id === targetNode.id) return getNodeRadius(d.id) * 1.2
          return getNodeRadius(d.id)
        })

      // 找到相关的连接
      const relatedLinks = currentLinks.filter(d =>
        d.source.id === targetNode.id || d.target.id === targetNode.id
      )

      // 高亮相关连接
      currentLinks.selectAll('line')
        .attr('stroke', d => {
          if (d.source.id === targetNode.id || d.target.id === targetNode.id) {
            return '#1890ff'
          }
          return '#999'
        })
        .attr('stroke-width', d => {
          if (d.source.id === targetNode.id || d.target.id === targetNode.id) {
            return 2
          }
          return 1
        })
        .attr('opacity', d => {
          if (d.source.id === targetNode.id || d.target.id === targetNode.id) {
            return 1
          }
          return 0.6
        })

      // 高亮相关文本
      currentLinks.selectAll('text')
        .attr('fill', d => {
          if (d.source.id === targetNode.id || d.target.id === targetNode.id) {
            return '#1890ff'
          }
          return '#666'
        })
        .style('font-weight', d => {
          if (d.source.id === targetNode.id || d.target.id === targetNode.id) {
            return 'bold'
          }
          return 'normal'
        })
        .attr('opacity', d => {
          if (d.source.id === targetNode.id || d.target.id === targetNode.id) {
            return 1
          }
          return 0.6
        })

      // 高亮相关节点
      const relatedNodeIds = new Set()
      relatedLinks.each(d => {
        relatedNodeIds.add(d.source.id)
        relatedNodeIds.add(d.target.id)
      })

      currentNodes.selectAll('circle')
        .attr('fill', d => {
          if (d.id === targetNode.id) return '#1890ff'
          if (relatedNodeIds.has(d.id)) return '#69c0ff'
          return getNodeColor(d.group)
        })
        .attr('opacity', d => {
          if (d.id === targetNode.id || relatedNodeIds.has(d.id)) {
            return 1
          }
          return 0.4
        })
        .attr('stroke', d => {
          if (d.id === targetNode.id) return '#096dd9'
          if (relatedNodeIds.has(d.id)) return '#1890ff'
          return 'none'
        })
        .attr('stroke-width', 2)

      // 高亮节点文本
      currentNodes.selectAll('text')
        .attr('fill', d => {
          if (d.id === targetNode.id || relatedNodeIds.has(d.id)) {
            return '#fff'
          }
          return '#fff'
        })
        .attr('opacity', d => {
          if (d.id === targetNode.id || relatedNodeIds.has(d.id)) {
            return 1
          }
          return 0.4
        })
        .style('font-weight', d => {
          if (d.id === targetNode.id || relatedNodeIds.has(d.id)) {
            return 'bold'
          }
          return 'normal'
        })
    }

    // 处理搜索
    const handleSearch = () => {
      if (!currentNodes || !searchText.value) return

      const searchTerm = searchText.value.toLowerCase()

      // 重置所有节点样式
      currentNodes.selectAll('circle')
        .attr('fill', d => getNodeColor(d.group))
        .attr('r', d => getNodeRadius(d.id))

      currentLinks.selectAll('line')
        .attr('stroke', '#999')
        .attr('stroke-width', 1)

      // 找到匹配的节点
      const matchedNode = currentSimulation.nodes()
        .find(node => node.id.toLowerCase().includes(searchTerm))

      if (matchedNode) {
        highlightRelatedNodes(matchedNode)

        // 获取 SVG 容器的尺寸
        const svgElement = svgContainer.value
        const width = svgElement.clientWidth
        const height = svgElement.clientHeight

        // 计算需要移动的距离
        const moveX = width / 2
        const moveY = height / 2

        // 直接移动节点到中心
        matchedNode.fx = moveX
        matchedNode.fy = moveY

        // 重启模拟器，但设置较小的alpha值使移动更平滑
        currentSimulation
          .alpha(0.3)
          .restart()

        // 等待节点移动完成后释放固定位置
        setTimeout(() => {
          matchedNode.fx = null
          matchedNode.fy = null
          currentSimulation
            .alpha(0.1)
            .restart()
        }, 1000)

        // 同时调整视图以确保节点在视野中心
        svg.transition()
          .duration(1000)
          .call(
            zoom.transform,
            d3.zoomIdentity
              .translate(width/2, height/2)
              .scale(1.2)
              .translate(-moveX, -moveY)
          )
      }
    }

    // 拖拽相关函数
    const dragstarted = (event) => {
      if (!event.active) currentSimulation.alphaTarget(0.3).restart()
      event.subject.fx = event.subject.x
      event.subject.fy = event.subject.y
    }

    const dragged = (event) => {
      event.subject.fx = event.x
      event.subject.fy = event.y
    }

    const dragended = (event) => {
      if (!event.active) currentSimulation.alphaTarget(0)
      event.subject.fx = null
      event.subject.fy = null
    }

    // 处理节点鼠标悬停
    const handleNodeMouseover = (event, d) => {
      selectedNode.value = d
      nodeRelations.value = getNodeRelations(d, currentSimulation.force('link').links())
      highlightRelatedNodes(d)
    }

    // 处理节点鼠标移出
    const handleNodeMouseout = () => {
      selectedNode.value = null
      nodeRelations.value = { incoming: [], outgoing: [] }
      
      // 重置所有节点样式
      currentNodes.selectAll('circle')
        .attr('fill', d => getNodeColor(d.group))
        .attr('r', d => getNodeRadius(d.id))
        .attr('opacity', 1)
        .attr('stroke', 'none')
        .attr('stroke-width', 0)

      currentLinks.selectAll('line')
        .attr('stroke', '#999')
        .attr('stroke-width', 1)
        .attr('opacity', 0.6)

      currentLinks.selectAll('text')
        .attr('fill', '#666')
        .style('font-weight', 'normal')
        .attr('opacity', 0.6)
    }

    // 更新节点的鼠标悬停样式
    const updateNodeHoverStyle = () => {
      if (!currentNodes) return

      currentNodes
        .style('cursor', isCtrlPressed.value ? 'help' : 'pointer')
        .selectAll('circle')
        .classed('hoverable', isCtrlPressed.value)
    }

    // 初始化图形
    const initGraph = async () => {
      const data = await fetchGraphData()
      const width = window.innerWidth
      const height = window.innerHeight - 100

      const renderer = new GraphRenderer(svgContainer.value, width, height)

      // 初始化缩放
      zoom = renderer.initZoom()
      svg = renderer.svg

      // 初始化力导向图
      currentSimulation = renderer.initSimulation(data)

      // 渲染图形
      const { nodes, links } = renderer.renderGraph(data, {
        onNodeMouseover: handleNodeMouseover,
        onNodeMouseout: handleNodeMouseout
      })

      // 设置节点文本
      nodes.selectAll('text')
        .attr('dy', 4)
        .attr('text-anchor', 'middle')
        .style('font-size', '12px')
        .style('fill', '#fff')
        .style('pointer-events', 'none')
        .style('text-shadow', '0 1px 2px rgba(0,0,0,0.5)')

      // 设置关系标签
      links.selectAll('text')
        .attr('dy', -3)
        .attr('text-anchor', 'middle')
        .style('font-size', '12px')
        .style('fill', '#666')
        .style('pointer-events', 'none')
        .style('text-shadow', '0 1px 2px rgba(255,255,255,0.8)')
        .text(d => getRelationTypeName(d.type))

      currentNodes = nodes
      currentLinks = links

      // 设置拖拽
      renderer.setupDrag(dragstarted, dragged, dragended)

      // 设置tick更新
      renderer.setupSimulationTick()
    }

    onMounted(() => {
      initGraph()
      window.addEventListener('keydown', handleKeyDown)
      window.addEventListener('keyup', handleKeyUp)
    })

    onBeforeUnmount(() => {
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('keyup', handleKeyUp)
    })

    return {
      svgContainer,
      searchText,
      handleSearch,
      selectedNode,
      nodeRelations,
      isCtrlPressed
    }
  }
}
</script>

<style scoped>
.knowledge-graph {
  width: 100%;
  height: calc(100vh - 64px);
  background-color: #f5f5f5;
  position: relative;
  overflow: hidden;
}

svg {
  border: 1px solid #ddd;
  cursor: default;
}

/* 添加节点悬停效果 */
:deep(circle.hoverable) {
  transition: all 0.3s ease;
}

:deep(circle.hoverable:hover) {
  stroke: #1890ff;
  stroke-width: 3px;
  filter: drop-shadow(0 0 4px rgba(24, 144, 255, 0.5));
}

:deep(circle.hover) {
  stroke: #1890ff;
  stroke-width: 3px;
  filter: drop-shadow(0 0 4px rgba(24, 144, 255, 0.5));
}
</style>
