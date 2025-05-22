<template>
  <div class="p-4 bg-[#0f0f0f] text-green-400 rounded shadow-lg">
    <!-- Заголовок и раунд -->
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">Состояние шифрования</h2>
      <div class="text-sm">
        Раунд: {{ currentRound }}/{{ totalRounds }}
      </div>
    </div>

    <!-- Визуализация блока -->
    <div class="grid grid-cols-4 gap-2 mb-6 justify-center">
      <transition-group name="cell" tag="div" class="contents">
        <div
          v-for="(byte, idx) in currentState"
          :key="`${idx}-${byte}-${stepKey}`"
          class="w-12 h-12 flex items-center justify-center rounded bg-[#1e1e1e] text-lime-400 font-mono text-sm border border-green-700"
          :class="{
            'bg-green-900': highlightedBytes.includes(idx),
            'border-yellow-400': highlightedBytes.includes(idx)
          }"
          :style="{'transition-duration': `${animationSpeed}ms`}"
        >
          {{ byte }}
        </div>
      </transition-group>
    </div>

    <!-- Шаги описания -->
    <transition-group name="fade" tag="div">
      <div
        v-for="(step, index) in displayedSteps"
        :key="`step-${index}-${stepKey}`"
        class="mb-4 p-3 rounded-lg"
        :class="{
          'bg-green-900/30': index === displayedSteps.length - 1,
          'border-l-4 border-green-500': index === displayedSteps.length - 1
        }"
        :style="{'transition-duration': `${animationSpeed}ms`}"
      >
        <h2 class="text-lg font-bold mb-1 flex items-center">
          <span class="mr-2">{{ step.title }}</span>
          <span v-if="step.round" class="text-xs bg-green-800 px-2 py-1 rounded">
            Раунд {{ step.round }}
          </span>
        </h2>
        <p class="break-all bg-[#1e1e1e] p-2 rounded">{{ step.content }}</p>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';

const props = defineProps({
  steps: Array,
  animationSpeed: {
    type: Number,
    default: 1500,
    validator: value => typeof value === 'number'
  }
});

const displayedSteps = ref([]);
const currentState = ref(Array(16).fill('00'));
const highlightedBytes = ref([]);
const stepKey = ref(0);
let timeoutId = null;

const totalRounds = computed(() => {
  const lastRoundStep = props.steps?.findLast(step => step.round);
  return lastRoundStep ? lastRoundStep.round : 0;
});

const currentRound = computed(() => {
  const lastStep = displayedSteps.value[displayedSteps.value.length - 1];
  return lastStep?.round || 0;
});

const processSteps = () => {
  clearTimeout(timeoutId);
  displayedSteps.value = [];
  currentState.value = Array(16).fill('00');
  highlightedBytes.value = [];
  stepKey.value++;

  if (!props.steps?.length) return;

  let index = 0;
  const processNextStep = () => {
    if (index >= props.steps.length) return;

    const step = props.steps[index];
    displayedSteps.value.push(step);
    
    if (step.state) {
      currentState.value = [...step.state];
      
      if (index > 0 && props.steps[index-1]?.state) {
        highlightedBytes.value = step.state
          .map((byte, i) => byte !== props.steps[index-1].state[i] ? i : -1)
          .filter(i => i !== -1);
        
        setTimeout(() => highlightedBytes.value = [], 1000);
      }
    }

    index++;
    if (index < props.steps.length) {
      timeoutId = setTimeout(processNextStep, props.animationSpeed);
    }
  };

  processNextStep();
};

watch(() => props.steps, processSteps, { immediate: true });

watch(() => props.animationSpeed, (newSpeed, oldSpeed) => {
  if (newSpeed !== oldSpeed) {
    processSteps();
  }
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active,
.cell-enter-active,
.cell-leave-active {
  transition-property: opacity, transform;
  transition-timing-function: ease;
}
.fade-enter-from,
.cell-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-enter-to,
.cell-enter-to {
  opacity: 1;
  transform: translateY(0);
}
</style>