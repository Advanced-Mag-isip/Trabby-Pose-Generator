// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
    server: {
        host: '0.0.0.0',
        port: 8312,
        allowedHosts: [
            'sandbox1.advancedthinkers.app',
            '165.22.107.245',
            'localhost',
            'backend',
        ]
    },
    devToolbar: {
        enabled: false
    }
});
