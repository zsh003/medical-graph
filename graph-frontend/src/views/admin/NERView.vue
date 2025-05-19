<template>
  <div class="recognizer-container">
    <a-row :gutter="[24, 24]">
      <a-col :span="12">
        <a-card title="请输入医疗文本或上传文件">
          <a-upload :file-list="[]" :before-upload="handleFileUpload" accept=".txt">
            <a-button>点击上传文本文件</a-button>
          </a-upload>
          <br /><br />
          <a-textarea v-model:value="inputText" placeholder="请输入医疗相关文本..." :rows="8" />
          <br /><br />
          <a-button type="primary" @click="handleConvert" block>转换</a-button>
        </a-card>
      </a-col>
      <a-col :span="12">
        <a-card title="识别出的医药实体">
          <div v-if="entities.length > 0">
            <a-list item-layout="horizontal" :data-source="entities">
              <template #renderItem="{ item }">
                <a-list-item>
                  <a-list-item-meta :title="item.text" :description="`类型: ${item.type}`" />
                </a-list-item>
              </template>
            </a-list>
          </div>
          <div v-else>
            <p>暂无识别结果</p>
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'

const inputText = ref('')
const entities = ref([])

// 医药领域实体 mock 数据（CMeEE 风格），每个实体可包含多个关键词
const mockData = [
  { keywords: ['糖尿病', '血糖高'], type: '疾病' },
  { keywords: ['高血压', '血压升高'], type: '疾病' },
  { keywords: ['头痛', '头晕', '胸闷'], type: '症状' },
  { keywords: ['阿司匹林', '头孢克肟', '对乙酰氨基酚'], type: '药物' },
  { keywords: ['心脏', '肝脏', '肺部'], type: '解剖部位' },
  { keywords: ['CT扫描', 'X光检查', 'B超'], type: '检查' },
  { keywords: ['手术治疗', '放疗', '理疗'], type: '治疗' },
  { keywords: ['血常规', '尿检', '肝功能'], type: '实验室检验' },
  { keywords: ['心电图机', '呼吸机', '监护仪'], type: '设备' },
  { keywords: ['大肠杆菌', '金黄色葡萄球菌'], type: '微生物类' }
]

// 实体识别函数：从输入文本中提取匹配的实体
function recognizeEntities(text) {
  const matched = []

  for (const item of mockData) {
    for (const keyword of item.keywords) {
      if (text.includes(keyword)) {
        matched.push({
          text: keyword,
          type: item.type
        })
      }
    }
  }

  return matched
}

function handleConvert() {
  if (!inputText.value.trim()) {
    entities.value = []
    return
  }

  const result = recognizeEntities(inputText.value)
  entities.value = result
}

// 文件上传处理函数
function handleFileUpload(file) {
  const reader = new FileReader()
  reader.onload = function(e) {
    inputText.value = e.target.result
    handleConvert() // 自动调用转换函数
  }
  reader.readAsText(file)
  return false // 不自动上传文件
}
</script>

<style scoped>
.recognizer-container {
  padding: 20px;
}
</style>
