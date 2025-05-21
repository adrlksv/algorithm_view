<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <h1 class="text-4xl mb-6">Регистрация</h1>
    <form @submit.prevent="handleRegister" class="w-full max-w-sm">
      <input v-model="username" type="text" placeholder="Имя пользователя" class="w-full mb-4 p-2 rounded" />
      <input v-model="email" type="email" placeholder="Email" class="w-full mb-4 p-2 rounded" />
      <input v-model="password" type="password" placeholder="Пароль" class="w-full mb-4 p-2 rounded" />
      <button type="submit" class="w-full">Зарегистрироваться</button>
    </form>
    <p class="mt-4">
      Уже есть аккаунт?
      <router-link to="/login">Войти</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';

const username = ref('');
const email = ref('');
const password = ref('');
const router = useRouter();
const authStore = useAuthStore();

const handleRegister = async () => {
  try {
    await authStore.register(username.value, email.value, password.value);
    router.push('/login');
  } catch (error) {
    alert('Ошибка регистрации');
  }
};
</script>
