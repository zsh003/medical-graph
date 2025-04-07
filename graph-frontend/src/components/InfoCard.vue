<template>
  <div class="info-card" :style="style">
    <div class="info-card-header">
      <span :class="['type-tag', `type-${node.type}`]">
        {{ node.type }}
      </span>
      <h3>{{ node.id }}</h3>
      <button class="close-button" @click="$emit('close')">×</button>
    </div>
    <div class="info-card-content">
      <div class="info-section" v-if="relations.incoming.length">
        <h4>被影响</h4>
        <ul>
          <li v-for="rel in relations.incoming" :key="rel.id">
            {{ rel.source }} <span class="relation-text">{{ rel.relation }}</span>
          </li>
        </ul>
      </div>
      <div class="info-section" v-if="relations.outgoing.length">
        <h4>影响</h4>
        <ul>
          <li v-for="rel in relations.outgoing" :key="rel.id">
            <span class="relation-text">{{ rel.relation }}</span> {{ rel.target }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InfoCard',
  props: {
    node: {
      type: Object,
      required: true
    },
    relations: {
      type: Object,
      required: true
    },
    style: {
      type: Object,
      default: () => ({
        top: '20px',
        left: '20px'
      })
    }
  },
  emits: ['close']
}
</script>

<style scoped>
.info-card {
  position: absolute;
  width: 300px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.info-card-header {
  padding: 16px;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  gap: 12px;
}

.info-card-header h3 {
  margin: 0;
  flex-grow: 1;
  font-size: 18px;
  color: #2c3e50;
}

.type-tag {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.type-药品 {
  background: #fff1f0;
  color: #cf1322;
}

.type-症状 {
  background: #f6ffed;
  color: #389e0d;
}

.type-疾病 {
  background: #e6f7ff;
  color: #096dd9;
}

.close-button {
  background: none;
  border: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  padding: 4px 8px;
  transition: all 0.3s;
}

.close-button:hover {
  color: #666;
}

.info-card-content {
  padding: 16px;
}

.info-section {
  margin-bottom: 16px;
}

.info-section h4 {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
}

.info-section ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.info-section li {
  padding: 6px 0;
  color: #2c3e50;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.relation-text {
  color: #666;
  font-size: 12px;
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 4px;
}
</style> 