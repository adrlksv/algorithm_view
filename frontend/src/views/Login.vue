<template>
  <div class="min-h-screen bg-gray-900 text-gray-100 p-6 flex flex-col items-center justify-center">
    <div class="w-full max-w-md">
      <h1 class="text-4xl md:text-5xl font-bold mb-8 text-center text-green-400">Вход</h1>
      
      <form @submit.prevent="handleLogin" class="mb-6 p-6 rounded-xl bg-gray-800 border border-gray-700 shadow-md">
        <div class="mb-4">
          <label for="email" class="block mb-2 font-medium text-gray-300">Email:</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Введите email"
            class="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-900 text-gray-300 transition-all"
            required
          />
        </div>
        
        <div class="mb-6">
          <label for="password" class="block mb-2 font-medium text-gray-300">Пароль:</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Введите пароль"
            class="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-900 text-gray-300 transition-all"
            required
          />
        </div>
        
        <button
          type="submit"
          class="w-full py-3 px-6 rounded-lg font-medium text-lg bg-green-700 hover:bg-green-600 text-white transition-all"
        >
          Войти
        </button>
      </form>
      
      <p class="text-center text-gray-400">
        Нет аккаунта? 
        <router-link to="/register" class="text-green-400 hover:underline">Зарегистрироваться</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';

const email = ref('');
const password = ref('');
const router = useRouter();
const authStore = useAuthStore();

const handleLogin = async () => {
  try {
    await authStore.login(email.value, password.value);
    router.push('/');
  } catch (error) {
    alert('Ошибка входа: ' + (error.response?.data?.message || error.message));
  }
};
</script>