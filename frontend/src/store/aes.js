import { defineStore } from 'pinia';
import { generateAESKey } from '../api/aes';

export const useAESStore = defineStore('aes', {
  state: () => ({
    key: '',
    iv: '',
    encrypted: '',
    steps: [],
    loading: false,
  }),
  actions: {
    async generateAES() {
      this.loading = true;
      this.steps = [];
      try {
        const result = await generateAESKey();
        this.key = result.key;
        this.iv = result.iv;
        this.encrypted = result.encrypted_sample;

        // Моделируем пошаговый процесс
        this.steps = [
          { title: 'Генерация ключа', content: this.key },
          { title: 'Генерация IV', content: this.iv },
          { title: 'Шифрование текста', content: this.encrypted },
        ];
      } catch (e) {
        console.error('Ошибка AES:', e);
      } finally {
        this.loading = false;
      }
    }
  }
});
