<template>
  <router-view />
</template>

<script setup>
</script>

<style>
/* Глобальные стили */
body {
  @apply bg-gray-900 text-gray-100 font-sans antialiased;
}

/* Анимации для переходов между страницами */
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Стили для скроллбара */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  @apply bg-gray-800;
}
::-webkit-scrollbar-thumb {
  @apply bg-gray-600 rounded-full;
}
::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-500;
}
</style>