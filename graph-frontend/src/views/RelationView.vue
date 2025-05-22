<template>
  <div class="relation-view">
    <a-row :gutter="16">
      <a-col :span="12">
        <a-card title="文本输入" :bordered="false">
          <a-textarea
            v-model:value="inputText"
            placeholder="请输入医疗文本..."
            :rows="10"
          />
          <a-button
            type="primary"
            @click="extractRelations"
            :loading="loading"
            style="margin-top: 16px"
          >
            抽取关系
          </a-button>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card title="关系抽取结果" :bordered="false">
          <div v-if="relations.length > 0">
            <a-list
              :data-source="relations"
              :grid="{ gutter: 16, column: 1 }"
            >
              <template #renderItem="{ item }">
                <a-list-item>
                  <a-card>
                    <template #title>
                      <span>{{ item.source.name }}</span>
                      <a-tag :color="getRelationTypeColor(item.type)" style="margin: 0 8px">
                        {{ getRelationTypeName(item.type) }}
                      </a-tag>
                      <span>{{ item.target.name }}</span>
                    </template>
                    <template #extra>
                      <a-tag :color="getEntityTypeColor(item.source.type)">{{ getEntityTypeName(item.source.type) }}</a-tag>
                      <a-tag :color="getEntityTypeColor(item.target.type)">{{ getEntityTypeName(item.target.type) }}</a-tag>
                    </template>
                    <div v-if="item.properties" class="relation-properties">
                      <p v-for="(value, key) in item.properties" :key="key" class="property-item">
                        <span class="property-label">{{ key }}:</span>
                        <span class="property-value">{{ value }}</span>
                      </p>
                    </div>
                  </a-card>
                </a-list-item>
              </template>
            </a-list>
          </div>
          <a-empty v-else description="暂无关系抽取结果" />
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import axios from 'axios'
import { getEntityTypeName, getEntityTypeColor } from '../config/entityConfig'
import { getRelationTypeName, getRelationTypeColor } from '../config/relationConfig'

const inputText = ref('肺泡蛋白质沉积症是否会造成乏力、呼吸困难等症状？')
const relations = ref([])
const loading = ref(false)

const extractRelations = async () => {
  if (!inputText.value) {
    message.warning('请输入文本内容')
    return
  }

  loading.value = true
  try {
    const response = await axios.post('/api/relation/extract', {
      text: inputText.value
    })
    if (response.data.success) {
      relations.value = response.data.relations
    } else {
      message.error(response.data.error || '关系抽取失败')
    }
  } catch (error) {
    message.error('请求失败：' + error.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.relation-view {
  padding: 24px;
}

.relation-properties {
  margin-top: 8px;
}

.property-item {
  margin: 4px 0;
  display: flex;
  align-items: baseline;
}

.property-label {
  font-weight: bold;
  margin-right: 8px;
  color: #666;
}

.property-value {
  color: #333;
}
</style> 