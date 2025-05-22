<template>
  <div class="home-view">
    <a-row :gutter="[16, 16]">
      <!-- 系统概览卡片 -->
      <a-col :span="24">
        <a-card title="系统概览" :bordered="false">
          <a-row :gutter="16">
            <a-col :span="6">
              <a-statistic
                title="实体总数"
                :value="statistics.entityCount"
                :loading="loading"
              >
                <template #prefix>
                  <database-outlined />
                </template>
              </a-statistic>
            </a-col>
            <a-col :span="6">
              <a-statistic
                title="关系总数"
                :value="statistics.relationCount"
                :loading="loading"
              >
                <template #prefix>
                  <link-outlined />
                </template>
              </a-statistic>
            </a-col>
            <a-col :span="6">
              <a-statistic
                title="疾病数量"
                :value="statistics.diseaseCount"
                :loading="loading"
              >
                <template #prefix>
                  <medicine-box-outlined />
                </template>
              </a-statistic>
            </a-col>
            <a-col :span="6">
              <a-statistic
                title="药品数量"
                :value="statistics.drugCount"
                :loading="loading"
              >
                <template #prefix>
                  <experiment-outlined />
                </template>
              </a-statistic>
            </a-col>
          </a-row>
        </a-card>
      </a-col>

      <!-- 功能入口卡片 -->
      <a-col :span="24">
        <a-card title="功能入口" :bordered="false">
          <a-row :gutter="16">
            <a-col :span="6">
              <a-card hoverable @click="$router.push('/entity')">
                <template #cover>
                  <div class="feature-image entity-image">
                    <search-outlined />
                  </div>
                </template>
                <a-card-meta title="实体识别">
                  <template #description>
                    从医疗文本中识别疾病、症状、药品等实体
                  </template>
                </a-card-meta>
              </a-card>
            </a-col>
            <a-col :span="6">
              <a-card hoverable @click="$router.push('/relation')">
                <template #cover>
                  <div class="feature-image relation-image">
                    <link-outlined />
                  </div>
                </template>
                <a-card-meta title="关系抽取">
                  <template #description>
                    分析实体之间的关系，构建知识图谱
                  </template>
                </a-card-meta>
              </a-card>
            </a-col>
            <a-col :span="6">
              <a-card hoverable @click="$router.push('/knowledge')">
                <template #cover>
                  <div class="feature-image knowledge-image">
                    <database-outlined />
                  </div>
                </template>
                <a-card-meta title="知识更新">
                  <template #description>
                    管理知识图谱中的实体和关系
                  </template>
                </a-card-meta>
              </a-card>
            </a-col>
            <a-col :span="6">
              <a-card hoverable @click="$router.push('/graph')">
                <template #cover>
                  <div class="feature-image graph-image">
                    <project-outlined />
                  </div>
                </template>
                <a-card-meta title="知识图谱">
                  <template #description>
                    可视化展示知识图谱网络结构
                  </template>
                </a-card-meta>
              </a-card>
            </a-col>
          </a-row>
        </a-card>
      </a-col>

      <!-- 数据可视化卡片 -->
      <a-col :span="24">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-card title="实体类型分布" :bordered="false">
              <div ref="entityTypeChart" class="chart-container"></div>
            </a-card>
          </a-col>
          <a-col :span="12">
            <a-card title="关系类型分布" :bordered="false">
              <div ref="relationTypeChart" class="chart-container"></div>
            </a-card>
          </a-col>
        </a-row>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import {
  DatabaseOutlined,
  LinkOutlined,
  MedicineBoxOutlined,
  ExperimentOutlined,
  SearchOutlined,
  ProjectOutlined
} from '@ant-design/icons-vue'
import axios from 'axios'
import * as echarts from 'echarts'
import { getEntityTypeName, getEntityTypeColor } from '../config/entityConfig'
import { getRelationTypeName, getRelationTypeColor } from '../config/relationConfig'

const loading = ref(false)
const statistics = ref({
  entityCount: 0,
  relationCount: 0,
  entityTypeCounts: [],
  relationTypeCounts: []
})

const entityTypeChart = ref(null)
const relationTypeChart = ref(null)
let entityChart = null
let relationChart = null

const fetchStatistics = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/statistics')
    if (response.data.success) {
      statistics.value = response.data.statistics
      updateCharts()
    }
  } catch (error) {
    console.error('获取统计数据失败：', error)
  } finally {
    loading.value = false
  }
}

const updateCharts = () => {
  // 更新实体类型分布图表
  if (entityChart) {
    const entityTypeData = statistics.value.entityTypeCounts.map(item => ({
      value: item.count,
      name: getEntityTypeName(item.type)
    }))
    
    entityChart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center',
        type: 'scroll'
      },
      series: [
        {
          name: '实体类型分布',
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['40%', '50%'],
          avoidLabelOverlap: true,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            formatter: '{b}: {c}'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '14',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: true
          },
          data: entityTypeData
        }
      ]
    })
  }

  // 更新关系类型分布图表
  if (relationChart) {
    const relationTypeData = statistics.value.relationTypeCounts.map(item => ({
      value: item.count,
      name: getRelationTypeName(item.type)
    }))
    
    relationChart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function(params) {
          const param = params[0]
          return `${param.name}<br/>数量：${param.value}`
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: relationTypeData.map(item => item.name),
        axisLabel: {
          interval: 0,
          rotate: 30,
          fontSize: 12
        }
      },
      yAxis: {
        type: 'value',
        name: '数量'
      },
      series: [
        {
          name: '关系数量',
          type: 'bar',
          data: relationTypeData.map(item => item.value),
          itemStyle: {
            color: function(params) {
              const colorList = [
                '#91cc75', '#fac858', '#ee6666',
                '#73c0de', '#3ba272', '#fc8452',
                '#9a60b4', '#ea7ccc'
              ]
              return colorList[params.dataIndex % colorList.length]
            }
          },
          label: {
            show: true,
            position: 'top',
            formatter: '{c}'
          }
        }
      ]
    })
  }
}

onMounted(() => {
  fetchStatistics()
  
  // 初始化图表
  if (entityTypeChart.value) {
    entityChart = echarts.init(entityTypeChart.value)
  }
  if (relationTypeChart.value) {
    relationChart = echarts.init(relationTypeChart.value)
  }

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    entityChart?.resize()
    relationChart?.resize()
  })
})

onUnmounted(() => {
  // 销毁图表实例
  entityChart?.dispose()
  relationChart?.dispose()
  window.removeEventListener('resize', () => {
    entityChart?.resize()
    relationChart?.resize()
  })
})
</script>

<style scoped>
.home-view {
  padding: 24px;
}

.feature-image {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  color: #fff;
}

.entity-image {
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
}

.relation-image {
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
}

.knowledge-image {
  background: linear-gradient(135deg, #722ed1 0%, #531dab 100%);
}

.graph-image {
  background: linear-gradient(135deg, #fa8c16 0%, #d46b08 100%);
}

.chart-container {
  height: 400px;
  width: 100%;
}
</style> 