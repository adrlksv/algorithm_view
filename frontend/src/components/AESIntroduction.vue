<template>
  <div class="p-6 rounded-xl shadow-lg bg-gray-800 border border-gray-700 transition-all duration-300">
    <h2 class="text-2xl font-bold mb-4 text-green-400">Введение в AES</h2>
    
    <div class="space-y-4 text-gray-300">
      <p>
        <strong>AES (Advanced Encryption Standard)</strong> - симметричный алгоритм блочного шифрования, 
        принятый в качестве стандарта правительством США в 2001 году. Он заменил устаревший стандарт DES.
      </p>
      
      <p>
        AES работает с блоками данных размером 128 бит (16 байт) и использует ключи длиной 128, 192 или 256 бит.
        Количество раундов шифрования зависит от размера ключа:
      </p>
      
      <ul class="list-disc pl-6 space-y-1">
        <li>128 бит - 10 раундов</li>
        <li>192 бит - 12 раундов</li>
        <li>256 бит - 14 раундов</li>
      </ul>

      <h3 class="text-lg font-semibold text-green-300 mt-4 mb-2">Основные преобразования:</h3>
      <ul class="list-disc pl-6 space-y-2">
        <li>
          <strong>SubBytes</strong> - нелинейная замена каждого байта через S-Box:
          <div class="text-sm text-gray-400 mt-1">S(x) = M·x⁻¹ + C</div>
        </li>
        <li>
          <strong>ShiftRows</strong> - циклический сдвиг строк матрицы состояния:
          <div class="text-sm text-gray-400 mt-1">Строка N сдвигается на N байт (0-3)</div>
        </li>
        <li>
          <strong>MixColumns</strong> - умножение столбцов на матрицу в GF(2⁸):
          <div class="text-sm text-gray-400 mt-1">Используется многочлен x⁸ + x⁴ + x³ + x + 1</div>
        </li>
        <li>
          <strong>AddRoundKey</strong> - побитовый XOR с ключом раунда:
          <div class="text-sm text-gray-400 mt-1">state[i,j] ⊕ round_key[i,j]</div>
        </li>
      </ul>
      
      <h3 class="text-xl font-semibold text-green-300 mt-6 mb-2">Основные преимущества AES:</h3>
      <ul class="list-disc pl-6 space-y-1">
        <li>Высокая скорость шифрования и расшифрования</li>
        <li>Устойчивость к известным атакам</li>
        <li>Эффективная реализация как на программном, так и на аппаратном уровне</li>
        <li>Гибкость в выборе длины ключа</li>
      </ul>
      
      <h3 class="text-xl font-semibold text-green-300 mt-6 mb-2">Области применения:</h3>
      <ul class="list-disc pl-6 space-y-1">
        <li>Шифрование файлов и дисков</li>
        <li>Защита сетевого трафика (SSL/TLS, VPN)</li>
        <li>Защита беспроводных сетей (WPA2)</li>
        <li>Шифрование данных в базах данных</li>
      </ul>
    </div>
  </div>
</template>