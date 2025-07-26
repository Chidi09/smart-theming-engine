
// theme.css.js - Helper for Tailwind config to read dynamic values
module.exports = {{
    colors: {{
        primary: '#FFFFFF',
        secondary: '#CCCCCC',
        accent: '#000000',
        text_dark: '#333333',
        text_light: '#FFFFFF',
        background_light: '#F9FAFB',
        background_dark: '#1F2937',
        surface: '#FFFFFF',
    }},
    fontSizes: {{
        h1: '554px',
        h2: '330px',
        h3: '197px',
        h4: '117px',
        h5: '70px',
        h6: '42px',
        body: '25px',
        small: '15px',
        caption: '11px',
        display: '931px',
    }},
    spacing: {{
        xs: '15.0px',
        sm: '25px',
        md: '42px',
        lg: '70px',
        xl: '117px',
        '2xl': '197px',
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
