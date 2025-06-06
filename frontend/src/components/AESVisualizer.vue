<template>
  <div class="p-6 rounded-xl shadow-lg bg-gray-900 border border-gray-700 transition-all duration-300">
    <!-- Заголовок и управление -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <div>
        <h2 class="text-2xl font-bold text-green-400">Состояние шифрования AES</h2>
        <div class="text-sm text-green-300 opacity-80">
          Раунд: {{ currentRound }}/{{ totalRounds }}
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

    <!-- Визуализация блока -->
    <div class="mb-8">
      <div class="grid grid-cols-4 gap-3 mb-4 justify-center">
        <transition-group name="cell" tag="div" class="contents">
          <div
            v-for="(byte, idx) in currentState"
            :key="`${idx}-${byte}-${stepKey}`"
            class="w-14 h-14 flex items-center justify-center rounded font-mono text-sm border border-gray-700 text-green-400 transition-all duration-300 relative"
            :class="{
              'transform scale-110 bg-green-900 border-green-500 text-green-300 shadow-lg shadow-green-900/30': highlightedBytes.includes(idx)
            }"
          >
            {{ byte }}
            <div class="absolute bottom-1 text-xs text-gray-500">
              {{ getBytePosition(idx) }}
            </div>
          </div>
        </transition-group>
      </div>
      
      <div class="text-center text-sm text-gray-500 mb-2">
        State Matrix ({{ currentState.length }} bytes)
      </div>
    </div>

    <!-- Прогресс шагов -->
    <div class="mb-6">
      <div class="flex justify-between text-sm text-green-300 mb-1">
        <span>Прогресс</span>
        <span>Шаг {{ currentStepIndex + 1 }}/{{ steps.length }}</span>
      </div>
      <div class="h-2 rounded-full overflow-hidden bg-gray-700">
        <div 
          class="h-full transition-all duration-300 bg-green-500" 
          :style="{ width: `${(currentStepIndex + 1) / steps.length * 100}%` }"
        ></div>
      </div>
    </div>

    <!-- Шаги описания -->
    <div class="space-y-4">
      <transition name="fade-slide" mode="out-in">
        <div
          :key="`step-${currentStepIndex}`"
          class="p-4 rounded-lg bg-gray-800 border border-gray-700 transition-all duration-300"
        >
          <h2 class="text-lg font-bold mb-2 flex items-center gap-2 text-green-400">
            <span>{{ currentStep.title }}</span>
            <span v-if="currentStep.round" class="text-xs px-2 py-1 rounded bg-green-700 text-green-100">
              Раунд {{ currentStep.round }}
            </span>
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p class="mb-3 text-gray-300">{{ currentStep.content }}</p>
              <div v-if="currentStep.details" class="text-sm text-gray-400">
                {{ currentStep.details }}
              </div>
            </div>
            
            <div v-if="currentStep.extra" class="p-3 rounded text-sm font-mono overflow-x-auto bg-gray-700 border border-gray-600 text-green-300">
              {{ currentStep.extra }}
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
  steps: Array,
  animationSpeed: {
    type: Number,
    default: 1000
  }
});

const emit = defineEmits(['step-changed']);

const currentStepIndex = ref(0);
const currentState = ref(Array(16).fill('00'));
const highlightedBytes = ref([]);
const stepKey = ref(0);
const isPlaying = ref(false);
let playInterval = null;

const currentStep = computed(() => props.steps[currentStepIndex.value] || {});
const totalRounds = computed(() => Math.max(...props.steps.map(s => s.round || 0), 0));
const currentRound = computed(() => currentStep.value.round || 0);

const getBytePosition = (idx) => {
  const row = Math.floor(idx / 4);
  const col = idx % 4;
  return `r${row}c${col}`;
};

const updateState = () => {
  const step = props.steps[currentStepIndex.value];
  if (step?.state) {
    // Вычисляем измененные байты для анимации
    if (currentStepIndex.value > 0) {
      const prevState = props.steps[currentStepIndex.value - 1].state || [];
      highlightedBytes.value = step.state
        .map((byte, i) => byte !== prevState[i] ? i : -1)
        .filter(i => i !== -1);
      
      setTimeout(() => highlightedBytes.value = [], props.animationSpeed * 0.7);
    }
    
    currentState.value = [...step.state];
    stepKey.value++;
  }
};

const nextStep = () => {
  if (currentStepIndex.value < props.steps.length - 1) {
    currentStepIndex.value++;
    updateState();
    emit('step-changed', currentStepIndex.value);
  }
};

const prevStep = () => {
  if (currentStepIndex.value > 0) {
    currentStepIndex.value--;
    updateState();
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
    updateState();
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
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.cell-enter-active,
.cell-leave-active {
  transition: all 0.5s ease;
}
.cell-enter-from {
  opacity: 0;
  transform: scale(0.8);
}
.cell-leave-to {
  opacity: 0;
  transform: scale(1.2);
}
</style>