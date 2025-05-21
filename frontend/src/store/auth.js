import { defineStore } from 'pinia';
import axios from 'axios';


export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null
  }),
  actions: {
    async login(email, password) {
      await axios.post('/auth/login', { email, password });
      await this.fetchUser();
    },
    async register(username, email, password) {
      await axios.post('/auth/register', { username, email, password });
    },
    async logout() {
      await axios.post('/auth/logout');
      this.user = null;
    },
    async fetchUser() {
      try {
        const response = await axios.get('/auth/me');
        this.user = response.data;
      } catch (error) {
        this.user = null;
      }
    }
  }
});
