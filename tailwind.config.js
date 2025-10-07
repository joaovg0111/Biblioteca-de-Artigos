/** @type {import('tailwindcss').Config} */
module.exports = {
  // --- MUDANÇA: Habilita o dark mode ---
  darkMode: 'class',

  content: [
      './templates/**/*.html',
      './apps/**/*.py',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}