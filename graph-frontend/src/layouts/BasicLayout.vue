<template>
  <a-layout has-sider>
    <a-layout-sider
      :style="{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0, top: 0, bottom: 0 }"
    >
      <!-- 用户头像和用户名 -->
      <div class="user-info">
        <a-avatar :size="64" :src="authStore.user?.avatar_url" />
        <span class="username"> {{ authStore.user?.username }} </span>
      </div>
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline" @select="handleSelect">
        <a-menu-item v-for="item in menuItems" :key="item.key">
          <component :is="item.icon" />
          <span class="nav-text">{{ item.text }}</span>
        </a-menu-item>
        <a-menu-item @click="logout">
          <LogoutOutlined></LogoutOutlined>
          <span class="nav-text">登出</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout :style="{ marginLeft: '200px' }">

      <a-layout-content :style="{ margin: '24px 16px 0', overflow: 'initial' }">
        <component :is="currentComponent" />
      </a-layout-content>
      <a-layout-footer class="footer">
        Ant Design ©2018 Created by Ant UED
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script lang="ts" setup>
import { ref } from 'vue'
import {
  VideoCameraOutlined,
  StarOutlined,
  LockOutlined,
  TagOutlined,
  EditOutlined,
  LikeOutlined,
  LogoutOutlined,
  SettingOutlined, TeamOutlined, VideoCameraFilled, ClockCircleOutlined
} from '@ant-design/icons-vue'
import KnowledgeGraph from "../views/admin/KnowledgeGraph.vue";
import { useRouter } from 'vue-router'
import {useAuthStore} from "../stores/authStore.js";
import InfoChange from "../views/user/InfoChange.vue";
import PWDChangeView from "../views/user/PWDChangeView.vue";

const router = useRouter()
const authStore = useAuthStore()
console.log(authStore?.user)
const selectedKeys = ref<string[]>(['0'])
const menuItems = [
  { key: '0', icon: LockOutlined , text: '知识图谱', component: KnowledgeGraph },
  { key: '1', icon: EditOutlined , text: '修改信息', component: InfoChange },
  { key: '2', icon: LogoutOutlined , text: '修改密码', component: PWDChangeView },

]
// 定义当前要显示的组件
const currentComponent = ref(null)
// 处理菜单项点击事件
const handleSelect = (selected) => {
  const key = selected.key;

  // 尝试从 menuItems 找到选中的菜单项
  let selectedItem = menuItems.find(item => item.key === key);

  if (selectedItem) {
    // 如果找到了对应的菜单项，则设置 currentComponent
    if (selectedItem.component) {
      currentComponent.value = selectedItem.component;
    } else {
      console.error(`Selected menu item with key ${key} does not have a component.`);
    }
  }
};
// 初始化当前显示的组件
const initialItem = menuItems.find(item => item.key === selectedKeys.value[0])
if (initialItem) {
  currentComponent.value = initialItem.component
}

const logout = ()=>{
  authStore.logout()
  router.push('/login')
}
</script>
<style scoped>

.footer {
  text-align: center;
  background: #efefef;
  margin-top: 20px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1); /* 添加分割线 */
}

.username {
  margin-top: 12px;
  color: white;
  font-size: 16px;
  font-weight: bold;
}
</style>
