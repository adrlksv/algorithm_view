<!-- components/ECCExplanationPanel.vue -->
<template>
  <div class="p-6 rounded-xl shadow-lg bg-gray-800 border border-gray-700 transition-all duration-300">
    <h2 class="text-2xl font-bold mb-4 text-green-400">Пояснения к шагам ECC</h2>
    
    <div v-if="currentExplanation" class="space-y-4">
      <h3 class="text-xl font-semibold text-green-300">{{ currentExplanation.title }}</h3>
      <div class="text-gray-300 space-y-2">
        <p v-for="(paragraph, idx) in currentExplanation.content" :key="idx">{{ paragraph }}</p>
      </div>
      
      <div v-if="currentExplanation.formula" class="mt-3 p-3 bg-gray-700 rounded-lg font-mono text-sm">
        {{ currentExplanation.formula }}
      </div>
      
      <div v-if="currentExplanation.note" class="mt-2 p-2 bg-gray-900 rounded text-sm text-gray-400">
        {{ currentExplanation.note }}
      </div>

      <div v-if="currentExplanation.curves" class="mt-3 p-3 bg-gray-700 rounded-lg">
        <h4 class="font-medium text-green-300 mb-2">Для кривой {{ curveName }}:</h4>
        <p class="text-gray-300 text-sm">{{ currentExplanation.curves[curveName] }}</p>
      </div>
    </div>
    
    <div v-else class="text-gray-400 italic">
      Выберите шаг алгоритма для просмотра пояснений
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  stepName: String,
  curveName: {
    type: String,
    default: 'secp256r1'
  }
});

const explanations = {
  'Выбор кривой': {
    title: 'Выбор эллиптической кривой',
    content: [
      'Выбирается стандартная эллиптическая кривая с определенными параметрами.',
      'Кривая определяет группу точек, используемых в криптографии.'
    ],
    formula: 'y² = x³ + ax + b mod p',
    curves: {
      'secp256r1': 'NIST P-256 (secp256r1): 256-битная кривая, широко используется',
      'secp384r1': 'NIST P-384 (secp384r1): 384-битная, более высокая безопасность',
      'secp521r1': 'NIST P-521 (secp521r1): 521-битная, максимальная безопасность'
    }
  },
  'Выбор базовой точки': {
    title: 'Базовая точка G',
    content: [
      'Выбирается генератор (базовая точка) подгруппы точек кривой.',
      'Эта точка будет использоваться для генерации ключей.'
    ],
    note: 'Базовая точка является публичным параметром кривой'
  },
  'Генерация закрытого ключа': {
    title: 'Закрытый ключ',
    content: [
      'Закрытый ключ - это случайное целое число d, выбранное из диапазона [1, n-1],',
      'где n - порядок подгруппы, генерируемой точкой G.'
    ],
    formula: 'd ∈ [1, n-1]',
    note: 'Должен храниться в секрете'
  },
  'Вычисление открытого ключа': {
    title: 'Открытый ключ',
    content: [
      'Открытый ключ вычисляется как умножение базовой точки G на закрытый ключ d.',
      'Q = d × G (точка на кривой)'
    ],
    formula: 'Q = d × G',
    note: 'Может свободно распространяться'
  },
  'Формирование ключей': {
    title: 'Формирование ключей',
    content: [
      'Закрытый ключ: целое число d',
      'Открытый ключ: точка Q на кривой',
      'Формат PEM используется для хранения ключей'
    ],
    curves: {
      'secp256r1': 'Размер закрытого ключа: 256 бит, открытого: 257 бит',
      'secp384r1': 'Размер закрытого ключа: 384 бит, открытого: 385 бит',
      'secp521r1': 'Размер закрытого ключа: 521 бит, открытого: 522 бит'
    }
  }
};

const currentExplanation = computed(() => {
  if (!props.stepName) return null;
  
  for (const [key, value] of Object.entries(explanations)) {
    if (props.stepName.includes(key)) {
      return value;
    }
  }
  
  return {
    title: props.stepName,
    content: ['Описание этого шага будет добавлено']
  };
});
</script>