import * as d3 from 'd3'
import { getNodeColor, getNodeRadius } from '../utils/graphUtils'

export class GraphRenderer {
  constructor(container, width, height) {
    this.width = width
    this.height = height
    
    this.svg = d3.select(container)
      .attr('width', width)
      .attr('height', height)
    
    this.container = this.svg.append('g')
    this.simulation = null
    this.nodes = null
    this.links = null
    
    // 添加箭头定义
    this.svg.append('defs').selectAll('marker')
      .data(['arrow'])
      .enter()
      .append('marker')
      .attr('id', 'arrow')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 28)
      .attr('markerWidth', 8)
      .attr('markerHeight', 8)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', '#999')
  }

  initSimulation(data) {
    this.simulation = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink(data.links).id(d => d.id).distance(200))
      .force('charge', d3.forceManyBody().strength(-2000))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('collision', d3.forceCollide().radius(d => getNodeRadius(d.id) + 20))
    
    return this.simulation
  }

  initZoom(onZoom) {
    const zoom = d3.zoom()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        this.container.attr('transform', event.transform)
        if (onZoom) onZoom(event)
      })

    this.svg.call(zoom)
    return zoom
  }

  renderGraph(data, { onNodeClick, onNodeMouseover, onNodeMouseout } = {}) {
    // 创建连线
    this.links = this.container.append('g')
      .selectAll('g')
      .data(data.links)
      .enter()
      .append('g')

    this.links.append('line')
      .attr('stroke', '#999')
      .attr('stroke-width', 1)
      .attr('marker-end', 'url(#arrow)')

    this.links.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', -5)
      .attr('fill', '#666')
      .style('font-size', '12px')
      .text(d => d.relation)

    // 创建节点
    this.nodes = this.container.append('g')
      .selectAll('g')
      .data(data.nodes)
      .enter()
      .append('g')
      // 添加事件处理
      .on('click', onNodeClick)
      .on('mouseover', onNodeMouseover)
      .on('mouseout', onNodeMouseout)

    this.nodes.append('circle')
      .attr('r', d => getNodeRadius(d.id))
      .attr('fill', d => getNodeColor(d.group))

    this.nodes.append('text')
      .text(d => d.id)
      .attr('text-anchor', 'middle')
      .attr('dy', '.35em')
      .attr('fill', '#fff')
      .style('font-size', '14px')
      .style('font-weight', '500')

    return {
      nodes: this.nodes,
      links: this.links
    }
  }

  setupSimulationTick() {
    this.simulation.on('tick', () => {
      this.links.selectAll('line')
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)

      this.links.selectAll('text')
        .attr('x', d => (d.source.x + d.target.x) / 2)
        .attr('y', d => (d.source.y + d.target.y) / 2)

      this.nodes
        .attr('transform', d => `translate(${d.x},${d.y})`)
    })
  }

  setupDrag(onDragStart, onDrag, onDragEnd) {
    this.nodes.call(d3.drag()
      .on('start', onDragStart)
      .on('drag', onDrag)
      .on('end', onDragEnd))
  }

  // ... 其他渲染相关方法
} 