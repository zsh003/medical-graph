import { message } from 'ant-design-vue'

// 路由前置守卫
export const beforeEachGuard = (to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 医疗知识图谱系统` : '医疗知识图谱系统'

  // 检查是否需要登录权限
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 这里可以添加登录状态检查
    // const isAuthenticated = checkAuth()
    // if (!isAuthenticated) {
    //   message.warning('请先登录')
    //   next({ path: '/login' })
    //   return
    // }
  }

  // 检查是否需要特定权限
  if (to.matched.some(record => record.meta.permissions)) {
    // 这里可以添加权限检查
    // const hasPermission = checkPermissions(to.meta.permissions)
    // if (!hasPermission) {
    //   message.error('没有访问权限')
    //   next({ path: '/403' })
    //   return
    // }
  }

  next()
}

// 路由后置守卫
export const afterEachGuard = (to, from) => {
  // 滚动到顶部
  window.scrollTo(0, 0)

  // 可以在这里添加页面访问统计等逻辑
  console.log(`从 ${from.path} 导航到 ${to.path}`)
}

// 路由错误处理
export const onErrorHandler = (error) => {
  console.error('路由错误：', error)
  message.error('页面加载失败，请刷新重试')
} 