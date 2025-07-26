
// tailwind.config.js
/** @type {{import('tailwindcss').Config}} */
const colors = require('./theme.css.js'); // Import generated colors from a helper JS file
const fontSizes = require('./theme.css.js').fontSizes; // Import font sizes
const spacing = require('./theme.css.js').spacing; // Import spacing

module.exports = {{
  content: [
    "./*.html", // Adjust according to your project structure
    "./src/**/*.{{html,js,ts,jsx,tsx}}", // Corrected: double curly braces for the literal glob pattern
  ],
  theme: {{
    extend: {{
      // Dynamically generated colors
      colors: {{
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
        accent: 'var(--color-accent)',
        textDark: 'var(--color-text-dark)',
        textLight: 'var(--color-text-light)',
        backgroundLight: 'var(--color-background-light)',
        backgroundDark: 'var(--color-background-dark)',
        surface: 'var(--color-surface)',
      }},
      // Dynamically generated font families
      fontFamily: {{
        heading: ['var(--font-heading)', 'sans-serif'],
        body: ['var(--font-body)', 'sans-serif'],
      }},
      // Dynamically generated font sizes
      fontSize: {{
        'h1': 'var(--font-size-h1)',
        'h2': 'var(--font-size-h2)',
        'h3': 'var(--font-size-h3)',
        'h4': 'var(--font-size-h4)',
        'h5': 'var(--font-size-h5)',
        'h6': 'var(--font-size-h6)',
        'body': 'var(--font-size-body)',
        'sm': 'var(--font-size-small)', // Use 'sm' for small
        'caption': 'var(--font-size-caption)', // New custom size
        'display': 'var(--font-size-display)', // New custom size
      }},
      // Dynamically generated spacing units
      spacing: {{
        'xs': 'var(--spacing-xs)',
        'sm': 'var(--spacing-sm)',
        'md': 'var(--spacing-md)',
        'lg': 'var(--spacing-lg)',
        'xl': 'var(--spacing-xl)',
        '2xl': 'var(--spacing-2xl)',
      }},
      // Dynamically generated line heights
      lineHeight: {{
        'tight': '1.25',
        'normal': '1.5',
        'relaxed': '1.625',
        'loose': '2',
      }},
      // Dynamically generated letter spacing
      letterSpacing: {{
        'tight': '-0.025em',
        'normal': '0em',
        'wide': '0.025em',
        'wider': '0.05em',
        'widest': '0.1em',
      }},
      // Dynamic shadows (conceptual, can be extended with actual values if needed)
      boxShadow: {{
        'default': 'var(--shadow-default)',
        'subtle': 'var(--shadow-subtle)',
        'prominent': 'var(--shadow-prominent)',
        'bold': 'var(--shadow-bold)',
      }},
      // Dynamic borders (conceptual, can be extended with actual values if needed)
      borderColor: {{
        'default': 'var(--border-color-default)',
      }},
      borderWidth: {{
        'default': '1px',
      }},
      borderStyle: {{
        'default': 'var(--border-style-default)',
      }},
      // Dynamic transitions (conceptual)
      transitionDuration: {{
        'default': '300ms',
      }},
      transitionTimingFunction: {{
        'default': 'ease-in-out',
      }},
    }},
  }},
  plugins: [],
}}
