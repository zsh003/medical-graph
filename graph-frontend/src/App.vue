<template>
  <a-layout class="layout">
    <a-layout-header class="header">
      <div class="logo">医药知识图谱系统</div>
      <a-menu
        v-model:selectedKeys="selectedKeys"
        theme="dark"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="home">
          <router-link to="/">首页</router-link>
        </a-menu-item>
        <a-menu-item key="entity">
          <router-link to="/entity">实体识别</router-link>
        </a-menu-item>
        <a-menu-item key="relation">
          <router-link to="/relation">关系抽取</router-link>
        </a-menu-item>
        <a-menu-item key="knowledge">
          <router-link to="/knowledge">知识更新</router-link>
        </a-menu-item>
        <a-menu-item key="graph">
          <router-link to="/graph">知识图谱</router-link>
        </a-menu-item>
      </a-menu>
    </a-layout-header>
    <a-layout-content class="content">
      <router-view></router-view>
    </a-layout-content>
    <a-layout-footer class="footer">
      医药知识图谱系统 ©2024 Created by Your Company
    </a-layout-footer>
  </a-layout>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const selectedKeys = ref(['home'])

// 监听路由变化，更新导航栏选中状态
watch(
  () => route.path,
  (newPath) => {
    // 根据路径设置选中的菜单项
    const pathMap = {
      '/': 'home',
      '/entity': 'entity',
      '/relation': 'relation',
      '/knowledge': 'knowledge',
      '/graph': 'graph'
    }
    selectedKeys.value = [pathMap[newPath] || 'home']
  },
  { immediate: true }
)
</script>

<style scoped>
.layout {
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  padding: 0 24px;
}

.logo {
  color: white;
  font-size: 20px;
  font-weight: bold;
  margin-right: 48px;
}

.content {
  background: #f0f2f5;
  min-height: calc(100vh - 64px - 70px);
}

.footer {
  text-align: center;
  background: #f0f2f5;
  padding: 24px 50px;
}

:deep(.ant-menu-item a) {
  color: rgba(255, 255, 255, 0.65);
}

:deep(.ant-menu-item-selected a) {
  color: white;
}
</style>
