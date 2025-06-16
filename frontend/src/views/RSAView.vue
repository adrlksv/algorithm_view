<template>
  <div class="min-h-screen bg-gray-900 text-gray-100 p-6">
    <button
      @click="goHome"
      class="absolute top-6 right-6 px-4 py-2 rounded-lg font-medium bg-green-700 hover:bg-green-600 text-white transition-colors focus:outline-none focus:ring-2 focus:ring-green-500"
    >
      На главную
    </button>

    <div class="container mx-auto">
      <div class="flex flex-col lg:flex-row gap-8 transition-all duration-500" :class="{'lg:items-start': showVisualization}">
        <div 
          class="w-full transition-all duration-500 mx-auto"
          :class="{
            'lg:w-1/2': showVisualization,
            'max-w-2xl': !showVisualization
          }"
        >
          <div class="text-center mb-10">
            <h1 class="text-4xl md:text-5xl font-bold mb-4 text-green-400">RSA Алгоритм</h1>
            <p class="text-lg text-green-300">Генерация асимметричных ключей</p>
          </div>

          <button
            @click="showIntroduction = true"
            class="w-full mb-6 py-3 px-6 rounded-lg font-medium bg-blue-700 hover:bg-blue-600 text-white transition-all"
          >
            Что такое RSA?
          </button>

          <div v-if="showIntroduction" class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center p-4 z-50">
            <div class="bg-gray-800 rounded-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto p-6 relative">
              <button @click="showIntroduction = false" class="absolute top-4 right-4 p-2 rounded-full bg-gray-700 hover:bg-gray-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
              <RSAIntroduction />
            </div>
          </div>

          <form @submit.prevent="handleGenerate" class="mb-8 p-6 rounded-xl bg-gray-800 border border-gray-700 shadow-md transition-all">
            <div class="mb-4">
              <label for="keySize" class="block mb-2 font-medium text-gray-300">Размер ключа (бит):</label>
              <select
                id="keySize"
                v-model.number="keySize"
                class="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-900 text-gray-300 transition-all"
                required
                :disabled="isGenerating"
              >
                <option value="1024">1024 бит</option>
                <option value="2048">2048 бит</option>
                <option value="4096">4096 бит</option>
              </select>
            </div>

            <button
              type="submit"
              :disabled="isGenerating"
              class="w-full py-3 px-6 rounded-lg font-medium text-lg bg-green-700 hover:bg-green-600 text-white transition-all disabled:opacity-50"
            >
              <span v-if="isGenerating" class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Генерация...
              </span>
              <span v-else>Сгенерировать RSA ключи</span>
            </button>
          </form>

          <div v-if="rsaStore.privateKey" class="p-6 rounded-xl bg-gray-800 border border-gray-700 shadow-md transition-all">
            <h2 class="text-2xl font-bold mb-4 pb-2 border-b border-gray-700 text-green-400">Результаты</h2>
            
            <div class="space-y-4 mb-6">
              <div>
                <h3 class="font-semibold mb-1 text-gray-300">Приватный ключ:</h3>
                <div class="p-3 rounded-lg bg-gray-700 text-green-300 overflow-x-auto text-sm font-mono whitespace-pre-line">
                  {{ rsaStore.privateKey }}
                </div>
              </div>
              <div>
                <h3 class="font-semibold mb-1 text-gray-300">Публичный ключ:</h3>
                <div class="p-3 rounded-lg bg-gray-700 text-green-300 overflow-x-auto text-sm font-mono whitespace-pre-line">
                  {{ rsaStore.publicKey }}
                </div>
              </div>
            </div>

            <button
              v-if="!showVisualization"
              @click="showVisualization = true"
              class="w-full py-3 px-6 rounded-lg font-medium bg-purple-700 hover:bg-purple-600 text-white transition-all"
            >
              Показать визуализацию
            </button>

            <div v-if="showVisualization" class="space-y-4 mt-4">
              <div>
                <label class="block mb-2 font-medium text-gray-300">Скорость анимации:</label>
                <div class="flex items-center gap-4">
                  <input
                    type="range"
                    v-model.number="animationSpeed"
                    min="100"
                    max="3000"
                    step="100"
                    class="flex-1 h-2 rounded-lg bg-gray-700 appearance-none cursor-pointer accent-green-500"
                  />
                  <span class="text-sm text-gray-400 w-16 text-center">{{ animationSpeed }}ms</span>
                </div>
              </div>
              <button
                @click="showVisualization = false"
                class="w-full py-3 px-6 rounded-lg font-medium bg-gray-700 hover:bg-gray-600 text-gray-300 transition-all"
              >
                Скрыть визуализацию
              </button>
            </div>
          </div>
        </div>

        <transition name="visualization">
          <div 
            v-if="showVisualization && visualizationSteps.length"
            class="w-full lg:w-1/2 transition-all duration-500 space-y-6"
          >
            <RSAVisualizer 
              :steps="visualizationSteps"
              :animation-speed="animationSpeed"
              @step-changed="onStepChanged"
            />
            <RSAExplanationPanel 
              :step-name="currentStepName" 
              :key-size="keySize"
            />
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import RSAVisualizer from '../components/RSAVisualizer.vue';
import { useRSAStore } from '../store/rsa';
import { RSAVisualizer as RsaViz } from '../utils/rsa_visualization';
import RSAIntroduction from '../components/RSAIntroduction.vue';
import RSAExplanationPanel from '../components/RSAExplanationPanel.vue';

const rsaStore = useRSAStore();
const router = useRouter();

const keySize = ref(2048);
const showVisualization = ref(false);
const showIntroduction = ref(false);
const animationSpeed = ref(1000);
const visualizationSteps = ref([]);
const isGenerating = ref(false);
const currentStepName = ref('');

const handleGenerate = async () => {
  try {
    isGenerating.value = true;
    showVisualization.value = false;
    visualizationSteps.value = [];
    currentStepName.value = '';
    
    const success = await rsaStore.generateKeys(keySize.value);
    
    if (success) {
      const viz = new RsaViz(keySize.value);
      visualizationSteps.value = await viz.visualize();
    }
  } catch (error) {
    console.error('Ошибка генерации:', error);
  } finally {
    isGenerating.value = false;
  }
};

const onStepChanged = (index) => {
  if (visualizationSteps.value[index]) {
    currentStepName.value = visualizationSteps.value[index].title;
  }
};

watch(() => rsaStore.privateKey, () => {
  showVisualization.value = false;
});

const goHome = () => {
  router.push('/');
};
</script>

<style scoped>
.visualization-enter-active,
.visualization-leave-active {
  transition: all 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}
.visualization-enter-from,
.visualization-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>