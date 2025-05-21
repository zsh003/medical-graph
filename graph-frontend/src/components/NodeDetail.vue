<template>
  <div class="node-detail" v-if="node">
    <a-card :title="node.name" :bordered="false">
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
  top: 20px;
  right: 20px;
  width: 400px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 1000;
}

.section-title {
  margin: 16px 0 8px;
  font-size: 16px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
}

.relation-group {
  margin-bottom: 16px;
}

.relation-title {
  margin-bottom: 8px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

:deep(.ant-descriptions-item-label) {
  width: 120px;
  font-weight: 500;
}
</style> 