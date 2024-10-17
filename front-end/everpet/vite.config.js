import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs';
import path from 'path';

const __dirname = path.resolve();

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'index.html')
      }
    }
  },
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_APP_LOCALHOST_URL, // 실제 API 서버의 주소로 변경
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    },
    https: {
      key: fs.readFileSync(path.resolve(__dirname, 'certs', 'privkey.pem')),
      cert: fs.readFileSync(path.resolve(__dirname, 'certs', 'fullchain.pem')),
    },
    port: 5173, // 원하는 포트로 설정
  },
  resolve: {
    alias: [
      { find: "@", replacement: "/src" },
      { find: "@components", replacement: "/src/components" },
      { find: "@headers", replacement: "/src/components/headers" },
      { find: "@pages", replacement: "/src/pages" },
    ],
  },
  build: {
    rollupOptions: {
      output: {
        entryFileNames: 'assets/main.js', // 메인 엔트리 파일 이름 고정
        chunkFileNames: 'assets/[name].js', // 청크 파일 이름 고정
        assetFileNames: ({ name }) => {
          if (name && name.endsWith('.css')) {
            return 'assets/main.css'; // CSS 파일 이름 고정
          }
          return 'assets/[name][extname]'; // 기타 자산 파일 이름
        }
      },
    },
  },
})