import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://backend:8000',  // имя сервиса из docker-compose
        changeOrigin: true,
      },
      '/portal': {
        target: 'http://backend:8000',  // имя сервиса из docker-compose
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'build',
  },
});