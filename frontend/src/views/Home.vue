<template>
  <div class="min-h-screen bg-gray-900 text-gray-100 p-6 flex flex-col items-center justify-center">
    <div class="w-full max-w-md text-center">
      <h1 class="text-4xl md:text-5xl font-bold mb-6 text-green-400">Добро пожаловать, {{ authStore.user?.username }}!</h1>
      
      <div class="flex flex-col gap-4 justify-center">
        <button 
          @click="goToAES" 
          class="px-6 py-3 rounded-lg font-medium bg-green-700 hover:bg-green-600 text-white transition-colors focus:outline-none focus:ring-2 focus:ring-green-500"
        >
          Перейти к AES
        </button>
        
        <button 
          @click="goToRSA"
          class="px-6 py-3 rounded-lg font-medium bg-blue-700 hover:bg-blue-600 text-white transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Перейти к RSA
        </button>
        
        <button 
          @click="handleLogout"
          class="px-6 py-3 rounded-lg font-medium bg-gray-700 hover:bg-gray-600 text-gray-300 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500"
        >
          Выйти
        </button>
      </div>
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

const goToRSA = () => {
  router.push('/rsa');
};
</script>