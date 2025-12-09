/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'cyber-black': '#0a0a0f',
        'cyber-darker': '#0d0d14',
        'cyber-dark': '#12121a',
        'cyber-gray': '#1a1a24',
        'cyber-light': '#2a2a3a',
        'cyber-blue': '#00d4ff',
        'cyber-blue-dim': '#0099cc',
        'cyber-green': '#00ff88',
        'cyber-red': '#ff3366',
        'cyber-yellow': '#ffcc00',
        'cyber-purple': '#aa66ff',
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
        display: ['Orbitron', 'sans-serif'],
      },
      boxShadow: {
        cyber: '0 0 20px rgba(0, 212, 255, 0.3)',
        'cyber-strong': '0 0 40px rgba(0, 212, 255, 0.5)',
      },
    },
  },
  plugins: [],
};
