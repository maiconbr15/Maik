/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1f4788',
        secondary: '#0f2744',
        accent: '#ff6b35',
      },
    },
  },
  plugins: [],
}
