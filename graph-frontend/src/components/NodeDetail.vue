<template>
  <div class="node-detail" v-if="node">
    <a-card 
      :title="node.name" 
      :bordered="false"
      class="detail-card"
    >
      <template #extra>
        <a-tag :color="getEntityTypeColor(node.type)">
          {{ getEntityTypeName(node.type) }}
        </a-tag>
      </template>
      
      <!-- 基本信息 -->
      <a-descriptions :column="1" bordered>
        <a-descriptions-item label="ID">
          {{ node.id }}
        </a-descriptions-item>
        <a-descriptions-item label="类型">
          {{ getEntityTypeName(node.type) }}
        </a-descriptions-item>
      </a-descriptions>

      <!-- 属性信息 -->
      <template v-if="node.properties && Object.keys(node.properties).length > 0">
        <div class="section-title">属性信息</div>
        <a-descriptions :column="1" bordered>
          <a-descriptions-item 
            v-for="(value, key) in node.properties" 
            :key="key" 
            :label="key"
          >
            {{ value }}
          </a-descriptions-item>
        </a-descriptions>
      </template>

      <!-- 关系信息 -->
      <template v-if="relations && (relations.incoming.length > 0 || relations.outgoing.length > 0)">
        <div class="section-title">关系信息</div>
        
        <!-- 入边关系 -->
        <template v-if="relations.incoming.length > 0">
          <div class="relation-group">
            <div class="relation-title">入边关系</div>
            <a-list size="small" :data-source="relations.incoming">
              <template #renderItem="{ item }">
                <a-list-item>
                  <span>{{ item.source.name }}</span>
                  <a-tag :color="getRelationTypeColor(item.type)" style="margin: 0 8px">
                    {{ getRelationTypeName(item.type) }}
                  </a-tag>
                  <span>{{ item.target.name }}</span>
                </a-list-item>
              </template>
            </a-list>
          </div>
        </template>

        <!-- 出边关系 -->
        <template v-if="relations.outgoing.length > 0">
          <div class="relation-group">
            <div class="relation-title">出边关系</div>
            <a-list size="small" :data-source="relations.outgoing">
              <template #renderItem="{ item }">
                <a-list-item>
                  <span>{{ item.source.name }}</span>
                  <a-tag :color="getRelationTypeColor(item.type)" style="margin: 0 8px">
                    {{ getRelationTypeName(item.type) }}
                  </a-tag>
                  <span>{{ item.target.name }}</span>
                </a-list-item>
              </template>
            </a-list>
          </div>
        </template>
      </template>
    </a-card>
  </div>
</template>

<script setup>
import { 
  getEntityTypeName, 
  getEntityTypeColor,
  getRelationTypeName, 
  getRelationTypeColor 
} from '../config/entityConfig'

const props = defineProps({
  node: {
    type: Object,
    default: null
  },
  relations: {
    type: Object,
    default: () => ({ incoming: [], outgoing: [] })
  }
})
</script>

<style scoped>
.node-detail {
  position: absolute;
  top: 100px;
  right: 20px;
  width: 400px;
  max-height: calc(100vh - 140px);
  overflow-y: auto;
  z-index: 1000;
}

.detail-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.detail-card :deep(.ant-card-head) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px 12px 0 0;
}

.detail-card :deep(.ant-card-head-title) {
  font-size: 16px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
}

.detail-card :deep(.ant-card-body) {
  padding: 20px;
}

.section-title {
  margin: 16px 0 12px;
  font-size: 15px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
  padding-left: 8px;
  border-left: 3px solid #1890ff;
}

.relation-group {
  margin-bottom: 20px;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 8px;
  padding: 12px;
}

.relation-title {
  margin-bottom: 12px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
  font-weight: 500;
}

:deep(.ant-descriptions) {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

:deep(.ant-descriptions-item-label) {
  width: 120px;
  font-weight: 500;
  background: rgba(0, 0, 0, 0.02);
}

:deep(.ant-descriptions-item-content) {
  background: white;
}

:deep(.ant-list-item) {
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.3s;
}

:deep(.ant-list-item:hover) {
  background: rgba(0, 0, 0, 0.02);
}

:deep(.ant-tag) {
  margin: 0;
  padding: 2px 8px;
  border-radius: 4px;
}

/* 自定义滚动条样式 */
.node-detail::-webkit-scrollbar {
  width: 6px;
}

.node-detail::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
}

.node-detail::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.node-detail::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}
</style> 