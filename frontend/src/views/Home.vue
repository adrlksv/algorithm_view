<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-black text-white p-6">
    <h1 class="text-4xl mb-6 neon-text">Добро пожаловать, {{ authStore.user?.username }}!</h1>
    <div class="flex gap-4">
      <button @click="goToAES" class="neon-button">Перейти к AES</button>
      <button @click="handleLogout" class="neon-button-red">Выйти</button>
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

<style scoped>
.neon-text {
  text-shadow: 0 0 5px #0ff, 0 0 10px #0ff, 0 0 20px #0ff;
}

.neon-button {
  background: transparent;
  border: 2px solid #0ff;
  color: #0ff;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
  text-shadow: 0 0 10px #0ff;
}

.neon-button:hover {
  background-color: #0ff;
  color: black;
  box-shadow: 0 0 15px #0ff;
}

.neon-button-red {
  background: transparent;
  border: 2px solid #f00;
  color: #f00;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
  text-shadow: 0 0 10px #f00;
}

.neon-button-red:hover {
  background-color: #f00;
  color: black;
  box-shadow: 0 0 15px #f00;
}
</style>
