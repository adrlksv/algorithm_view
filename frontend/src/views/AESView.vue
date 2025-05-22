<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-black text-white p-6">
    <h1 class="text-4xl mb-6 neon-text">AES Алгоритм</h1>

    <button
      @click="goHome"
      class="absolute top-6 right-6 neon-button"
    >
      На главную
    </button>

    <form @submit.prevent="onGenerate" class="mb-6 w-full max-w-md">
      <div class="mb-4">
        <label for="keySize" class="block mb-1">Размер ключа (бит):</label>
        <input
          id="keySize"
          type="number"
          v-model.number="keySize"
          placeholder="Введите 128, 192 или 256"
          min="128"
          max="256"
          step="64"
          required
          class="w-full px-3 py-2 rounded bg-[#111] text-green-400 placeholder-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
        />
      </div>

      <div class="mb-4">
        <label for="sampleText" class="block mb-1">Текст для шифрования:</label>
        <input
          id="sampleText"
          type="text"
          v-model="sampleText"
          placeholder="Введите текст для шифрования"
          required
          class="w-full px-3 py-2 rounded bg-[#111] text-green-400 placeholder-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
        />
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="bg-green-600 hover:bg-green-800 text-white px-4 py-2 rounded w-full transition duration-300"
      >
        {{ loading ? 'Генерация...' : 'Сгенерировать AES ключ' }}
      </button>
    </form>

    <AESVisualizer v-if="steps.length" :steps="steps" />

    <div v-if="loading" class="mt-4 text-sm text-gray-400">Генерация...</div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import AESVisualizer from '../components/AESVisualizer.vue';
import { useAESStore } from '../store/aes';
import { storeToRefs } from 'pinia';

const aes = useAESStore();
const { steps, loading } = storeToRefs(aes);

const keySize = ref(256);
const sampleText = ref("Test message");

const router = useRouter();

const onGenerate = async () => {
  await aes.generateAES(keySize.value, sampleText.value);
};

const goHome = () => {
  router.push('/');
}
</script>

<style scoped>
.neon-text {
  text-shadow: 0 0 5px #0f0, 0 0 10px #0f0, 0 0 20px #0f0;
}

.neon-button {
  background-color: transparent;
  border: 2px solid #7f00ff; /* фиолетовый */
  color: #7f00ff;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  text-shadow:
    0 0 5px #7f00ff,
    0 0 10px #7f00ff,
    0 0 20px #7f00ff,
    0 0 40px #a64dff;
  transition: all 0.3s ease;
  user-select: none;
}

.neon-button:hover {
  background-color: #7f00ff;
  color: #fff;
  box-shadow:
    0 0 10px #a64dff,
    0 0 20px #a64dff,
    0 0 30px #d18aff;
  text-shadow: none;
}

</style>
