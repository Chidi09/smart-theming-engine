
// theme.css.js - Helper for Tailwind config to read dynamic values
module.exports = {{
    colors: {{
        primary: '#1A73E8',
        secondary: '#F0F0F0',
        accent: '#EA4335',
        text_dark: '#333333',
        text_light: '#FFFFFF',
        background_light: '#F9FAFB',
        background_dark: '#1F2937',
        surface: '#FFFFFF',
    }},
    fontSizes: {{
        h1: '60px',
        h2: '48px',
        h3: '38px',
        h4: '30px',
        h5: '24px',
        h6: '20px',
        body: '18px',
        small: '15px',
        caption: '13px',
        display: '80px',
    }},
    spacing: {{
        xs: '15.0px',
        sm: '18px',
        md: '20px',
        lg: '24px',
        xl: '30px',
        '2xl': '38px',
    }},
    lineHeights: {{
        tight: '1.25',
        normal: '1.5',
        relaxed: '1.625',
        loose: '2',
    }},
    letterSpacings: {{
        tight: '-0.025em',
        normal: '0em',
        wide: '0.025em',
        wider: '0.05em',
        widest: '0.1em',
    }},
    boxShadows: {{
        default: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        subtle: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        prominent: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        bold: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    }},
    borderStyles: {{
        default: 'solid',
    }},
    borderWidths: {{
        default: '1px',
    }},
    borderColors: {{
        default: 'var(--color-secondary)',
    }},
    transitionDurations: {{
        default: '300ms',
    }},
    transitionTimingFunctions: {{
        default: 'ease-in-out',
    }},
}};
