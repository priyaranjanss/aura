/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      // AURA design system palette (see docs/DESIGN.md)
      colors: {
        aura: {
          bg: '#0f0f0f',
          surface: '#1a1a1a',
          'surface-light': '#262626',
          border: '#333333',
          primary: '#6366f1',
          'primary-hover': '#4f46e5',
          'text-secondary': '#a3a3a3',
        },
      },
      fontFamily: {
        sans: [
          'Inter',
          'system-ui',
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          'Roboto',
          'sans-serif',
        ],
      },
    },
  },
  plugins: [],
};
