import './app.css'
import App from './App.svelte'
import "carbon-components-svelte/css/white.css"
import cors from 'cors'

const app = new App({
  target: document.getElementById('app')
})
export default app
