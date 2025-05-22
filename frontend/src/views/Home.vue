<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <h1 class="text-4xl mb-6">Добро пожаловать, {{ authStore.user?.username }}!</h1>
    <div class="flex gap-4">
      <button @click="goToAES" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        Перейти к AES
      </button>
      <button @click="handleLogout" class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">
        Выйти
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';

const router = useRouter();
const authStore = useAuthStore();

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};

const goToAES = () => {
  router.push('/aes');
};
</script>
