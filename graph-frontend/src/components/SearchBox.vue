<template>
  <div class="search-container">
    <div class="search-box">
      <a-input-search
        v-model:value="searchValue"
        placeholder="搜索药品、症状或疾病..."
        style="width: 300px"
        @search="$emit('search')"
      />
    </div>
    <div class="tips">
      <a-tag color="blue">提示：按住空格键可拖动画布</a-tag>
      <a-tag color="green">鼠标悬停在节点上可查看详细信息</a-tag>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: String
})

const emit = defineEmits(['update:modelValue', 'search'])

const searchValue = ref(props.modelValue)

watch(() => props.modelValue, (newValue) => {
  searchValue.value = newValue
})

watch(searchValue, (newValue) => {
  emit('update:modelValue', newValue)
})
</script>

<style scoped>
.search-container {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  text-align: center;
  background: rgba(255, 255, 255, 0.9);
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.search-box {
  margin-bottom: 8px;
}

.tips {
  display: flex;
  gap: 8px;
  justify-content: center;
}

:deep(.ant-input-search) {
  background: white;
}

:deep(.ant-tag) {
  margin: 0;
  padding: 4px 8px;
  font-size: 12px;
}
</style> 