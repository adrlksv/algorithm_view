<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-black text-white p-6">
    <h1 class="text-4xl mb-6 neon-text">Вход</h1>
    <form @submit.prevent="handleLogin" class="w-full max-w-sm">
      <input v-model="email" type="email" placeholder="Email" class="neon-input mb-4" />
      <input v-model="password" type="password" placeholder="Пароль" class="neon-input mb-4" />
      <button type="submit" class="neon-button w-full">Войти</button>
    </form>
    <p class="mt-4">
      Нет аккаунта?
      <router-link to="/register" class="text-blue-400 hover:underline">Зарегистрироваться</router-link>
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

<style scoped>
.neon-text {
  text-shadow: 0 0 5px #0ff, 0 0 10px #0ff, 0 0 20px #0ff;
}

.neon-input {
  width: 100%;
  padding: 0.5rem;
  border-radius: 0.5rem;
  background: #111;
  color: #0ff;
  border: 1px solid #0ff;
  outline: none;
  box-shadow: 0 0 5px #0ff;
}

.neon-input::placeholder {
  color: #066;
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
</style>
