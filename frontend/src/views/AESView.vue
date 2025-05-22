<template>
  <div class="min-h-screen flex items-center justify-center bg-black text-white p-6 relative">
    <!-- Кнопка "На главную" -->
    <button
      @click="goHome"
      class="absolute top-6 right-6 neon-button"
    >
      На главную
    </button>

    <!-- Основной контент -->
    <div class="w-full max-w-3xl transition-all duration-500" :class="{'translate-x-[-100px]': showVisualization}">
      <div class="text-center mb-10">
        <h1 class="text-6xl neon-text mb-4">AES Алгоритм</h1>
        <p class="text-green-300">Визуализация процесса шифрования</p>
      </div>

      <form @submit.prevent="onGenerate" class="mb-8 p-6 bg-[#0f0f0f] rounded-lg border border-green-900/50">
        <div class="mb-4">
          <label for="keySize" class="block mb-2 text-green-300">Размер ключа (бит):</label>
          <input
            id="keySize"
            type="number"
            v-model.number="keySize"
            placeholder="128, 192 или 256"
            min="128"
            max="256"
            step="64"
            required
            class="w-full px-4 py-3 rounded bg-[#111] text-green-400 placeholder-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 border border-green-900/50"
          />
        </div>

        <div class="mb-6">
          <label for="sampleText" class="block mb-2 text-green-300">Текст для шифрования:</label>
          <input
            id="sampleText"
            type="text"
            v-model="sampleText"
            placeholder="Введите текст для шифрования"
            required
            class="w-full px-4 py-3 rounded bg-[#111] text-green-400 placeholder-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 border border-green-900/50"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg w-full transition duration-300 font-medium text-lg shadow-lg hover:shadow-green-800/50"
        >
          {{ loading ? 'Генерация...' : 'Сгенерировать AES ключ' }}
        </button>
      </form>

      <!-- Результаты -->
      <div v-if="realResults.key" class="p-6 bg-[#0f0f0f] rounded-lg border border-green-900/50">
        <h2 class="text-2xl font-bold mb-4 text-green-400 border-b border-green-900/50 pb-2">Результаты</h2>
        <div class="space-y-4 mb-6">
          <div>
            <h3 class="font-semibold text-green-300 mb-1">Ключ:</h3>
            <p class="break-all bg-[#1a1a1a] p-3 rounded font-mono text-sm">{{ realResults.key }}</p>
          </div>
          <div>
            <h3 class="font-semibold text-green-300 mb-1">IV:</h3>
            <p class="break-all bg-[#1a1a1a] p-3 rounded font-mono text-sm">{{ realResults.iv }}</p>
          </div>
          <div>
            <h3 class="font-semibold text-green-300 mb-1">Зашифрованный текст:</h3>
            <p class="break-all bg-[#1a1a1a] p-3 rounded font-mono text-sm">{{ realResults.encrypted }}</p>
          </div>
        </div>

        <!-- Управление визуализацией -->
        <button
          v-if="!showVisualization"
          @click="showVisualization = true"
          class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg w-full transition duration-300 font-medium text-lg shadow-lg hover:shadow-purple-800/50"
        >
          Показать визуализацию
        </button>

        <div v-if="showVisualization" class="space-y-4">
          <div>
            <label class="block text-green-300 mb-2">Скорость анимации:</label>
            <input
              type="range"
              v-model.number="animationSpeed"
              min="100"
              max="3000"
              step="100"
              class="w-full h-2 bg-green-900 rounded-lg appearance-none cursor-pointer"
            >
            <div class="flex justify-between text-xs text-green-400 mt-1">
              <span>Медленно</span>
              <span>Быстро</span>
            </div>
          </div>
          <button
            @click="showVisualization = false"
            class="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-lg w-full transition duration-300 font-medium text-lg"
          >
            Скрыть визуализацию
          </button>
        </div>
      </div>
    </div>

    <!-- Панель визуализации -->
    <transition name="slide">
      <div 
        v-if="showVisualization && visualizationSteps.length"
        class="fixed top-0 right-0 h-full w-[450px] bg-[#0a0a0a] border-l border-green-900/50 overflow-y-auto p-6 shadow-2xl"
      >
        <AESVisualizer 
          :steps="visualizationSteps"
          :animation-speed="animationSpeed"
        />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import AESVisualizer from '../components/AESVisualizer.vue';
import { useAESStore } from '../store/aes';
import { storeToRefs } from 'pinia';
import { AESVisualizer as AesViz } from '../utils/aes_visualization';

const aes = useAESStore();
const { steps, loading } = storeToRefs(aes);

const keySize = ref(256);
const sampleText = ref("Test message");
const realResults = ref({});
const visualizationSteps = ref([]);
const showVisualization = ref(false);
const animationSpeed = ref(1000);

const router = useRouter();

const onGenerate = async () => {
  realResults.value = {};
  visualizationSteps.value = [];
  showVisualization.value = false;
  
  try {
    await aes.generateAES(keySize.value, sampleText.value);
    realResults.value = {
      key: aes.key,
      iv: aes.iv,
      encrypted: aes.encrypted
    };
    
    const viz = new AesViz(keySize.value, sampleText.value);
    visualizationSteps.value = await viz.visualize();
  } catch (error) {
    console.error('Ошибка при генерации AES:', error);
  }
};

const goHome = () => {
  router.push('/');
};
</script>

<style scoped>
.neon-text {
  text-shadow: 0 0 5px #0f0, 0 0 10px #0f0, 0 0 20px #0f0;
  font-weight: 700;
  letter-spacing: 1px;
}

.neon-button {
  background-color: transparent;
  border: 2px solid #7f00ff;
  color: #7f00ff;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  text-shadow:
    0 0 5px #7f00ff,
    0 0 10px #7f00ff,
    0 0 20px #7f00ff,
    0 0 40px #a64dff;
  transition: all 0.3s ease;
}

.neon-button:hover {
  background-color: #7f00ff;
  color: #fff;
  box-shadow:
    0 0 10px #a64dff,
    0 0 20px #a64dff,
    0 0 30px #d18aff;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  background: #7f00ff;
  cursor: pointer;
  border-radius: 50%;
  box-shadow: 0 0 5px #a64dff;
  transition: all 0.2s ease;
}

input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}
</style>