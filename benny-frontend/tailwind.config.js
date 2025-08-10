/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Your custom OSU color palette
      colors: {
        'osu-orange': '#D73F09',
        'osu-black': '#000000',
        'osu-gray': '#423E3C',
        'osu-light-gray': '#F7F5F5',
      },
    },
  },
  plugins: [],
}