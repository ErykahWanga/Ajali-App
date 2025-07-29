module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#d32f2f", // Red
        secondary: "#000000", // Black
        light: "#ffffff",
        dark: "#1a1a1a",
        gray: {
          100: "#f8f9fa",
          200: "#e9ecef",
          800: "#212529",
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  darkMode: 'class',
  plugins: [],
}