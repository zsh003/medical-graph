<template>
  <div class="knowledge-view">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card title="知识图谱更新" :bordered="false">
          <a-tabs v-model:activeKey="activeTab">
            <a-tab-pane key="entity" tab="实体管理">
              <a-row :gutter="16">
                <a-col :span="8">
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
                      :pagination="entityPagination"
                      @change="handleEntityPageChange"
                    >
                      <template #renderItem="{ item }">
                        <a-list-item>
                          <a-card hoverable @click="selectEntity(item)">
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
                </a-col>
                <a-col :span="16">
                  <a-card title="实体详情" :bordered="false">
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
                        <a-form-item :wrapper-col="{ offset: 4 }">
                          <a-space>
                            <a-button type="primary" @click="updateEntity">保存</a-button>
                            <a-button danger @click="deleteEntity">删除</a-button>
                          </a-space>
                        </a-form-item>
                      </a-form>
                    </template>
                    <a-empty v-else description="请选择一个实体" />
                  </a-card>
                </a-col>
              </a-row>
            </a-tab-pane>
            <a-tab-pane key="relation" tab="关系管理">
              <a-row :gutter="16">
                <a-col :span="8">
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
                      :pagination="relationPagination"
                      @change="handleRelationPageChange"
                    >
                      <template #renderItem="{ item }">
                        <a-list-item>
                          <a-card hoverable @click="selectRelation(item)">
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
                </a-col>
                <a-col :span="16">
                  <a-card title="关系详情" :bordered="false">
                    <template v-if="selectedRelation">
                      <a-form
                        :model="selectedRelation"
                        :label-col="{ span: 4 }"
                        :wrapper-col="{ span: 20 }"
                      >
                        <a-form-item label="源实体">
                          <a-select
                            v-model:value="selectedRelation.source"
                            :options="entityOptions"
                            :loading="entityLoading"
                          />
                        </a-form-item>
                        <a-form-item label="关系类型">
                          <a-select v-model:value="selectedRelation.type">
                            <a-select-option value="belongs_to">属于</a-select-option>
                            <a-select-option value="has_symptom">有症状</a-select-option>
                            <a-select-option value="has_drug">有药品</a-select-option>
                            <a-select-option value="has_food">有食物</a-select-option>
                            <a-select-option value="has_check">有检查</a-select-option>
                            <a-select-option value="produced_by">生产商</a-select-option>
                          </a-select>
                        </a-form-item>
                        <a-form-item label="目标实体">
                          <a-select
                            v-model:value="selectedRelation.target"
                            :options="entityOptions"
                            :loading="entityLoading"
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
                        <a-form-item :wrapper-col="{ offset: 4 }">
                          <a-space>
                            <a-button type="primary" @click="updateRelation">保存</a-button>
                            <a-button danger @click="deleteRelation">删除</a-button>
                          </a-space>
                        </a-form-item>
                      </a-form>
                    </template>
                    <a-empty v-else description="请选择一个关系" />
                  </a-card>
                </a-col>
              </a-row>
            </a-tab-pane>
          </a-tabs>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { message } from 'ant-design-vue'
import axios from 'axios'

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
    value: entity
  }))
})

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

const handleEntityPageChange = (page) => {
  entityPagination.value.current = page
  searchEntities()
}

const selectEntity = (entity) => {
  selectedEntity.value = { ...entity }
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
      searchEntities()
    }
  } catch (error) {
    message.error('更新失败：' + error.message)
  }
}

const deleteEntity = async () => {
  try {
    const response = await axios.delete(`/api/entity/${selectedEntity.value.id}`)
    if (response.data.success) {
      message.success('删除成功')
      selectedEntity.value = null
      searchEntities()
    }
  } catch (error) {
    message.error('删除失败：' + error.message)
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

const handleRelationPageChange = (page) => {
  relationPagination.value.current = page
  searchRelations()
}

const selectRelation = (relation) => {
  selectedRelation.value = { ...relation }
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
      searchRelations()
    }
  } catch (error) {
    message.error('更新失败：' + error.message)
  }
}

const deleteRelation = async () => {
  try {
    const response = await axios.delete(`/api/relation/${selectedRelation.value.id}`)
    if (response.data.success) {
      message.success('删除成功')
      selectedRelation.value = null
      searchRelations()
    }
  } catch (error) {
    message.error('删除失败：' + error.message)
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

const getRelationTypeColor = (type) => {
  const colorMap = {
    'belongs_to': 'purple',
    'has_symptom': 'orange',
    'has_drug': 'green',
    'has_food': 'blue',
    'has_check': 'cyan',
    'produced_by': 'magenta'
  }
  return colorMap[type] || 'default'
}

// 初始化
searchEntities()
searchRelations()
</script>

<style scoped>
.knowledge-view {
  padding: 24px;
}
</style> 