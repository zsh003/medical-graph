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
            <a-col :span="8">
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
            <a-col :span="8">
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
            <a-col :span="8">
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
          </a-row>
        </a-card>
      </a-col>

      <!-- 最近更新卡片 -->
      <a-col :span="24">
        <a-card title="最近更新" :bordered="false">
          <a-list
            :data-source="recentUpdates"
            :loading="loading"
            :pagination="{ pageSize: 5 }"
          >
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta>
                  <template #title>
                    {{ item.title }}
                  </template>
                  <template #description>
                    {{ item.description }}
                  </template>
                  <template #avatar>
                    <a-avatar :style="{ backgroundColor: item.color }">
                      {{ item.icon }}
                    </a-avatar>
                  </template>
                </a-list-item-meta>
                <div>{{ item.time }}</div>
              </a-list-item>
            </template>
          </a-list>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  DatabaseOutlined,
  LinkOutlined,
  MedicineBoxOutlined,
  ExperimentOutlined,
  SearchOutlined
} from '@ant-design/icons-vue'
import axios from 'axios'

const loading = ref(false)
const statistics = ref({
  entityCount: 0,
  relationCount: 0,
  diseaseCount: 0,
  drugCount: 0
})

const recentUpdates = ref([])

const fetchStatistics = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/statistics')
    if (response.data.success) {
      statistics.value = response.data.statistics
    }
  } catch (error) {
    console.error('获取统计数据失败：', error)
  } finally {
    loading.value = false
  }
}

const fetchRecentUpdates = async () => {
  try {
    const response = await axios.get('/api/updates/recent')
    if (response.data.success) {
      recentUpdates.value = response.data.updates
    }
  } catch (error) {
    console.error('获取最近更新失败：', error)
  }
}

onMounted(() => {
  fetchStatistics()
  fetchRecentUpdates()
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
</style> 