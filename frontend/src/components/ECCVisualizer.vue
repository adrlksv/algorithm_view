<template>
  <div class="p-6 rounded-xl shadow-lg bg-gray-900 border border-gray-700 transition-all duration-300">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
      <div>
        <h2 class="text-2xl font-bold text-green-400">Генерация ECC ключей</h2>
        <div class="text-sm text-green-300 opacity-80">
          Шаг {{ currentStepIndex + 1 }} из {{ steps.length }}
        </div>
      </div>
      
      <div class="flex gap-2">
        <button @click="prevStep" :disabled="currentStepIndex === 0" class="p-2 rounded-md bg-gray-700 text-green-400 hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <button @click="nextStep" :disabled="currentStepIndex >= steps.length - 1" class="p-2 rounded-md bg-gray-700 text-green-400 hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <button @click="playPause" class="p-2 rounded-md bg-gray-700 text-green-400 hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path v-if="isPlaying" fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
            <path v-else fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Визуализация эллиптической кривой -->
    <div class="mb-6 h-64 bg-gray-800 rounded-lg flex items-center justify-center">
      <canvas ref="curveCanvas" class="w-full h-full"></canvas>
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
        <div class="h-full transition-all duration-300 bg-green-500" 
             :style="{ width: `${(currentStepIndex + 1) / steps.length * 100}%` }"></div>
      </div>
    </div>

    <!-- Описание шага -->
    <div class="space-y-4">
      <transition name="fade-slide" mode="out-in">
        <div :key="`step-${currentStepIndex}`"
             class="p-4 rounded-lg bg-gray-800 border border-gray-700 transition-all duration-300">
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
import { ref, computed, watch, onUnmounted, onMounted } from 'vue';

const props = defineProps({
  steps: {
    type: Array,
    required: true
  },
  animationSpeed: {
    type: Number,
    default: 1000
  },
  curveParams: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['step-changed']);

const currentStepIndex = ref(0);
const isPlaying = ref(false);
let playInterval = null;
const curveCanvas = ref(null);

const currentStep = computed(() => props.steps[currentStepIndex.value] || {});
const currentOperations = computed(() => currentStep.value.operations || []);

const nextStep = () => {
  if (currentStepIndex.value < props.steps.length - 1) {
    currentStepIndex.value++;
    emit('step-changed', currentStepIndex.value);
    drawCurve();
  }
};

const prevStep = () => {
  if (currentStepIndex.value > 0) {
    currentStepIndex.value--;
    emit('step-changed', currentStepIndex.value);
    drawCurve();
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

const drawCurve = () => {
  const canvas = curveCanvas.value;
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  
  ctx.clearRect(0, 0, width, height);
  
  // Настройка стилей
  ctx.strokeStyle = '#4ade80';
  ctx.fillStyle = '#4ade80';
  ctx.lineWidth = 2;
  
  // Масштабирование для отображения кривой
  const scale = 30;
  const centerX = width / 2;
  const centerY = height / 2;
  
  // Рисование сетки
  ctx.strokeStyle = '#374151';
  ctx.lineWidth = 1;
  for (let x = 0; x <= width; x += scale) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
    ctx.stroke();
  }
  for (let y = 0; y <= height; y += scale) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
    ctx.stroke();
  }
  
  // Рисование осей
  ctx.strokeStyle = '#6b7280';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, centerY);
  ctx.lineTo(width, centerY);
  ctx.moveTo(centerX, 0);
  ctx.lineTo(centerX, height);
  ctx.stroke();
  
  // Рисование кривой
  ctx.strokeStyle = '#4ade80';
  ctx.lineWidth = 2;
  ctx.beginPath();
  
  const a = props.curveParams.a;
  const b = props.curveParams.b;
  
  // Упрощенное рисование кривой (для демонстрации)
  for (let x = -10; x <= 10; x += 0.1) {
    const xNorm = x;
    const ySquared = Math.pow(xNorm, 3) + a * xNorm + b;
    
    if (ySquared >= 0) {
      const y = Math.sqrt(ySquared);
      const canvasX = centerX + xNorm * scale;
      const canvasY = centerY - y * scale;
      
      if (x === -10) ctx.moveTo(canvasX, canvasY);
      else ctx.lineTo(canvasX, canvasY);
      
      // Симметричная часть (отрицательный y)
      const canvasY2 = centerY + y * scale;
      if (x === -10) ctx.moveTo(canvasX, canvasY2);
      else ctx.lineTo(canvasX, canvasY2);
    }
  }
  
  ctx.stroke();
  
  // Рисование точек для текущего шага
  if (currentStep.value.points) {
    currentStep.value.points.forEach(point => {
      const canvasX = centerX + point.x * scale;
      const canvasY = centerY - point.y * scale;
      
      ctx.fillStyle = point.color || '#f87171';
      ctx.beginPath();
      ctx.arc(canvasX, canvasY, 6, 0, Math.PI * 2);
      ctx.fill();
      
      if (point.label) {
        ctx.fillStyle = '#e2e8f0';
        ctx.font = '12px Arial';
        ctx.fillText(point.label, canvasX + 10, canvasY + 5);
      }
    });
  }
  
  // Рисование операций (сложение/удвоение точек)
  drawOperation(ctx, centerX, centerY, scale);
};

const drawOperation = (ctx, centerX, centerY, scale) => {
  if (!currentStep.value.operation) return;
  
  switch (currentStep.value.operation) {
    case 'add':
      if (currentStep.value.points?.length >= 2) {
        const p1 = currentStep.value.points[0];
        const p2 = currentStep.value.points[1];
        
        ctx.strokeStyle = '#93c5fd';
        ctx.setLineDash([5, 3]);
        ctx.beginPath();
        ctx.moveTo(centerX + p1.x * scale, centerY - p1.y * scale);
        ctx.lineTo(centerX + p2.x * scale, centerY - p2.y * scale);
        ctx.stroke();
        ctx.setLineDash([]);
      }
      break;
      
    case 'double':
      if (currentStep.value.points?.length >= 1) {
        const p = currentStep.value.points[0];
        
        // Рисование касательной
        ctx.strokeStyle = '#f59e0b';
        ctx.setLineDash([5, 3]);
        ctx.beginPath();
        
        // Упрощенная касательная для демонстрации
        const slope = (3 * Math.pow(p.x, 2)) / (2 * p.y);
        const yIntercept = p.y - slope * p.x;
        
        const x1 = p.x - 2;
        const y1 = slope * x1 + yIntercept;
        const x2 = p.x + 2;
        const y2 = slope * x2 + yIntercept;
        
        ctx.moveTo(centerX + x1 * scale, centerY - y1 * scale);
        ctx.lineTo(centerX + x2 * scale, centerY - y2 * scale);
        ctx.stroke();
        ctx.setLineDash([]);
      }
      break;
  }
};

onMounted(() => {
  if (curveCanvas.value) {
    curveCanvas.value.width = curveCanvas.value.offsetWidth;
    curveCanvas.value.height = curveCanvas.value.offsetHeight;
    drawCurve();
  }
});

watch(() => props.steps, (newSteps) => {
  if (newSteps.length) {
    currentStepIndex.value = 0;
    drawCurve();
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