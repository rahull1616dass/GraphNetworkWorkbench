import sveltePreprocess from 'svelte-preprocess'
import switchCase from 'svelte-switch-case'
import json from "@rollup/plugin-json"

export default {
  // Consult https://github.com/sveltejs/svelte-preprocess
  // for more information about preprocessors
  preprocess: sveltePreprocess(),
  plugins: [
    json(),
  ]
}
