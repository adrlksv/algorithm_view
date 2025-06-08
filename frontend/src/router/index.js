import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Home from '../views/Home.vue';
import { useAuthStore } from '../store/auth';
import AESView from '../views/AESView.vue';
import RSAView from '../views/RSAView.vue';
import ECCView from '../views/ECCView.vue';

const routes = [
  { path: '/', name: 'Home', component: Home, meta: { requiresAuth: true } },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/aes', component: AESView },
  { path: '/rsa', component: RSAView, meta: { requiresAuth: true } },
  { path: '/ecc', component: ECCView, meta: { requiresAuth: true } },

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  if (!authStore.user) {
    await authStore.fetchUser();
  }
  if (to.meta.requiresAuth && !authStore.user) {
    next('/login');
  } else {
    next();
  }
});

export default router;
