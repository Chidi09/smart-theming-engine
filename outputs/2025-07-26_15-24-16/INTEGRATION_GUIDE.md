
# Integration Guide

This guide explains how to integrate the generated theme files into your web project.

## 1. `themed-layout.html`

This file provides a complete example of a web page using the generated theme.
You can open it directly in your browser to preview the design.
It uses Tailwind CSS classes and will eventually load the `theme.css` for custom properties.

## 2. `tailwind.config.js`

This file contains the generated color palette, font families, and spacing scale for Tailwind CSS.

**To use it in your Tailwind project:**

1.  **Locate your existing `tailwind.config.js` file.** If you don't have one, you can generate a basic one with `npx tailwindcss init`.
2.  **Merge the `theme.extend` section** from the generated `tailwind.config.js` into your project's `tailwind.config.js`.

    **Example `tailwind.config.js` structure:**

    ```javascript
    // tailwind.config.js
    module.exports = {
      content: [
        './*.html',
        './**/*.html',
        './**/*.js',
        // Add other paths where you use Tailwind classes
      ],
      theme: {
        extend: {
          // PASTE THE 'extend' OBJECT FROM THE GENERATED FILE HERE
          colors: {
            primary: '#000000',
            secondary: '#102549',
            accent: '#a589a9',
          },
          fontFamily: {
            heading: ['Oswald', 'sans-serif'],
            body: ['Merriweather', 'sans-serif'],
          },
          fontSize: {
            xs: '11px',
            sm: '17px',
            base: '17px',
            lg: '28px',
            xl: '46px',
            '2xl': '74px',
            '3xl': '120px',
            '4xl': '195px',
            '5xl': '316px',
          },
          spacing: {
            xs: '6px',
            sm: '10px',
            md: '16px',
            lg: '26px',
            xl: '42px',
          },
        },
      },
      plugins: [],
    };
    ```

3.  **Recompile your Tailwind CSS** if you are using a build process (e.g., `npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch`).

## 3. `theme.css`

This file provides the generated theme's colors, fonts, and spacing as standard CSS custom properties (variables). This is useful for projects that do not use Tailwind CSS or for integrating the theme into specific components.

**To use it in your project:**

1.  **Link the `theme.css` file** in your HTML `<head>` section:
    ```html
    <link rel="stylesheet" href="path/to/theme.css">
    ```
    (Adjust `path/to/theme.css` to the correct relative path from your HTML file.)

2.  **Use the CSS variables** in your own CSS:
    ```css
    body {
        font-family: var(--font-body);
        font-size: var(--font-size-base);
        color: var(--color-primary);
    }

    h1 {
        font-family: var(--font-heading);
        font-size: var(--font-size-5xl);
        color: var(--color-accent);
    }

    .my-component {
        margin-top: var(--spacing-lg);
        padding: var(--spacing-md);
        background-color: var(--color-secondary);
    }
    ```

## Further Customization

* **Adjust Colors:** You can manually edit the hex codes in `tailwind.config.js` or `theme.css` to fine-tune your palette.
* **Change Fonts:** Modify the `fontFamily` arrays in `tailwind.config.js` or the `--font-*` variables in `theme.css`. Remember to link new Google Fonts in your HTML if you change them (`<link href="https://fonts.googleapis.com/css2?family=New+Font&display=swap" rel="stylesheet">`).
* **Modify Spacing/Sizes:** Adjust the `spacing` or `fontSize` values in `tailwind.config.js` or the `--spacing-*` and `--font-size-*` variables in `theme.css`.

This guide should help you quickly integrate the generated theme into your projects!
