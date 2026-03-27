import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [
      'bore.pub',
      '.bore.pub',
      'serveo.net',
      '.serveo.net',
      '44aeaf72ba66b435-185-106-29-190.serveousercontent.com',
      '.serveousercontent.com',
      'localhost',
      '.localhost'
    ],
    host: true,
    port: 5173
  }
})