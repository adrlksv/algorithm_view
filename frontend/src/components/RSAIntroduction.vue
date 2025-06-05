<!-- components/RSAIntroduction.vue -->
<template>
  <div class="p-6 rounded-xl shadow-lg bg-gray-800 border border-gray-700 transition-all duration-300">
    <h2 class="text-2xl font-bold mb-4 text-green-400">Введение в RSA</h2>
    
    <div class="space-y-4 text-gray-300">
      <p>
        <strong>RSA</strong> - асимметричный криптографический алгоритм, основанный на вычислительной сложности 
        задачи факторизации больших чисел. Разработан в 1977 году.
      </p>
      
      <h3 class="text-lg font-semibold text-green-300 mt-4 mb-2">Ключевые понятия:</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div class="p-3 bg-gray-700 rounded-lg">
          <h4 class="font-medium text-green-200">Асимметричное шифрование</h4>
          <p class="text-sm">Использует пару ключей: открытый и закрытый</p>
        </div>
        <div class="p-3 bg-gray-700 rounded-lg">
          <h4 class="font-medium text-green-200">Факторизация</h4>
          <p class="text-sm">Разложение числа на простые множители</p>
        </div>
        <div class="p-3 bg-gray-700 rounded-lg">
          <h4 class="font-medium text-green-200">Открытый ключ</h4>
          <p class="text-sm">(e, n) - для шифрования и проверки подписи</p>
        </div>
        <div class="p-3 bg-gray-700 rounded-lg">
          <h4 class="font-medium text-green-200">Закрытый ключ</h4>
          <p class="text-sm">(d, n) - для расшифровки и создания подписи</p>
        </div>
      </div>

      <h3 class="text-lg font-semibold text-green-300 mt-4 mb-2">Основные этапы:</h3>
      <ol class="list-decimal pl-6 space-y-2">
        <li>Генерация двух больших простых чисел p и q</li>
        <li>Вычисление модуля n = p × q</li>
        <li>Вычисление функции Эйлера φ(n) = (p-1)(q-1)</li>
        <li>Выбор открытой экспоненты e (обычно 65537)</li>
        <li>Вычисление секретной экспоненты d ≡ e⁻¹ mod φ(n)</li>
      </ol>

      <h3 class="text-xl font-semibold text-green-300 mt-6 mb-2">Применение:</h3>
      <ul class="list-disc pl-6 space-y-1">
        <li>Шифрование данных</li>
        <li>Цифровые подписи</li>
        <li>Обмен ключами</li>
        <li>Аутентификация</li>
      </ul>
    </div>
  </div>
</template>