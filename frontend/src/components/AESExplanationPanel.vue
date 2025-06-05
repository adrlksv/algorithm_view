<template>
  <div class="p-6 rounded-xl shadow-lg bg-gray-800 border border-gray-700 transition-all duration-300">
    <h2 class="text-2xl font-bold mb-4 text-green-400">Пояснения к шагам AES</h2>
    
    <div v-if="currentExplanation" class="space-y-4">
      <h3 class="text-xl font-semibold text-green-300">{{ currentExplanation.title }}</h3>
      <div class="text-gray-300 space-y-2">
        <p v-for="(paragraph, idx) in currentExplanation.content" :key="idx">{{ paragraph }}</p>
      </div>
      
      <div v-if="currentExplanation.image" class="mt-4">
        <img :src="currentExplanation.image" :alt="currentExplanation.title" class="max-w-full rounded-lg border border-gray-700">
      </div>

      <div v-if="currentExplanation.keySizes" class="mt-4 p-3 bg-gray-700 rounded-lg">
        <h4 class="font-medium text-green-300 mb-2">Различия для размеров ключа:</h4>
        <ul class="list-disc pl-5 space-y-1 text-sm text-gray-300">
          <li v-for="(item, size) in currentExplanation.keySizes" :key="size">
            <span class="font-mono font-bold">{{ size }} бит:</span> {{ item }}
          </li>
        </ul>
      </div>
    </div>
    
    <div v-else class="text-gray-400 italic">
      Выберите шаг алгоритма для просмотра подробных пояснений
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  stepName: String,
  keySize: {
    type: Number,
    default: 256
  }
});

const explanations = {
  'Генерация ключа': {
    title: 'Генерация ключа AES',
    content: (keySize) => [
      `Для ${keySize}-битного ключа:`,
      keySize === 128 
        ? 'Генерируется 16-байтовый ключ (128 бит) для 10 раундов шифрования'
        : keySize === 192
        ? 'Генерируется 24-байтовый ключ (192 бита) для 12 раундов шифрования'
        : 'Генерируется 32-байтовый ключ (256 бит) для 14 раундов шифрования',
      'Ключ должен быть криптографически стойким и храниться в секрете'
    ],
    keySizes: {
      '128': '16 байт, 10 раундов, 11 ключей раунда',
      '192': '24 байта, 12 раундов, 13 ключей раунда',
      '256': '32 байта, 14 раундов, 15 ключей раунда'
    }
  },
  'Генерация IV': {
    title: 'Генерация вектора инициализации (IV)',
    content: [
      'Вектор инициализации (IV) используется в режимах шифрования, таких как CBC',
      'IV должен быть случайным и уникальным для каждого шифрования',
      'Размер IV всегда 16 байт (128 бит), независимо от размера ключа AES'
    ]
  },
  'Дополнение данных (Padding)': {
    title: 'Дополнение данных (Padding)',
    content: [
      'AES работает с блоками по 16 байт (128 бит)',
      'Если исходные данные не кратны 16 байтам, применяется дополнение PKCS#7',
      'Пример: для дополнения 3 байтами добавляется "03 03 03"'
    ],
    image: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/PKCS7_padding.svg/1200px-PKCS7_padding.svg.png'
  },
  'Преобразование в State Matrix': {
    title: 'State Matrix',
    content: [
      'Исходные данные преобразуются в матрицу 4x4 байта',
      'Заполнение происходит по столбцам: первые 4 байта - первый столбец',
      'Матрица состояния обрабатывается на каждом раунде шифрования'
    ],
    image: 'https://www.researchgate.net/publication/334390891/figure/fig1/AS:781058376359936@1563388839605/AES-State-matrix-representation-of-the-128-bit-block.png'
  },
  'Начальное добавление ключа': {
    title: 'Начальное добавление ключа',
    content: (keySize) => [
      `Для ${keySize}-битного ключа:`,
      keySize === 128
        ? 'Весь 16-байтовый ключ используется для начального раунда'
        : keySize === 192
        ? 'Первые 16 байт из 24-байтового ключа для начального раунда'
        : 'Первые 16 байт из 32-байтового ключа для начального раунда',
      'Применяется операция XOR между State Matrix и ключом'
    ],
    keySizes: {
      '128': 'Используется весь ключ (16 байт)',
      '192': 'Используются первые 16 байт из 24',
      '256': 'Используются первые 16 байт из 32'
    }
  },
  'SubBytes': {
    title: 'SubBytes (Замена байтов)',
    content: [
      'Каждый байт матрицы заменяется по таблице S-Box',
      'S-Box обеспечивает нелинейное преобразование',
      'Одинаковая для всех размеров ключа (128/192/256 бит)'
    ],
    image: 'https://www.researchgate.net/publication/334390891/figure/fig2/AS:781058376359937@1563388839606/Substitution-box-S-box-used-in-AES.png'
  },
  'ShiftRows': {
    title: 'ShiftRows (Сдвиг строк)',
    content: [
      'Строки матрицы сдвигаются циклически:',
      'Строка 0: без сдвига',
      'Строка 1: сдвиг на 1 байт влево',
      'Строка 2: сдвиг на 2 байта влево', 
      'Строка 3: сдвиг на 3 байта влево'
    ],
    image: 'https://www.researchgate.net/publication/334390891/figure/fig3/AS:781058376359938@1563388839607/ShiftRows-transformation-in-AES.png'
  },
  'MixColumns': {
    title: 'MixColumns (Перемешивание столбцов)',
    content: [
      'Каждый столбец умножается на матрицу в поле GF(2^8)',
      'Обеспечивает диффузию между байтами',
      'Не выполняется в последнем раунде'
    ],
    image: 'https://www.researchgate.net/publication/334390891/figure/fig4/AS:781058376359939@1563388839608/MixColumns-transformation-in-AES.png'
  },
  'AddRoundKey': {
    title: 'AddRoundKey (Добавление ключа раунда)',
    content: (keySize) => [
      `Для ${keySize}-битного AES:`,
      keySize === 128
        ? '11 ключей раунда (включая начальный)'
        : keySize === 192
        ? '13 ключей раунда'
        : '15 ключей раунда',
      'Ключи генерируются из основного ключа',
      'Применяется операция XOR к State Matrix'
    ],
    keySizes: {
      '128': '10 раундов, 11 ключей',
      '192': '12 раундов, 13 ключей',
      '256': '14 раундов, 15 ключей'
    },
    image: 'https://www.researchgate.net/publication/334390891/figure/fig5/AS:781058376359940@1563388839609/AddRoundKey-transformation-in-AES.png'
  },
  'Key Schedule': {
    title: 'Генерация ключей раунда',
    content: (keySize) => {
      const content = [
        `Генерация ключей для ${keySize}-битного AES:`,
        '1. RotWord - циклический сдвиг',
        '2. SubWord - замена байтов через S-Box',
        '3. XOR с константой раунда'
      ];
      
      if (keySize === 256) {
        content.push('4. Для 256-бит: дополнительный SubWord каждые 4 слова');
      }
      
      return content;
    },
    keySizes: {
      '128': '4-словные ключи, 10 раундов',
      '192': '6-словные ключи, 12 раундов',
      '256': '8-словные ключи с доп. SubWord, 14 раундов'
    },
    image: 'https://www.researchgate.net/publication/334390891/figure/fig6/AS:781058376359941@1563388839610/Key-schedule-algorithm-for-AES-128.png'
  },
  'Завершение': {
    title: 'Завершение шифрования',
    content: (keySize) => [
      `Завершение ${keySize}-битного AES:`,
      keySize === 128
        ? '10 раундов выполнено'
        : keySize === 192
        ? '12 раундов выполнено'
        : '14 раундов выполнено',
      'Финальный блок зашифрован',
      'Готов к передаче или хранению'
    ],
    keySizes: {
      '128': '10 раундов, последний без MixColumns',
      '192': '12 раундов, последний без MixColumns',
      '256': '14 раундов, последний без MixColumns'
    }
  }
};

const currentExplanation = computed(() => {
  if (!props.stepName) return null;

  // Поиск подходящего объяснения
  for (const [key, value] of Object.entries(explanations)) {
    if (props.stepName.includes(key)) {
      const explanation = {...value};
      
      // Если content - функция, вызываем с текущим keySize
      if (typeof explanation.content === 'function') {
        explanation.content = explanation.content(props.keySize);
      }
      
      return explanation;
    }
  }

  // Обработка шагов раундов
  if (props.stepName.includes('Раунд')) {
    const roundNumber = props.stepName.match(/Раунд (\d+)/)?.[1];
    if (roundNumber) {
      const totalRounds = props.keySize === 128 ? 10 : 
                         props.keySize === 192 ? 12 : 14;
      
      return {
        title: `Раунд ${roundNumber}/${totalRounds}`,
        content: [
          `Тип ключа: ${props.keySize} бит`,
          `Раунд ${roundNumber} из ${totalRounds}`,
          roundNumber == totalRounds 
            ? 'Финальный раунд (без MixColumns)'
            : 'Обычный раунд',
          'Операции: SubBytes → ShiftRows' + 
          (roundNumber == totalRounds ? '' : ' → MixColumns') + 
          ' → AddRoundKey'
        ],
        keySizes: {
          '128': `Раунд ${roundNumber} из 10`,
          '192': `Раунд ${roundNumber} из 12`,
          '256': `Раунд ${roundNumber} из 14`
        }
      };
    }
  }

  return {
    title: props.stepName,
    content: ['Подробное описание этого шага будет добавлено в ближайшее время.']
  };
});
</script>