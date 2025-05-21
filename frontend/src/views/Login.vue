<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <h1 class="text-4xl mb-6">Вход</h1>
    <form @submit.prevent="handleLogin" class="w-full max-w-sm">
      <input v-model="email" type="email" placeholder="Email" class="w-full mb-4 p-2 rounded" />
      <input v-model="password" type="password" placeholder="Пароль" class="w-full mb-4 p-2 rounded" />
      <button type="submit" class="w-full">Войти</button>
    </form>
    <p class="mt-4">
      Нет аккаунта?
      <router-link to="/register">Зарегистрироваться</router-link>
    </p>
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
    alert('Ошибка входа');
  }
};
</script>
