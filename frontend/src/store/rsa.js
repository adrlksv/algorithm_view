import { defineStore } from 'pinia';
import { generateRSAKeys } from '../api/rsa';

export const useRSAStore = defineStore('rsa', {
  state: () => ({
    privateKey: '',
    publicKey: '',
    loading: false,
    error: null
  }),
  actions: {
    async generateKeys(keySize = 2048) {
      this.loading = true;
      this.error = null;
      try {
        const result = await generateRSAKeys(keySize);
        this.privateKey = result.private_key;
        this.publicKey = result.public_key;
        return true;
      } catch (error) {
        this.error = error.message;
        console.error('RSA generation error:', error);
        return false;
      } finally {
        this.loading = false;
      }
    }
  }
});