/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html"],
  theme: {
    extend: {
      backgroundImage: {
        'wind': "url('./assets/wind-1.gif')",
        'fireplace': "url('./assets/fireplace-at.gif')",
        'rain': "url('./assets/summer-1.gif')"
      }
    },
  },
  plugins: [],
}

