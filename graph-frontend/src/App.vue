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
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const selectedKeys = ref([route.name])
</script>

<style scoped>
.layout {
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
}

.logo {
  color: white;
  font-size: 20px;
  margin-right: 30px;
}

.content {
  padding: 24px 50px;
  background: #fff;
  margin: 24px;
  min-height: 280px;
}

.footer {
  text-align: center;
}
</style>
