// src/stores/authStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import request from "../utils/request.js";
import axios from "axios";

export const useAuthStore = defineStore('auth', () => {
    const user = ref(111);

    // 登录方法
    async function login(username, password) {
        try {
            // 发送登录请求到 Flask 后端
            const response = await axios.post('http://localhost:5000/auth/login', {
                username,
                password,
            }, {
                headers: {
                    'Content-Type': 'application/json', // 确保请求头正确
                },
            });

            // 假设后端返回的数据格式为 { success: true, user: { username: 'admin' } }
            if (response.data.success) {
                user.value = response.data.user; // 存储用户信息
                // console.log(1, response.data.user)
                // console.log(2, user.value);
                //location.href="/"
                return true; // 登录成功
            } else {
                return true;
            }
        } catch (error) {
            console.error('登录失败:', error.message);
            throw error; // 抛出错误，方便调用方处理
        }
    }

    //管理员登录方法
    async function adminLogin(username, password) {
    }
    //注册方法
    async function register(username, password) {
        try {
            const response = await axios.post('http://localhost:5000/auth/register', {
                username,
                password
            }, {
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            if (response.data.success) {
                return true;
            }
        }catch (error) {
            console.error('注册失败:', error.message);
            throw error; // 抛出错误，方便调用方处理
        }
    }

    // 登出方法
    function logout() {
        user.value = null;
    }

    return {
        user,
        login,
        logout,
        register,
        adminLogin
    };
}, {
    persist: true,
});
