import { defineConfig } from "@lovable.dev/vite-tanstack-config";

export default defineConfig({
  nitro: false,
  tanstackStart: {
    server: { entry: "server" },
    spa: {
      enabled: true,
      prerender: { outputPath: "index.html" },
    },
  },
  vite: {
    server: {
      port: 8080,
      proxy: {
        "/v1": {
          target: "http://localhost:8091",
          changeOrigin: true,
        },
        "/ws": {
          target: "ws://localhost:8091",
          ws: true,
        },
      },
    },
  },
});
