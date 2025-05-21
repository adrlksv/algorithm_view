<template>
  <div class="p-4 bg-[#0f0f0f] text-green-400 rounded shadow-lg animate-fade-in">
    <div v-for="(step, index) in steps" :key="index" class="mb-4">
      <h2 class="text-xl font-bold mb-1">{{ step.title }}</h2>
      <p class="break-all bg-[#1e1e1e] p-2 rounded">{{ step.content }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps(['steps']);
</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.6s ease-in-out;
}
</style>
