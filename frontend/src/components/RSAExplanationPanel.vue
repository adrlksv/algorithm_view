<!-- RSAExplanationPanel.vue -->
<template>
  <div class="p-6 rounded-xl shadow-lg bg-gray-800 border border-gray-700 transition-all duration-300">
    <h2 class="text-2xl font-bold mb-4 text-green-400">Пояснения к шагам RSA</h2>
    
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

      <div v-if="currentExplanation.keySizes" class="mt-3 p-3 bg-gray-700 rounded-lg">
        <h4 class="font-medium text-green-300 mb-2">Для ключа {{ keySize }} бит:</h4>
        <p class="text-gray-300 text-sm">{{ currentExplanation.keySizes[keySize] }}</p>
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
  keySize: {
    type: Number,
    default: 2048
  }
});

const explanations = {
  'Генерация простых чисел': {
    title: 'Генерация простых чисел',
    content: [
      'Выбираются два больших случайных простых числа p и q.',
      'Для проверки простоты используется тест Миллера-Рабина.'
    ],
    formula: 'p и q: простые числа',
    note: 'Чем больше бит, тем выше безопасность, но медленнее операции',
    keySizes: {
      1024: 'p и q по ~512 бит каждое (быстрее генерация, меньшая безопасность)',
      2048: 'p и q по ~1024 бит (оптимальный баланс скорости и безопасности)',
      4096: 'p и q по ~2048 бит (максимальная безопасность, медленная генерация)'
    }
  },
  'Вычисление модуля n': {
    title: 'Модуль n',
    content: [
      'Модуль n вычисляется как произведение p и q.',
      'Этот модуль будет частью обоих ключей.'
    ],
    formula: 'n = p × q',
    keySizes: {
      1024: 'n будет ~1024 бит (минимальная безопасность по современным стандартам)',
      2048: 'n будет ~2048 бит (рекомендуемый размер для большинства применений)',
      4096: 'n будет ~4096 бит (максимальная безопасность для критически важных данных)'
    }
  },
  'Функция Эйлера φ(n)': {
    title: 'Функция Эйлера',
    content: [
      'Вычисляется количество чисел, меньших n и взаимно простых с ним.',
      'Используется для определения секретной экспоненты.'
    ],
    formula: 'φ(n) = (p-1) × (q-1)'
  },
  'Открытая экспонента e': {
    title: 'Открытая экспонента',
    content: [
      'Выбирается число e, взаимно простое с φ(n).',
      'Обычно используют 65537 (2¹⁶ + 1) - число Ферма.'
    ],
    formula: '1 < e < φ(n), НОД(e, φ(n)) = 1',
    note: 'Часто используемые значения: 3, 17, 65537'
  },
  'Секретная экспонента d': {
    title: 'Секретная экспонента',
    content: [
      'Вычисляется как обратное к e по модулю φ(n).',
      'Используется расширенный алгоритм Евклида.'
    ],
    formula: 'd ≡ e⁻¹ mod φ(n)',
    note: 'd должно храниться в секрете',
    keySizes: {
      1024: 'd будет ~1024 бит (легче вычислить при атаке)',
      2048: 'd будет ~2048 бит (сложнее для взлома)',
      4096: 'd будет ~4096 бит (максимальная защита)'
    }
  },
  'Формирование ключей': {
    title: 'Формирование ключей',
    content: [
      'Открытый ключ: (e, n)',
      'Закрытый ключ: (d, n)',
      'Формат PEM используется для хранения ключей'
    ],
    formula: 'Открытый: (e, n)\nЗакрытый: (d, n)',
    keySizes: {
      1024: 'Ключи меньшего размера, подходят для тестирования',
      2048: 'Стандартный размер для большинства применений',
      4096: 'Максимальная безопасность для долгосрочного хранения'
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