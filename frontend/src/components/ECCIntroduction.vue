<!-- components/ECCIntroduction.vue -->
<template>
  <div class="p-6 rounded-xl shadow-lg bg-gray-800 border border-gray-700 transition-all duration-300">
    <h2 class="text-2xl font-bold mb-4 text-green-400">Введение в ECC</h2>
    
    <div class="space-y-4 text-gray-300">
      <p>
        <strong>ECC (Elliptic Curve Cryptography)</strong> - криптографический алгоритм, основанный на математике эллиптических кривых.
        Обеспечивает такую же безопасность как RSA, но с меньшими размерами ключей.
      </p>
      
      <h3 class="text-lg font-semibold text-green-300 mt-4 mb-2">Ключевые понятия:</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div class="p-3 bg-gray-700 rounded-lg">
          <h4 class="font-medium text-green-200">Эллиптическая кривая</h4>
          <p class="text-sm">Уравнение вида: y² = x³ + ax + b</p>
        </div>
        <div class="p-3 bg-gray-700 rounded-lg">
          <h4 class="font-medium text-green-200">Точки кривой</h4>
          <p class="text-sm">Координаты (x,y), удовлетворяющие уравнению</p>
        </div>
        <div class="p-3 bg-gray-700 rounded-lg">
          <h4 class="font-medium text-green-200">Сложение точек</h4>
          <p class="text-sm">Геометрическая операция на кривой</p>
        </div>
        <div class="p-3 bg-gray-700 rounded-lg">
          <h4 class="font-medium text-green-200">Базовая точка G</h4>
          <p class="text-sm">Генератор подгруппы точек</p>
        </div>
      </div>

      <h3 class="text-lg font-semibold text-green-300 mt-4 mb-2">Основные этапы:</h3>
      <ol class="list-decimal pl-6 space-y-2">
        <li>Выбор эллиптической кривой и параметров</li>
        <li>Выбор базовой точки G</li>
        <li>Генерация закрытого ключа (случайное число)</li>
        <li>Вычисление открытого ключа (умножение точки)</li>
      </ol>

      <h3 class="text-xl font-semibold text-green-300 mt-6 mb-2">Преимущества:</h3>
      <ul class="list-disc pl-6 space-y-1">
        <li>Высокая безопасность при меньших размерах ключей</li>
        <li>Эффективность вычислений</li>
        <li>Меньший расход памяти</li>
        <li>Быстрое шифрование</li>
      </ul>
      
      <h3 class="text-xl font-semibold text-green-300 mt-6 mb-2">Применение:</h3>
      <ul class="list-disc pl-6 space-y-1">
        <li>SSL/TLS сертификаты</li>
        <li>Цифровые подписи (ECDSA)</li>
        <li>Криптовалюты (Bitcoin, Ethereum)</li>
        <li>Защищенные коммуникации</li>
      </ul>
    </div>
  </div>
</template>