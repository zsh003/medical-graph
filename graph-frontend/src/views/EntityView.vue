<template>
  <div class="entity-view">
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
            @click="recognizeEntities"
            :loading="loading"
            style="margin-top: 16px"
          >
            识别实体
          </a-button>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card title="识别结果" :bordered="false">
          <div v-if="entities.length > 0">
            <a-list
              :data-source="entities"
              :grid="{ gutter: 16, column: 2 }"
            >
              <template #renderItem="{ item }">
                <a-list-item>
                  <a-card :title="item.name">
                    <template #extra>
                      <a-tag :color="getEntityTypeColor(item.type)">
                        {{ item.type }}
                      </a-tag>
                    </template>
                    <p v-for="(value, key) in item.info" :key="key">
                      {{ key }}: {{ value }}
                    </p>
                  </a-card>
                </a-list-item>
              </template>
            </a-list>
          </div>
          <a-empty v-else description="暂无识别结果" />
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'
import axios from 'axios'

const inputText = ref('')
const entities = ref([])
const loading = ref(false)

const recognizeEntities = async () => {
  if (!inputText.value) {
    message.warning('请输入文本内容')
    return
  }

  loading.value = true
  try {
    const response = await axios.post('/api/entity/recognize', {
      text: inputText.value
    })
    if (response.data.success) {
      entities.value = response.data.entities
    } else {
      message.error(response.data.error || '识别失败')
    }
  } catch (error) {
    message.error('请求失败：' + error.message)
  } finally {
    loading.value = false
  }
}

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
</script>

<style scoped>
.entity-view {
  padding: 24px;
}
</style> 