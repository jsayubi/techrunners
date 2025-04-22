import { createRouter, createWebHistory } from 'vue-router';

// Import views
import ChatView from '../views/ChatView.vue';
import AboutView from '../views/AboutView.vue';

const routes = [
	{
		path: '/',
		name: 'chat',
		component: ChatView,
	},
	{
		path: '/about',
		name: 'about',
		component: AboutView,
	},
];

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes,
});

export default router;
