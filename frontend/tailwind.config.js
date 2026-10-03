/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        wood: {
          50: '#fbf8f3',
          100: '#f5eee3',
          200: '#ebdcbf',
          300: '#dec399',
          400: '#cfa26d',
          500: '#b88247',
          600: '#9d6738',
          700: '#7f4f2e',
          800: '#674029',
          900: '#543625',
          950: '#301c13',
        },
        blueprint: {
          50: '#eef6fc',
          100: '#d9ebf9',
          200: '#b8daf4',
          300: '#87c1ec',
          400: '#4fa1e0',
          500: '#2a84cb',
          600: '#1b69ab',
          700: '#17548b',
          800: '#164873',
          900: '#0e2e4c',
          950: '#081c30',
        }
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
