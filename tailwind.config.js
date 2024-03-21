/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html"],
  theme: {
    extend: {
      backgroundImage: {
        'wind': "url('./assets/gif/wind-1.gif')",
        'fireplace': "url('./assets/gif/fireplace-at.gif')",
        'rain': "url('./assets/gif/summer-1.gif')"
      }
    },
  },
  plugins: [],
}

