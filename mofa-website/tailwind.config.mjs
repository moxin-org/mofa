/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'mondrian-red': '#E31E24',
        'mondrian-blue': '#0C5DA5',
        'mondrian-yellow': '#FFD500',
        'mondrian-black': '#000000',
        'mondrian-white': '#FFFFFF',
        'mondrian-gray': '#E5E5E5',
        
        'mofa-primary': '#E31E24',
        'mofa-secondary': '#0C5DA5',
        'mofa-accent': '#FFD500',
      },
      fontFamily: {
        sans: ['Inter', 'Noto Sans SC', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      animation: {
        'grid-float': 'gridFloat 20s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        gridFloat: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            maxWidth: 'none',
            color: theme('colors.gray.900'),
            a: {
              color: theme('colors.mondrian-blue'),
              '&:hover': {
                color: theme('colors.mondrian-red'),
              },
            },
            'code::before': {
              content: '""',
            },
            'code::after': {
              content: '""',
            },
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
} 