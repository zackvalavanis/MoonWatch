import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    babel({ presets: [reactCompilerPreset()] })
  ],
  resolve: {
    // ⬇️ Forces Vite/Rolldown to bundle a single, unified copy of React across pnpm symlinks
    dedupe: ['react', 'react-dom', 'react-router'],
  },
})
