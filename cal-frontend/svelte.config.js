// svelte.config.js
import adapter from '@sveltejs/adapter-auto';
import preprocess from 'svelte-preprocess';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Use svelte-preprocess for things like PostCSS, TypeScript, etc.
	preprocess: preprocess(),

	kit: {
		adapter: adapter()
		// no 'vite' section here any more
	}
};

export default config;
