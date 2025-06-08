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

    <!-- Визуализация эллиптической кривой с контролами масштабирования -->
    <div class="mb-6 bg-gray-800 rounded-lg relative overflow-hidden">
      <div class="absolute top-2 right-2 z-10 flex gap-2">
        <button @click="zoomIn" class="p-1 rounded bg-gray-700 hover:bg-gray-600 text-gray-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
        </button>
        <button @click="zoomOut" class="p-1 rounded bg-gray-700 hover:bg-gray-600 text-gray-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" clip-rule="evenodd" />
          </svg>
        </button>
        <button @click="resetZoom" class="p-1 rounded bg-gray-700 hover:bg-gray-600 text-gray-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
      
      <canvas 
        ref="curveCanvas" 
        class="w-full h-64 cursor-move"
        @mousedown="startDrag"
        @mousemove="onDrag"
        @mouseup="endDrag"
        @mouseleave="endDrag"
        @wheel.prevent="onWheel"
      ></canvas>
    </div>

    <!-- Математические операции -->
    <div class="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="(op, idx) in currentOperations" :key="idx"
           class="p-4 rounded-lg bg-gray-800 border border-gray-700">
        <h3 class="text-green-400 font-mono mb-2">{{ op.title }}</h3>
        <div class="text-gray-300 font-mono text-sm whitespace-pre-wrap">{{ op.value }}</div>
        <div v-if="op.description" class="mt-1 text-xs text-gray-500">{{ op.description }}</div>
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
                <p v-for="(detail, idx) in currentStep.details" :key="idx">{{ detail }}</p>
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

// Управление графиком
const scale = ref(30);
const offsetX = ref(0);
const offsetY = ref(0);
const isDragging = ref(false);
const lastX = ref(0);
const lastY = ref(0);

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

// Оптимизированные методы для работы с графиком
const drawCurve = () => {
  const canvas = curveCanvas.value;
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  
  // Очистка canvas с учетом прозрачности
  ctx.clearRect(0, 0, width, height);
  
  // Центр с учетом смещения
  const centerX = width / 2 + offsetX.value;
  const centerY = height / 2 + offsetY.value;
  
  // Адаптивный шаг сетки в зависимости от масштаба
  const gridStep = calculateGridStep();
  
  // Оптимизированное рисование сетки
  drawGrid(ctx, width, height, centerX, centerY, gridStep);
  
  // Рисование осей
  drawAxes(ctx, width, height, centerX, centerY);
  
  // Рисование кривой с учетом реальных параметров
  drawEllipticCurve(ctx, centerX, centerY);
  
  // Рисование точек и операций
  drawPointsAndOperations(ctx, centerX, centerY);
};

const calculateGridStep = () => {
  // Адаптивный шаг сетки (0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, ...)
  const steps = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100];
  const targetStep = 50 / scale.value; // Желаемое расстояние в пикселях
  return steps.reduce((prev, curr) => 
    Math.abs(curr - targetStep) < Math.abs(prev - targetStep) ? curr : prev
  );
};

const drawGrid = (ctx, width, height, centerX, centerY, gridStep) => {
  ctx.strokeStyle = '#374151';
  ctx.lineWidth = Math.min(1, 0.5 * Math.sqrt(scale.value / 30)); // Адаптивная толщина
  
  // Вертикальные линии
  const startX = Math.floor((-centerX / scale.value) / gridStep) * gridStep;
  const endX = Math.ceil((width - centerX) / scale.value / gridStep) * gridStep;
  
  for (let x = startX; x <= endX; x += gridStep) {
    const canvasX = centerX + x * scale.value;
    if (canvasX >= 0 && canvasX <= width) {
      ctx.beginPath();
      ctx.moveTo(canvasX, 0);
      ctx.lineTo(canvasX, height);
      ctx.stroke();
    }
  }
  
  // Горизонтальные линии
  const startY = Math.floor((-centerY / scale.value) / gridStep) * gridStep;
  const endY = Math.ceil((height - centerY) / scale.value / gridStep) * gridStep;
  
  for (let y = startY; y <= endY; y += gridStep) {
    const canvasY = centerY + y * scale.value;
    if (canvasY >= 0 && canvasY <= height) {
      ctx.beginPath();
      ctx.moveTo(0, canvasY);
      ctx.lineTo(width, canvasY);
      ctx.stroke();
    }
  }
};

const drawAxes = (ctx, width, height, centerX, centerY) => {
  ctx.strokeStyle = '#6b7280';
  ctx.lineWidth = Math.min(2, 1.5 * Math.sqrt(scale.value / 30)); // Адаптивная толщина
  
  // Ось X
  if (centerY >= 0 && centerY <= height) {
    ctx.beginPath();
    ctx.moveTo(0, centerY);
    ctx.lineTo(width, centerY);
    ctx.stroke();
  }
  
  // Ось Y
  if (centerX >= 0 && centerX <= width) {
    ctx.beginPath();
    ctx.moveTo(centerX, 0);
    ctx.lineTo(centerX, height);
    ctx.stroke();
  }
};

const drawEllipticCurve = (ctx, centerX, centerY) => {
  const { a, b, p } = props.curveParams;
  const isSimplified = p === 17; // Для демонстрационных целей
  
  ctx.strokeStyle = '#4ade80';
  ctx.lineWidth = Math.min(3, 2 * Math.sqrt(scale.value / 30)); // Адаптивная толщина
  ctx.beginPath();
  
  // Определяем область видимости
  const visibleWidth = curveCanvas.value.width / scale.value;
  const startX = -visibleWidth / 2;
  const endX = visibleWidth / 2;
  const step = Math.max(0.01, visibleWidth / 200); // Количество точек для расчета
  
  // Рисуем кривую
  let firstPoint = true;
  for (let x = startX; x <= endX; x += step) {
    const xVal = isSimplified ? x : (x % p + p) % p; // Для реальных кривых учитываем модуль
    const ySquared = isSimplified ? 
      Math.pow(xVal, 3) + a * xVal + b :
      (Math.pow(xVal, 3) + a * xVal + b) % p;
    
    if (ySquared >= 0) {
      const y = Math.sqrt(ySquared);
      const canvasX = centerX + x * scale.value;
      
      // Верхняя часть кривой
      const canvasYUpper = centerY - y * scale.value;
      if (firstPoint) {
        ctx.moveTo(canvasX, canvasYUpper);
        firstPoint = false;
      } else {
        ctx.lineTo(canvasX, canvasYUpper);
      }
      
      // Нижняя часть кривой
      const canvasYLower = centerY + y * scale.value;
      if (firstPoint) {
        ctx.moveTo(canvasX, canvasYLower);
        firstPoint = false;
      } else {
        ctx.lineTo(canvasX, canvasYLower);
      }
    }
  }
  
  ctx.stroke();
};

const drawPointsAndOperations = (ctx, centerX, centerY) => {
  if (!currentStep.value.points) return;
  
  // Рисуем точки
  currentStep.value.points.forEach(point => {
    if (!point.visible && point.visible !== undefined) return;
    
    const canvasX = centerX + point.x * scale.value;
    const canvasY = centerY - point.y * scale.value;
    
    // Проверяем, видна ли точка в текущем масштабе
    if (canvasX < 0 || canvasX > curveCanvas.value.width || 
        canvasY < 0 || canvasY > curveCanvas.value.height) {
      return;
    }
    
    ctx.fillStyle = point.color || '#f87171';
    ctx.beginPath();
    ctx.arc(canvasX, canvasY, 6 * Math.sqrt(scale.value / 30), 0, Math.PI * 2); // Адаптивный размер
    ctx.fill();
    
    if (point.label) {
      ctx.fillStyle = '#e2e8f0';
      ctx.font = `${12 * Math.sqrt(scale.value / 30)}px Arial`; // Адаптивный размер шрифта
      ctx.fillText(point.label, canvasX + 10, canvasY + 5);
    }
  });
  
  // Рисуем операции (сложение/удвоение)
  drawOperation(ctx, centerX, centerY);
};

const drawOperation = (ctx, centerX, centerY) => {
  if (!currentStep.value.operation) return;
  
  ctx.setLineDash([5, 3]);
  ctx.lineWidth = Math.min(2, 1.5 * Math.sqrt(scale.value / 30)); // Адаптивная толщина
  
  switch (currentStep.value.operation) {
    case 'add':
      if (currentStep.value.points?.length >= 2) {
        const p1 = currentStep.value.points[0];
        const p2 = currentStep.value.points[1];
        
        ctx.strokeStyle = '#93c5fd';
        ctx.beginPath();
        ctx.moveTo(centerX + p1.x * scale.value, centerY - p1.y * scale.value);
        ctx.lineTo(centerX + p2.x * scale.value, centerY - p2.y * scale.value);
        ctx.stroke();
      }
      break;
      
    case 'double':
      if (currentStep.value.points?.length >= 1) {
        const p = currentStep.value.points[0];
        ctx.strokeStyle = '#f59e0b';
        ctx.beginPath();
        ctx.moveTo(centerX + (p.x - 1) * scale.value, centerY - (p.y - 1) * scale.value);
        ctx.lineTo(centerX + (p.x + 1) * scale.value, centerY - (p.y + 1) * scale.value);
        ctx.stroke();
      }
      break;
  }
  
  ctx.setLineDash([]);
};

// Методы управления графиком
const zoomIn = () => {
  scale.value = Math.min(scale.value * 1.2, 200);
  drawCurve();
};

const zoomOut = () => {
  scale.value = Math.max(scale.value / 1.2, 5); // Минимальный масштаб 5
  drawCurve();
};

const resetZoom = () => {
  scale.value = 30;
  offsetX.value = 0;
  offsetY.value = 0;
  drawCurve();
};

const startDrag = (e) => {
  isDragging.value = true;
  lastX.value = e.clientX;
  lastY.value = e.clientY;
};

const onDrag = (e) => {
  if (!isDragging.value) return;
  
  const dx = e.clientX - lastX.value;
  const dy = e.clientY - lastY.value;
  
  offsetX.value += dx;
  offsetY.value += dy;
  
  lastX.value = e.clientX;
  lastY.value = e.clientY;
  
  drawCurve();
};

const endDrag = () => {
  isDragging.value = false;
};

const onWheel = (e) => {
  e.preventDefault();
  const delta = e.deltaY > 0 ? -1 : 1;
  const zoomFactor = delta > 0 ? 1.1 : 0.9;
  const newScale = Math.max(5, Math.min(200, scale.value * zoomFactor)); // Ограничиваем масштаб
  
  // Центрируем масштабирование на курсоре
  const mouseX = e.clientX - curveCanvas.value.getBoundingClientRect().left;
  const mouseY = e.clientY - curveCanvas.value.getBoundingClientRect().top;
  
  const worldX = (mouseX - curveCanvas.value.width/2 - offsetX.value) / scale.value;
  const worldY = -(mouseY - curveCanvas.value.height/2 - offsetY.value) / scale.value;
  
  scale.value = newScale;
  offsetX.value = mouseX - curveCanvas.value.width/2 - worldX * scale.value;
  offsetY.value = mouseY - curveCanvas.value.height/2 + worldY * scale.value;
  
  drawCurve();
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