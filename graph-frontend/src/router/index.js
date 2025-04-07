import { createRouter, createWebHistory } from 'vue-router'
import KnowledgeGraph from "../views/KnowledgeGraph.vue";
import LogView from "../views/LogView.vue";
import Test from "../views/test.vue";
import RegisterView from "../views/RegisterView.vue";
import BasicLayout from "../layouts/BasicLayout.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [{
        path: '/',
        name: 'home',
        component: BasicLayout,
        meta: {
            requiresAuth: true
        },
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
            path: '/test',
            name: 'test',
            component: Test
        }]
})

// router.beforeEach((to, from, next) => {
//     const authStore = useAuthStore()
//     const user = authStore.user;
//     if (to.meta.requiresAdmin && user?.role !== 'admin') {
//         next('/admin/login')
//     }
//     else if (to.meta.requiresAuth && !user) {
//         next('/login')
//     } else {
//         next()
//     }
// })
export default router
