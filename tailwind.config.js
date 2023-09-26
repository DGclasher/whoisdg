/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/src/**/*.js",
  ],
  theme: {
    extend: {},
  },
  variants :{
    display: ['group-focus'],
    opacity: ['group-focus'],
    inset: ['group-focus']
  },
  plugins: [],
}