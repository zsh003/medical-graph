<template>
  <div class="search-container">
    <div class="search-box">
      <input 
        type="text" 
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        @keyup.enter="$emit('search')"
        placeholder="搜索药品、症状或疾病..."
        class="search-input"
      />
      <button class="search-button" @click="$emit('search')">
        <svg viewBox="0 0 24 24" width="20" height="20">
          <path fill="currentColor" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
        </svg>
      </button>
    </div>
    <div class="tips">
      <div class="tip">提示：按住空格键可拖动画布</div>
      <div class="tip">按住 Ctrl 键悬停在节点上可查看详细信息</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchBox',
  props: {
    modelValue: String
  },
  emits: ['update:modelValue', 'search']
}
</script>

<style scoped>
.search-container {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
  text-align: center;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 300px;
  padding: 8px 16px;
  padding-right: 40px;
  font-size: 16px;
  border: 2px solid #2c3e50;
  border-radius: 20px;
  outline: none;
  transition: all 0.3s;
  background-color: rgba(255, 255, 255, 0.9);
}

.search-button {
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.search-button:hover {
  color: #40a9ff;
}

.search-input:focus {
  border-color: #40a9ff;
  box-shadow: 0 0 8px rgba(64, 169, 255, 0.5);
}

.tips {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 8px;
  animation: fadeIn 0.5s ease-out;
}

.tip {
  color: #666;
  font-size: 12px;
  background: rgba(255, 255, 255, 0.8);
  padding: 4px 8px;
  border-radius: 4px;
  backdrop-filter: blur(4px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 