<template>
  <div class="p-6 rounded-xl shadow-lg bg-gray-900 border border-gray-700 transition-all duration-300">
    <!-- Заголовок и управление -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <div>
        <h2 class="text-2xl font-bold text-green-400">Генерация RSA ключей</h2>
        <div class="text-sm text-green-300 opacity-80">
          Шаг {{ currentStepIndex + 1 }} из {{ steps.length }}
        </div>
      </div>
      
      <div class="flex gap-2">
        <button 
          @click="prevStep" 
          :disabled="currentStepIndex === 0"
          class="p-2 rounded-md bg-gray-700 text-green-400 hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <button 
          @click="nextStep" 
          :disabled="currentStepIndex >= steps.length - 1"
          class="p-2 rounded-md bg-gray-700 text-green-400 hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <button 
          @click="playPause"
          class="p-2 rounded-md bg-gray-700 text-green-400 hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 transition-all"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path v-if="isPlaying" fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
            <path v-else fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Математические операции -->
    <div class="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="(op, idx) in currentOperations" :key="idx"
           class="p-4 rounded-lg bg-gray-800 border border-gray-700">
        <h3 class="text-green-400 font-mono mb-2">{{ op.title }}</h3>
        <div class="text-gray-300 font-mono text-sm whitespace-pre-wrap">{{ op.value }}</div>
      </div>
    </div>

    <!-- Прогресс -->
    <div class="mb-6">
      <div class="flex justify-between text-sm text-green-300 mb-1">
        <span>Прогресс</span>
        <span>{{ Math.round((currentStepIndex + 1) / steps.length * 100) }}%</span>
      </div>
      <div class="h-2 rounded-full overflow-hidden bg-gray-700">
        <div 
          class="h-full transition-all duration-300 bg-green-500" 
          :style="{ width: `${(currentStepIndex + 1) / steps.length * 100}%` }"
        ></div>
      </div>
    </div>

    <!-- Описание шага -->
    <div class="space-y-4">
      <transition name="fade-slide" mode="out-in">
        <div
          :key="`step-${currentStepIndex}`"
          class="p-4 rounded-lg bg-gray-800 border border-gray-700 transition-all duration-300"
        >
          <h2 class="text-lg font-bold mb-2 text-green-400">
            {{ currentStep.title }}
          </h2>
          
          <div class="grid grid-cols-1 gap-4">
            <div>
              <p class="mb-3 text-gray-300 whitespace-pre-line">{{ currentStep.content }}</p>
              <div v-if="currentStep.details" class="text-sm text-gray-400 whitespace-pre-line">
                {{ currentStep.details }}
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue';

const props = defineProps({
  steps: {
    type: Array,
    required: true
  },
  animationSpeed: {
    type: Number,
    default: 1000
  }
});

const emit = defineEmits(['step-changed']);

const currentStepIndex = ref(0);
const isPlaying = ref(false);
let playInterval = null;

const currentStep = computed(() => props.steps[currentStepIndex.value] || {});
const currentOperations = computed(() => currentStep.value.operations || []);

const nextStep = () => {
  if (currentStepIndex.value < props.steps.length - 1) {
    currentStepIndex.value++;
    emit('step-changed', currentStepIndex.value);
  }
};

const prevStep = () => {
  if (currentStepIndex.value > 0) {
    currentStepIndex.value--;
    emit('step-changed', currentStepIndex.value);
  }
};

const playPause = () => {
  isPlaying.value = !isPlaying.value;
  
  if (isPlaying.value) {
    playInterval = setInterval(() => {
      if (currentStepIndex.value >= props.steps.length - 1) {
        isPlaying.value = false;
        clearInterval(playInterval);
      } else {
        nextStep();
      }
    }, props.animationSpeed);
  } else {
    clearInterval(playInterval);
  }
};

watch(() => props.steps, (newSteps) => {
  if (newSteps.length) {
    currentStepIndex.value = 0;
  }
}, { immediate: true });

watch(() => props.animationSpeed, () => {
  if (playInterval) {
    clearInterval(playInterval);
    if (isPlaying.value) {
      playPause();
      playPause();
    }
  }
});

onUnmounted(() => {
  clearInterval(playInterval);
});
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>