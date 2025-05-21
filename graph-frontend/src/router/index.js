import { createRouter, createWebHistory } from 'vue-router'
import { beforeEachGuard, afterEachGuard, onErrorHandler } from './guards'
import KnowledgeGraph from "../views/KnowledgeGraph.vue";
import LogView from "../views/LogView.vue";
import RegisterView from "../views/RegisterView.vue";
import BasicLayout from "../layouts/BasicLayout.vue";
import {useAuthStore} from "../stores/authStore.js";
import AdminLoginView from "../views/admin/AdminLoginView.vue";
import AdminLayout from "../layouts/AdminLayout.vue";
import {message} from "ant-design-vue";


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [{
        path: '/',
        name: 'home',
        component: () => import('../views/HomeView.vue'),
        meta: {
            title: '首页',
            requiresAuth: false
        }
    },
        {
            path: '/login',
            name: 'login',
            component: LogView
        },
        {
            path: '/register',
            name: 'register',
            component: RegisterView
        },
        {
            path: '/admin/login',
            name: 'adminLogin',
            component: AdminLoginView
        },
        {
            path: '/admin',
            name: 'admin',
            component: AdminLayout,
            meta: {
                requiresAuth: true,
                requiresAdmin: true,
            }
        },
        {
            path: '/entity',
            name: 'entity',
            component: () => import('../views/EntityView.vue'),
            meta: {
                title: '实体识别',
                requiresAuth: false
            }
        },
        {
            path: '/relation',
            name: 'relation',
            component: () => import('../views/RelationView.vue'),
            meta: {
                title: '关系抽取',
                requiresAuth: false
            }
        },
        {
            path: '/knowledge',
            name: 'knowledge',
            component: () => import('../views/KnowledgeView.vue'),
            meta: {
                title: '知识更新',
                requiresAuth: false
            }
        },
        {
            path: '/graph',
            name: 'graph',
            component: () => import('../views/GraphView.vue'),
            meta: {
                title: '知识图谱',
                requiresAuth: false
            }
        },
        {
            path: '/:pathMatch(.*)*',
            name: 'not-found',
            component: () => import('../views/NotFoundView.vue'),
            meta: {
                title: '页面未找到',
                requiresAuth: false
            }
        }
    ]
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()
    const user = authStore.user;
    if (to.meta.requiresAdmin && user?.role !== 'admin') {
        message.error('不是管理员');

        next('/admin/login')
    }
    else if (to.meta.requiresAuth && !user) {
        next('/login')
    } else {
        next()
    }
})

// 注册路由守卫
router.beforeEach(beforeEachGuard)
router.afterEach(afterEachGuard)
router.onError(onErrorHandler)

export default router
