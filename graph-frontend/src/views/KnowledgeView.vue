<template>
  <div class="knowledge-view">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card title="知识图谱更新" :bordered="false">
          <a-tabs v-model:activeKey="activeTab">
            <a-tab-pane key="entity" tab="实体管理">
              <a-card title="实体列表" :bordered="false">
                <a-input-search
                  v-model:value="entitySearchText"
                  placeholder="搜索实体..."
                  style="margin-bottom: 16px"
                  @search="searchEntities"
                />
                <a-list
                  :data-source="entities"
                  :loading="entityLoading"
                  :pagination="{
                    current: entityPagination.current,
                    pageSize: entityPagination.pageSize,
                    total: entityPagination.total,
                    showSizeChanger: true,
                    showQuickJumper: true,
                    showTotal: (total) => `共 ${total} 条`,
                    onChange: handleEntityPageChange,
                    onShowSizeChange: handleEntityPageChange
                  }"
                >
                  <template #renderItem="{ item }">
                    <a-list-item>
                      <a-card hoverable @click="selectEntity(item)" style="width: 100%">
                        <template #title>
                          {{ item.name }}
                          <a-tag :color="getEntityTypeColor(item.type)">
                            {{ item.type }}
                          </a-tag>
                        </template>
                      </a-card>
                    </a-list-item>
                  </template>
                </a-list>
              </a-card>
            </a-tab-pane>
            <a-tab-pane key="relation" tab="关系管理">
              <a-card title="关系列表" :bordered="false">
                <a-input-search
                  v-model:value="relationSearchText"
                  placeholder="搜索关系..."
                  style="margin-bottom: 16px"
                  @search="searchRelations"
                />
                <a-list
                  :data-source="relations"
                  :loading="relationLoading"
                  :pagination="{
                    current: relationPagination.current,
                    pageSize: relationPagination.pageSize,
                    total: relationPagination.total,
                    showSizeChanger: true,
                    showQuickJumper: true,
                    showTotal: (total) => `共 ${total} 条`,
                    onChange: handleRelationPageChange,
                    onShowSizeChange: handleRelationPageChange
                  }"
                >
                  <template #renderItem="{ item }">
                    <a-list-item>
                      <a-card hoverable @click="selectRelation(item)" style="width: 100%">
                        <template #title>
                          {{ item.source.name }}
                          <a-tag :color="getRelationTypeColor(item.type)" style="margin: 0 8px">
                            {{ item.type }}
                          </a-tag>
                          {{ item.target.name }}
                        </template>
                      </a-card>
                    </a-list-item>
                  </template>
                </a-list>
              </a-card>
            </a-tab-pane>
          </a-tabs>
        </a-card>
      </a-col>
    </a-row>

    <!-- 实体详情弹窗 -->
    <a-modal
      v-model:visible="entityModalVisible"
      title="实体详情"
      width="800px"
      @ok="updateEntity"
      @cancel="entityModalVisible = false"
    >
      <template v-if="selectedEntity">
        <a-form
          :model="selectedEntity"
          :label-col="{ span: 4 }"
          :wrapper-col="{ span: 20 }"
        >
          <a-form-item label="名称">
            <a-input v-model:value="selectedEntity.name" />
          </a-form-item>
          <a-form-item label="类型">
            <a-select v-model:value="selectedEntity.type">
              <a-select-option value="Disease">疾病</a-select-option>
              <a-select-option value="Symptom">症状</a-select-option>
              <a-select-option value="Drug">药品</a-select-option>
              <a-select-option value="Food">食物</a-select-option>
              <a-select-option value="Check">检查</a-select-option>
              <a-select-option value="Department">科室</a-select-option>
              <a-select-option value="Producer">生产商</a-select-option>
            </a-select>
          </a-form-item>
          <a-form-item label="属性">
            <a-button type="primary" @click="addEntityProperty" style="margin-bottom: 16px">
              添加属性
            </a-button>
            <div v-for="(value, key) in selectedEntity.properties" :key="key" style="margin-bottom: 8px">
              <a-row :gutter="8">
                <a-col :span="10">
                  <a-input v-model:value="selectedEntity.properties[key]" placeholder="属性值" />
                </a-col>
                <a-col :span="4">
                  <a-button type="link" danger @click="removeEntityProperty(key)">
                    删除
                  </a-button>
                </a-col>
              </a-row>
            </div>
          </a-form-item>
        </a-form>
      </template>
    </a-modal>

    <!-- 关系详情弹窗 -->
    <a-modal
      v-model:visible="relationModalVisible"
      title="关系详情"
      width="800px"
      @ok="updateRelation"
      @cancel="relationModalVisible = false"
    >
      <template v-if="selectedRelation">
        <a-form
          :model="selectedRelation"
          :label-col="{ span: 4 }"
          :wrapper-col="{ span: 20 }"
        >
          <a-form-item label="关系类型">
            <a-select 
              v-model:value="selectedRelation.type"
              :options="relationTypeOptions"
              @change="handleRelationTypeChange"
            />
          </a-form-item>
          <a-form-item label="源实体">
            <a-select
              v-model:value="selectedRelation.source"
              :options="sourceEntityOptions"
              :loading="entityLoading"
              placeholder="请先选择关系类型"
            />
          </a-form-item>
          <a-form-item label="目标实体">
            <a-select
              v-model:value="selectedRelation.target"
              :options="targetEntityOptions"
              :loading="entityLoading"
              placeholder="请先选择关系类型"
            />
          </a-form-item>
          <a-form-item label="属性">
            <a-button type="primary" @click="addRelationProperty" style="margin-bottom: 16px">
              添加属性
            </a-button>
            <div v-for="(value, key) in selectedRelation.properties" :key="key" style="margin-bottom: 8px">
              <a-row :gutter="8">
                <a-col :span="10">
                  <a-input v-model:value="selectedRelation.properties[key]" placeholder="属性值" />
                </a-col>
                <a-col :span="4">
                  <a-button type="link" danger @click="removeRelationProperty(key)">
                    删除
                  </a-button>
                </a-col>
              </a-row>
            </div>
          </a-form-item>
        </a-form>
      </template>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import axios from 'axios'
import { 
  getRelationTypeName, 
  getRelationTypeColor, 
  relationTypeOptions 
} from '../config/relationConfig'

// 状态变量
const activeTab = ref('entity')
const entitySearchText = ref('')
const relationSearchText = ref('')
const entities = ref([])
const relations = ref([])
const selectedEntity = ref(null)
const selectedRelation = ref(null)
const entityLoading = ref(false)
const relationLoading = ref(false)
const entityModalVisible = ref(false)
const relationModalVisible = ref(false)

// 分页配置
const entityPagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

const relationPagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

// 实体选项
const entityOptions = computed(() => {
  return entities.value.map(entity => ({
    label: `${entity.name} (${entity.type})`,
    value: entity.id
  }))
})

// 根据关系类型获取源实体选项
const sourceEntityOptions = computed(() => {
  if (!selectedRelation.value?.type) return []
  
  const typeMap = {
    'belongs_to': ['Disease'],
    'has_symptom': ['Disease'],
    'has_drug': ['Disease'],
    'has_food': ['Disease'],
    'has_check': ['Disease'],
    'produced_by': ['Drug']
  }
  
  const allowedTypes = typeMap[selectedRelation.value.type] || []
  return entities.value
    .filter(entity => allowedTypes.includes(entity.type))
    .map(entity => ({
      label: `${entity.name} (${entity.type})`,
      value: entity.id
    }))
})

// 根据关系类型获取目标实体选项
const targetEntityOptions = computed(() => {
  if (!selectedRelation.value?.type) return []
  
  const typeMap = {
    'belongs_to': ['Department'],
    'has_symptom': ['Symptom'],
    'has_drug': ['Drug'],
    'has_food': ['Food'],
    'has_check': ['Check'],
    'produced_by': ['Producer']
  }
  
  const allowedTypes = typeMap[selectedRelation.value.type] || []
  return entities.value
    .filter(entity => allowedTypes.includes(entity.type))
    .map(entity => ({
      label: `${entity.name} (${entity.type})`,
      value: entity.id
    }))
})

// 获取所有实体（不分页）
const fetchAllEntities = async () => {
  try {
    const response = await axios.get('/api/entity/list', {
      params: {
        page: 1,
        pageSize: 10000, // 设置一个足够大的数来获取所有实体
        search: ''
      }
    })
    if (response.data.success) {
      entities.value = response.data.entities
    }
  } catch (error) {
    message.error('获取实体列表失败：' + error.message)
  }
}

// 监听关系类型变化
const handleRelationTypeChange = (type) => {
  // 清空源实体和目标实体的选择
  if (selectedRelation.value) {
    selectedRelation.value.source = undefined
    selectedRelation.value.target = undefined
  }
}

// 实体相关方法
const searchEntities = async () => {
  entityLoading.value = true
  try {
    const response = await axios.get('/api/entity/list', {
      params: {
        page: entityPagination.value.current,
        pageSize: entityPagination.value.pageSize,
        search: entitySearchText.value
      }
    })
    if (response.data.success) {
      entities.value = response.data.entities
      entityPagination.value.total = response.data.total
    }
  } catch (error) {
    message.error('获取实体列表失败：' + error.message)
  } finally {
    entityLoading.value = false
  }
}

const handleEntityPageChange = (page, pageSize) => {
  entityPagination.value.current = page
  entityPagination.value.pageSize = pageSize
  searchEntities()
}

const selectEntity = (entity) => {
  selectedEntity.value = { ...entity }
  entityModalVisible.value = true
}

const addEntityProperty = () => {
  if (!selectedEntity.value.properties) {
    selectedEntity.value.properties = {}
  }
  const key = `property_${Object.keys(selectedEntity.value.properties).length + 1}`
  selectedEntity.value.properties[key] = ''
}

const removeEntityProperty = (key) => {
  delete selectedEntity.value.properties[key]
}

const updateEntity = async () => {
  try {
    const response = await axios.put(`/api/entity/${selectedEntity.value.id}`, selectedEntity.value)
    if (response.data.success) {
      message.success('更新成功')
      entityModalVisible.value = false
      searchEntities()
    }
  } catch (error) {
    message.error('更新失败：' + error.message)
  }
}

// 关系相关方法
const searchRelations = async () => {
  relationLoading.value = true
  try {
    const response = await axios.get('/api/relation/list', {
      params: {
        page: relationPagination.value.current,
        pageSize: relationPagination.value.pageSize,
        search: relationSearchText.value
      }
    })
    if (response.data.success) {
      relations.value = response.data.relations
      relationPagination.value.total = response.data.total
    }
  } catch (error) {
    message.error('获取关系列表失败：' + error.message)
  } finally {
    relationLoading.value = false
  }
}

const handleRelationPageChange = (page, pageSize) => {
  relationPagination.value.current = page
  relationPagination.value.pageSize = pageSize
  searchRelations()
}

const selectRelation = (relation) => {
  selectedRelation.value = { ...relation }
  relationModalVisible.value = true
}

const addRelationProperty = () => {
  if (!selectedRelation.value.properties) {
    selectedRelation.value.properties = {}
  }
  const key = `property_${Object.keys(selectedRelation.value.properties).length + 1}`
  selectedRelation.value.properties[key] = ''
}

const removeRelationProperty = (key) => {
  delete selectedRelation.value.properties[key]
}

const updateRelation = async () => {
  try {
    const response = await axios.put(`/api/relation/${selectedRelation.value.id}`, selectedRelation.value)
    if (response.data.success) {
      message.success('更新成功')
      relationModalVisible.value = false
      searchRelations()
    }
  } catch (error) {
    message.error('更新失败：' + error.message)
  }
}

// 工具方法
const getEntityTypeColor = (type) => {
  const colorMap = {
    'Disease': 'red',
    'Symptom': 'orange',
    'Drug': 'green',
    'Food': 'blue',
    'Check': 'purple',
    'Department': 'cyan',
    'Producer': 'magenta'
  }
  return colorMap[type] || 'default'
}

// 初始化
onMounted(() => {
  searchEntities()
  searchRelations()
  fetchAllEntities() // 获取所有实体用于关系选择
})
</script>

<style scoped>
.knowledge-view {
  padding: 24px;
}

:deep(.ant-card-hoverable) {
  cursor: pointer;
  transition: all 0.3s;
}

:deep(.ant-card-hoverable:hover) {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
</style> 