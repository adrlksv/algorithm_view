<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-black text-white p-6">
    <h1 class="text-4xl mb-6 neon-text">AES Алгоритм</h1>
    <button 
      @click="generateAES"
      class="bg-green-600 hover:bg-green-800 text-white px-4 py-2 rounded mb-6 transition duration-300"
    >
      Сгенерировать AES ключ
    </button>

    <AESVisualizer v-if="steps.length" :steps="steps" />

    <div v-if="loading" class="mt-4 text-sm text-gray-400">Генерация...</div>
  </div>
</template>

<script setup>
import { useAESStore } from '../store/aes';
import { storeToRefs } from 'pinia';
import AESVisualizer from '../components/AESVisualizer.vue';

const aes = useAESStore();
const { generateAES } = aes;
const { steps, loading } = storeToRefs(aes);
</script>

<style scoped>
.neon-text {
  text-shadow: 0 0 5px #0f0, 0 0 10px #0f0, 0 0 20px #0f0;
}
</style>
