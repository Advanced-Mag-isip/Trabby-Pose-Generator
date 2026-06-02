// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
    server: {
        host: '0.0.0.0',
        port: 8312,
        allowedHosts: [
            'sandbox1.advancedthinkers.app',
            'http://165.22.107.245:8313',
            'http://localhost:8313',
        ]
    }
});
