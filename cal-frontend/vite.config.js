import { sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
	server: {
		proxy: {
			// any request to /api/* will get forwarded to your Django server
			'/api': {
				target: 'http://127.0.0.1:8000',
				changeOrigin: true,
				secure: false
			}
		}
	}
};

export default config;
