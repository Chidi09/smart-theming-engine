import math
from datetime import datetime
import numpy as np
import os

# Define the Golden Ratio
GOLDEN_RATIO = 1.61803398875

def generate_layout(
    image_analysis_results: list,
    brand_guidelines: dict,
    layout_style: str,
    output_dir: str, # Added output_dir parameter
    theme_css_content: str = "" # Added parameter to inline theme.css
) -> tuple:
    """
    Generates a responsive HTML layout based on image analysis, brand guidelines,
    and user-defined layout style. Incorporates Golden Ratio principles and
    advanced image analysis metrics for dynamic adjustments.
    Saves the generated HTML to a file in the specified output directory.

    Args:
        image_analysis_results (list): List of analysis results from image_analyzer.
        brand_guidelines (dict): Parsed brand guidelines.
        layout_style (str): 'minimal', 'dense', or 'creative'.
        output_dir (str): Directory to save the generated HTML file.
        theme_css_content (str): The content of the generated theme.css to inline.

    Returns:
        tuple: A tuple containing the generated HTML content (str) and
               the active brand guidelines (dict) used for generation.
    """
    os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

    # Aggregate image analysis results (simple average for now if multiple images)
    avg_whitespace = 0.5
    avg_h_symmetry = 0.5
    avg_v_symmetry = 0.5
    avg_fractal_dimension = 1.5
    avg_entropy = 4.0
    avg_visual_balance = 0.5
    avg_aesthetic_score = 5
    
    inferred_mood_tags = set()
    inferred_typography_tags = set()
    
    if image_analysis_results:
        whitespaces = [a.get("whitespace_percentage", 50.0) for a in image_analysis_results if a.get("whitespace_percentage") is not None]
        if whitespaces: avg_whitespace = sum(whitespaces) / len(whitespaces) / 100

        h_symmetries = [a.get("symmetry", {}).get("horizontal", 0.5) for a in image_analysis_results if a.get("symmetry", {}).get("horizontal") is not None]
        if h_symmetries: avg_h_symmetry = sum(h_symmetries) / len(h_symmetries)

        v_symmetries = [a.get("symmetry", {}).get("vertical", 0.5) for a in image_analysis_results if a.get("symmetry", {}).get("vertical") is not None]
        if v_symmetries: avg_v_symmetry = sum(v_symmetries) / len(v_symmetries)
        
        fractal_dimensions = [a.get("fractal_dimension", 1.5) for a in image_analysis_results if a.get("fractal_dimension") is not None]
        if fractal_dimensions: avg_fractal_dimension = sum(fractal_dimensions) / len(fractal_dimensions)

        entropies = [a.get("entropy", 4.0) for a in image_analysis_results if a.get("entropy") is not None]
        if entropies: avg_entropy = sum(entropies) / len(entropies)

        visual_balances = [a.get("visual_balance_score", 0.5) for a in image_analysis_results if a.get("visual_balance_score") is not None]
        if visual_balances: avg_visual_balance = sum(visual_balances) / len(visual_balances)

        aesthetic_scores = [a.get("aesthetic_neural_score", {}).get("score", 5) for a in image_analysis_results if a.get("aesthetic_neural_score", {}).get("score") is not None]
        if aesthetic_scores: avg_aesthetic_score = sum(aesthetic_scores) / len(aesthetic_scores)

        if any(a.get("golden_ratio_aspect_match", False) for a in image_analysis_results):
            avg_golden_ratio_match = True

        for analysis in image_analysis_results:
            if "mood_emotion" in analysis and analysis["mood_emotion"] and analysis["mood_emotion"] != "neutral":
                for mood in analysis["mood_emotion"].split(','):
                    inferred_mood_tags.add(mood.strip())
            if "typography_inference" in analysis and analysis["typography_inference"] and analysis["typography_inference"] != "unknown":
                for typo in analysis["typography_inference"].split(','):
                    inferred_typography_tags.add(typo.strip())

    # --- Brand Guideline Revamp: Infer if not provided ---
    active_brand_guidelines = brand_guidelines.copy() if brand_guidelines else {} # Ensure it's a mutable dict

    if not active_brand_guidelines: # If no brand guidelines are provided
        print("No brand guidelines provided. Inferring from image analysis...")
        inferred_layout_preference = "classic" # Default
        inferred_design_principles = set()

        # Infer layoutPreference
        if "minimalist" in inferred_mood_tags or avg_whitespace > 0.75:
            inferred_layout_preference = "minimalist"
        elif "dense" in inferred_mood_tags or avg_whitespace < 0.25:
            inferred_layout_preference = "bold"
        elif "creative" in inferred_mood_tags or "dynamic" in inferred_mood_tags or avg_entropy > 6.5:
            inferred_layout_preference = "modern"
        
        active_brand_guidelines["layoutPreference"] = inferred_layout_preference
        print(f"Inferred layout preference: {inferred_layout_preference}")

        # Infer designPrinciples
        if avg_h_symmetry > 0.85 and avg_v_symmetry > 0.85 and avg_visual_balance > 0.9:
            inferred_design_principles.add("structured")
        if "creative" in inferred_mood_tags or "dynamic" in inferred_mood_tags or avg_entropy > 6.0:
            inferred_design_principles.add("organic")
        if "bold" in inferred_typography_tags or avg_whitespace < 0.3:
            inferred_design_principles.add("bold")
        if "light" in inferred_typography_tags or avg_whitespace > 0.7:
            inferred_design_principles.add("subtle")
        if avg_aesthetic_score >= 8 and avg_fractal_dimension < 1.3:
            inferred_design_principles.add("clean") # New principle for high aesthetic, low complexity
        if avg_fractal_dimension > 1.7 or avg_entropy > 7.0:
            inferred_design_principles.add("complex") # New principle for high complexity/randomness
        
        active_brand_guidelines["designPrinciples"] = list(inferred_design_principles)
        print(f"Inferred design principles: {', '.join(inferred_design_principles)}")
    
    # Extract design principles from active brand guidelines (either provided or inferred)
    design_principles = set()
    if "designPrinciples" in active_brand_guidelines and isinstance(active_brand_guidelines["designPrinciples"], list):
        for principle in active_brand_guidelines["designPrinciples"]:
            design_principles.add(principle.strip().lower())

    # Override layout style if brand guidelines specify a preference (using active_brand_guidelines)
    original_layout_style = layout_style # Keep original for reference
    if "layoutPreference" in active_brand_guidelines:
        if active_brand_guidelines["layoutPreference"] == "minimalist":
            layout_style = "minimal"
        elif active_brand_guidelines["layoutPreference"] == "bold":
            layout_style = "dense" # Bold can imply denser, more impactful elements
        elif active_brand_guidelines["layoutPreference"] == "classic":
            layout_style = "minimal" # Classic often implies clean, balanced
        elif active_brand_guidelines["layoutPreference"] == "modern":
            layout_style = "creative" # Modern can imply dynamic, creative
        print(f"Applying brand guideline layout preference: {active_brand_guidelines['layoutPreference']} -> {layout_style}")

    # Golden Ratio for spacing/sizing - now influenced by whitespace, balance, and aesthetic score
    base_spacing_unit = 16 # Starting point
    base_spacing_unit += (avg_whitespace * 20)
    base_spacing_unit += (avg_visual_balance * 10)
    base_spacing_unit += (avg_aesthetic_score / 10 * 10)

    if avg_fractal_dimension > 1.7 or avg_entropy > 6.5:
        base_spacing_unit *= 0.9
    elif avg_fractal_dimension < 1.3 or avg_entropy < 3.0:
        base_spacing_unit *= 1.1

    golden_spacing_xs = round(base_spacing_unit / (GOLDEN_RATIO ** 2))
    golden_spacing_sm = round(base_spacing_unit / GOLDEN_RATIO)
    golden_spacing_md = round(base_spacing_unit)
    golden_spacing_lg = round(base_spacing_unit * GOLDEN_RATIO)
    golden_spacing_xl = round(base_spacing_unit * (GOLDEN_RATIO ** 2))
    golden_spacing_2xl = round(base_spacing_unit * (GOLDEN_RATIO ** 3))

    # Dynamic styling based on analysis and new design principles
    header_shadow_class = "shadow-md"
    button_rounded_class = "rounded-full"
    section_padding_class = f"p-{golden_spacing_lg // 4}"
    card_shadow_class = "shadow-md"
    card_rounded_class = "rounded-lg"
    transition_class = ""
    bg_pattern_class = ""
    border_style_class = "border-solid"
    text_leading_class = "leading-normal"
    text_tracking_class = "tracking-normal"

    if "professional" in inferred_mood_tags or avg_aesthetic_score >= 8:
        header_shadow_class = "shadow-xl"
        card_shadow_class = "shadow-lg"
        button_rounded_class = "rounded-md"
        transition_class = "transition-all duration-500 ease-in-out"
        if avg_fractal_dimension < 1.3:
            bg_pattern_class = "bg-white"
        border_style_class = "border-gray-200 border"
        text_leading_class = "leading-relaxed"
        text_tracking_class = "tracking-tight"
    if "playful" in inferred_mood_tags or "creative" in inferred_mood_tags:
        button_rounded_class = "rounded-full"
        card_rounded_class = "rounded-3xl"
        transition_class = "transition-all duration-300 ease-in-out"
        if avg_entropy > 6.0:
            bg_pattern_class = "bg-repeat bg-center bg-gray-50 bg-opacity-20"
        border_style_class = "border-dashed border-2 border-primary"
        text_leading_class = "leading-loose"
        text_tracking_class = "tracking-wide"
    if "minimalist" in inferred_mood_tags or avg_whitespace > 0.7:
        section_padding_class = f"p-{golden_spacing_xl // 4}"
        card_shadow_class = "shadow-sm"
        card_rounded_class = "rounded-xl"
        bg_pattern_class = "bg-white"
        border_style_class = "border-none"
        text_leading_class = "leading-relaxed"
        text_tracking_class = "tracking-tight"
    if "dense" in inferred_mood_tags or avg_whitespace < 0.3:
        section_padding_class = f"p-{golden_spacing_sm // 4}"
        card_shadow_class = "shadow-none"
        if avg_entropy > 7.0:
            bg_pattern_class = "bg-gray-200"
        border_style_class = "border-solid border-gray-400 border"
        text_leading_class = "leading-tight"
        text_tracking_class = "tracking-normal"

    if "structured" in design_principles:
        button_rounded_class = "rounded-md"
        card_rounded_class = "rounded-lg"
        header_shadow_class = "shadow-lg"
        border_style_class = "border-solid border-gray-300 border-2"
        text_leading_class = "leading-normal"
        text_tracking_class = "tracking-tight"
    if "organic" in design_principles:
        button_rounded_class = "rounded-full"
        card_rounded_class = "rounded-3xl"
        bg_pattern_class = "bg-repeat bg-center bg-gray-100 bg-opacity-50"
        border_style_class = "border-dotted border-primary border-2"
        text_leading_class = "leading-loose"
        text_tracking_class = "tracking-wide"
    if "bold" in design_principles:
        header_shadow_class = "shadow-2xl"
        card_shadow_class = "shadow-xl"
        section_padding_class = f"p-{golden_spacing_sm // 4}"
        border_style_class = "border-solid border-accent border-4"
        text_leading_class = "leading-tight"
        text_tracking_class = "tracking-wider"
    if "subtle" in design_principles:
        header_shadow_class = "shadow-sm"
        card_shadow_class = "shadow-sm"
        transition_class = "transition-all duration-700 ease-in-out"
        bg_pattern_class = "bg-white"
        border_style_class = "border-none"
        text_leading_class = "leading-relaxed"
        text_tracking_class = "tracking-normal"
    if "clean" in design_principles:
        card_shadow_class = "shadow-none"
        card_rounded_class = "rounded-md"
        bg_pattern_class = "bg-white"
        border_style_class = "border-gray-100 border"
        text_leading_class = "leading-relaxed"
        text_tracking_class = "tracking-tight"
    if "complex" in design_principles:
        card_shadow_class = "shadow-xl"
        button_rounded_class = "rounded-lg"
        bg_pattern_class = "bg-repeat bg-center bg-gray-200"
        border_style_class = "border-solid border-gray-500 border-2"
        text_leading_class = "leading-tight"
        text_tracking_class = "tracking-normal"


    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Theme Layout</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Apply Inter font family as a default, unless overridden by theme.css */
        body {{
            font-family: 'Inter', sans-serif;
        }}
        /* Custom CSS variables will be injected here by theme_builder.py */
        :root {{
            --primary-color: #1A73E8; /* Placeholder, will be replaced by theme_builder */
            --secondary-color: #F0F0F0;
            --accent-color: #EA4335;
            --font-heading: 'Inter', sans-serif; /* Placeholder */
            --font-body: 'Inter', sans-serif; /* Placeholder */

            /* Golden Ratio Spacing Units */
            --spacing-xs: {golden_spacing_xs}px;
            --spacing-sm: {golden_spacing_sm}px;
            --spacing-md: {golden_spacing_md}px;
            --spacing-lg: {golden_spacing_lg}px;
            --spacing-xl: {golden_spacing_xl}px;
            --spacing-2xl: {golden_spacing_2xl}px;
        }}

        /* Example usage of CSS variables (for demonstration) */
        .bg-primary {{ background-color: var(--primary-color); }}
        .text-accent {{ color: var(--accent-color); }}
        .font-heading {{ font-family: var(--font-heading); }}
        .font-body {{ font-family: var(--font-body); }}

        /* Inlined theme.css content from theme_builder.py */
        {theme_css_content}
    </style>
</head>
<body class="bg-gray-100 text-gray-900 min-h-screen flex flex-col antialiased {bg_pattern_class}">
    <!-- Main container for responsiveness -->
    <div class="container mx-auto {section_padding_class} flex-grow">

        <!-- Header Section -->
        <header class="bg-white {header_shadow_class} {card_rounded_class} p-4 mb-8 {transition_class}" style="padding: var(--spacing-md);">
            <div class="flex items-center justify-between">
                <h1 class="text-3xl font-bold text-primary font-heading">Your Brand</h1>
                <nav role="navigation" aria-label="Main navigation">
                    <ul class="flex space-x-4">
                        <li><a href="#" class="text-gray-700 hover:text-primary font-body {transition_class}">Home</a></li>
                        <li><a href="#" class="text-gray-700 hover:text-primary font-body {transition_class}">About</a></li>
                        <li><a href="#" class="text-gray-700 hover:text-primary font-body {transition_class}">Services</a></li>
                        <li><a href="#" class="text-gray-700 hover:text-primary font-body {transition_class}">Contact</a></li>
                    </ul>
                </nav>
            </div>
        </header>

        <!-- Hero Section -->
        <section class="bg-primary text-white {card_rounded_class} p-8 mb-8 flex flex-col items-center justify-center text-center {transition_class}"
                   style="min-height: 400px; padding: var(--spacing-xl);">
            <h2 class="text-5xl font-extrabold mb-4 font-heading {text_leading_class} {text_tracking_class}">
                Captivating Themes from Your Images
            </h2>
            <p class="text-xl mb-6 max-w-2xl font-body {text_leading_class} {text_tracking_class}">
                Automatically generate stunning web themes, tailored to your visual content and brand identity.
            </p>
            <button class="bg-accent text-white px-8 py-3 {button_rounded_class} text-lg font-semibold hover:bg-opacity-90 {transition_class}">
                Get Started
            </button>
        </section>

        <!-- Dynamic Content Section based on layout_style and analysis -->
        <main role="main" class="grid gap-8">
    """

    if layout_style == "minimal":
        grid_cols_class = "md:grid-cols-2 lg:grid-cols-3"
        if avg_h_symmetry > 0.8 and avg_v_symmetry > 0.8 and avg_visual_balance > 0.8:
            grid_cols_class = "md:grid-cols-1 lg:grid-cols-2"
        
        html_content += f"""
            <section class="grid grid-cols-1 {grid_cols_class} gap-{golden_spacing_lg // 4}" style="padding: var(--spacing-lg);">
                <div class="bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-6 {transition_class}" style="padding: var(--spacing-md);">
                    <h3 class="text-2xl font-bold text-gray-800 mb-2 font-heading {text_leading_class} {text_tracking_class}">Minimal Feature 1: Clean Design</h3>
                    <p class="text-gray-600 font-body {text_leading_class} {text_tracking_class}">
                        This section emphasizes clarity and simplicity. Content is presented with generous spacing,
                        allowing elements to breathe and focus on essential information.
                        (Whitespace: {avg_whitespace*100:.1f}%, Balance: {avg_visual_balance:.2f})
                    </p>
                    <!-- Accessibility hint: Consider adding aria-label to interactive elements within this card -->
                </div>
                <div class="bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-6 {transition_class}" style="padding: var(--spacing-md);">
                    <h3 class="text-2xl font-bold text-gray-800 mb-2 font-heading {text_leading_class} {text_tracking_class}">Minimal Feature 2: Subtle Elegance</h3>
                    <p class="text-gray-600 font-body {text_leading_class} {text_tracking_class}">
                        Clean lines and uncluttered design ensure a premium feel. The golden ratio guides
                        the visual weight distribution for balanced aesthetics.
                        (Fractal Dim: {avg_fractal_dimension:.2f}, Entropy: {avg_entropy:.2f})
                    </p>
                </div>
                <div class="bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-6 {transition_class}" style="padding: var(--spacing-md);">
                    <h3 class="text-2xl font-bold text-gray-800 mb-2 font-heading {text_leading_class} {text_tracking_class}">Minimal Feature 3: Focused Content</h3>
                    <p class="text-gray-600 font-body {text_leading_class} {text_tracking_class}">
                        Essential elements are highlighted, reducing cognitive load for the user.
                        This layout is ideal for elegant and focused presentations.
                        (Aesthetic Score: {avg_aesthetic_score}/10)
                    </p>
                </div>
            </section>
            <section class="grid grid-cols-1 lg:grid-cols-{(1 + GOLDEN_RATIO)} gap-{golden_spacing_md // 4}" style="grid-template-columns: {GOLDEN_RATIO}fr 1fr; padding: var(--spacing-lg);">
                <div class="bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-8 {transition_class}">
                    <h3 class="text-3xl font-bold mb-4 font-heading {text_leading_class} {text_tracking_class}">Main Content Area: Detailed Information</h3>
                    <p class="text-gray-700 font-body {text_leading_class} {text_tracking_class}">
                        This primary content block occupies a larger proportion, adhering to the golden ratio for visual hierarchy.
                        It's designed for detailed information or a prominent call to action.
                    </p>
                    <p class="text-gray-700 mt-4 font-body {text_leading_class} {text_tracking_class}">
                        The use of `grid-template-columns: {GOLDEN_RATIO}fr 1fr;` is a direct application of the Golden Ratio
                        to define the relative widths of columns.
                    </p>
                </div>
                <div class="bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-6 {transition_class}">
                    <h3 class="text-2xl font-bold mb-4 font-heading {text_leading_class} {text_tracking_class}">Sidebar: Quick Links</h3>
                    <p class="text-gray-600 font-body {text_leading_class} {text_tracking_class}">
                        A smaller, complementary section for navigation, related links, or secondary information.
                        Its size is proportionally balanced with the main content.
                    </p>
                    <!-- Accessibility hint: Ensure navigation links are clearly labeled -->
                </div>
            </section>
        """
    elif layout_style == "dense":
        grid_cols_class = "md:grid-cols-2 lg:grid-cols-4"
        if avg_entropy > 5.0:
            grid_cols_class = "md:grid-cols-3 lg:grid-cols-5"

        html_content += f"""
            <section class="grid grid-cols-1 {grid_cols_class} gap-{golden_spacing_sm // 4}" style="padding: var(--spacing-md);">
                {"".join([f'''
                <div class="bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-4 {transition_class}" style="padding: var(--spacing-sm);">
                    <h3 class="text-xl font-semibold text-gray-800 mb-1 font-heading {text_leading_class} {text_tracking_class}">Dashboard Widget {i+1}</h3>
                    <p class="text-gray-600 text-sm font-body {text_leading_class} {text_tracking_class}">
                        This layout maximizes information density, ideal for dashboards or content-heavy sites.
                        Smaller spacing units are used to keep elements close.
                        (Entropy: {avg_entropy:.2f}, Whitespace: {avg_whitespace*100:.1f}%)
                    </p>
                    <!-- Accessibility hint: For data-heavy widgets, consider ARIA table roles or descriptive labels -->
                </div>
                ''' for i in range(8)])}
            </section>
            <section class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-{golden_spacing_xs // 4}" style="padding: var(--spacing-sm);">
                {"".join([f'''
                <div class="bg-gray-50 {card_rounded_class} {border_style_class} p-3 text-center text-gray-700 text-sm font-body {transition_class}">
                    Data Point {i+1}
                </div>
                ''' for i in range(10)])}
            </section>
        """
    elif layout_style == "creative":
        col_span_main = "md:col-span-2"
        col_span_side = "md:col-span-1"
        if avg_h_symmetry < 0.6 or avg_v_symmetry < 0.6 or "dynamic" in inferred_mood_tags:
            col_span_main = "md:col-span-3 lg:col-span-2"
            col_span_side = "md:col-span-1 lg:col-span-1"

        html_content += f"""
            <section class="grid grid-cols-1 md:grid-cols-3 gap-{golden_spacing_md // 4}" style="padding: var(--spacing-xl);">
                <div class="{col_span_main} bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-8 {transition_class}" style="padding: var(--spacing-lg);">
                    <h3 class="text-4xl font-bold text-gray-800 mb-4 font-heading {text_leading_class} {text_tracking_class}">Creative Showcase: Visual Storytelling</h3>
                    <p class="text-gray-700 text-lg mb-4 font-body {text_leading_class} {text_tracking_class}">
                        This section embraces asymmetry and dynamic visual flow. It might highlight an image
                        with an aspect ratio of {image_analysis_results[0].get('aspect_ratio', 'N/A')} in a prominent, non-standard way.
                    </p>
                    <p class="text-gray-700 text-lg font-body {text_leading_class} {text_tracking_class}">
                        The layout adapts to inferred mood, for example, a '{", ".join(inferred_mood_tags) if inferred_mood_tags else "neutral"}' mood might lead to
                        more fluid and less rigid structures, potentially incorporating more whitespace
                        ({avg_whitespace*100:.1f}%) if the image analysis suggests it.
                        (Fractal Dim: {avg_fractal_dimension:.2f}, Aesthetic Score: {avg_aesthetic_score}/10)
                    </p>
                    <!-- Accessibility hint: For complex layouts, ensure clear tab order and focus management -->
                </div>
                <div class="bg-primary text-white {card_rounded_class} {card_shadow_class} {border_style_class} p-6 flex flex-col justify-between {transition_class}" style="padding: var(--spacing-md);">
                    <div>
                        <h3 class="text-3xl font-bold mb-2 font-heading {text_leading_class} {text_tracking_class}">Unique Element: Call to Action</h3>
                        <p class="text-white text-md font-body {text_leading_class} {text_tracking_class}">
                            A contrasting block designed to draw attention, perhaps for a call to action or a key statistic.
                        </p>
                    </div>
                    <button class="bg-white text-primary px-6 py-2 {button_rounded_class} font-semibold hover:bg-gray-200 {transition_class} mt-4">
                        Discover More
                    </button>
                </div>
            </section>
            <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-{golden_spacing_md // 4} mt-8" style="padding: var(--spacing-lg);">
                <div class="bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-6 md:col-span-1 {transition_class}">
                    <h4 class="text-2xl font-bold mb-2 font-heading {text_leading_class} {text_tracking_class}">Staggered Card 1: Image Gallery</h4>
                    <p class="text-gray-600 font-body {text_leading_class} {text_tracking_class}">Content for card 1. (Symmetry H: {avg_h_symmetry:.2f})</p>
                </div>
                <div class="bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-6 md:col-span-1 lg:col-start-2 lg:row-start-1 {transition_class}">
                    <h4 class="text-2xl font-bold mb-2 font-heading {text_leading_class} {text_tracking_class}">Staggered Card 2: Testimonial</h4>
                    <p class="text-gray-600 font-body {text_leading_class} {text_tracking_class}">Content for card 2, possibly taller. (Symmetry V: {avg_v_symmetry:.2f})</p>
                </div>
                <div class="bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-6 md:col-span-1 lg:col-start-3 lg:row-start-1 {transition_class}">
                    <h4 class="text-2xl font-bold mb-2 font-heading {text_leading_class} {text_tracking_class}">Staggered Card 3: Pricing Table</h4>
                    <p class="text-gray-600 font-body {text_leading_class} {text_tracking_class}">Content for card 3. (Balance: {avg_visual_balance:.2f})</p>
                </div>
            </section>
        """
    else:
        html_content += f"""
            <section class="grid grid-cols-1 md:grid-cols-2 gap-{golden_spacing_md // 4}" style="padding: var(--spacing-md);">
                <div class="bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-6 {transition_class}">
                    <h3 class="text-2xl font-bold text-gray-800 mb-2 font-heading {text_leading_class} {text_tracking_class}">Default Feature 1: General Information</h3>
                    <p class="text-gray-600 font-body {text_leading_class} {text_tracking_class}">
                        This is a standard two-column layout, providing a balanced presentation for general content.
                        (Entropy: {avg_entropy:.2f}, Fractal Dim: {avg_fractal_dimension:.2f})
                    </p>
                </div>
                <div class="bg-white {card_rounded_class} {card_shadow_class} {border_style_class} p-6 {transition_class}">
                    <h3 class="text-2xl font-bold text-gray-800 mb-2 font-heading {text_leading_class} {text_tracking_class}">Default Feature 2: Key Benefits</h3>
                    <p class="text-gray-600 font-body {text_leading_class} {text_tracking_class}">
                        It's versatile and can be used for various types of information, ensuring readability.
                        (Aesthetic Score: {avg_aesthetic_score}/10)
                    </p>
                </div>
            </section>
        """

    html_content += f"""
        </main>

        <!-- Footer Section -->
        <footer role="contentinfo" class="bg-gray-800 text-white {card_rounded_class} p-6 mt-8 text-center {transition_class}" style="padding: var(--spacing-md);">
            <p class="text-sm font-body {text_leading_class} {text_tracking_class}">&copy; {datetime.now().year} Smart Theming Engine. All rights reserved.</p>
        </footer>

    </div>
</body>
</html>
    """
    
    # Save the generated HTML to a file
    themed_layout_path = os.path.join(output_dir, "themed-layout.html")
    with open(themed_layout_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML layout saved to: {themed_layout_path}")

    return html_content, active_brand_guidelines # Return both html_content and active_brand_guidelines

if __name__ == "__main__":
    print("--- Testing Layout Generator ---")

    # Create a dummy output directory for testing
    test_output_dir = "outputs/layout_test_output"
    os.makedirs(test_output_dir, exist_ok=True)

    # Dummy image analysis results (mimicking actual output from advanced image_analyzer)
    dummy_image_analysis_minimal_calm = {
        "symmetry": {"horizontal": 0.95, "vertical": 0.95},
        "whitespace_percentage": 85.0,
        "aspect_ratio": 1.5,
        "golden_ratio_aspect_match": False,
        "fractal_dimension": 1.1,
        "entropy": 2.0,
        "visual_balance_score": 0.98,
        "typography_inference": "light, geometric",
        "mood_emotion": "calm, minimalist, balanced",
        "aesthetic_neural_score": {"score": 9, "explanation": "Very clean and balanced."}
    }
    dummy_image_analysis_dense_vibrant = {
        "symmetry": {"horizontal": 0.6, "vertical": 0.5},
        "whitespace_percentage": 25.0,
        "aspect_ratio": 1.33,
        "golden_ratio_aspect_match": False,
        "fractal_dimension": 1.8,
        "entropy": 7.5,
        "visual_balance_score": 0.7,
        "typography_inference": "sans-serif, bold",
        "mood_emotion": "vibrant, energetic, dense",
        "aesthetic_neural_score": {"score": 7, "explanation": "Dynamic and engaging."}
    }
    dummy_image_analysis_creative_playful = {
        "symmetry": {"horizontal": 0.4, "vertical": 0.7},
        "whitespace_percentage": 50.0,
        "aspect_ratio": 1.0,
        "golden_ratio_aspect_match": False,
        "fractal_dimension": 1.6,
        "entropy": 6.0,
        "visual_balance_score": 0.85,
        "typography_inference": "script, expressive",
        "mood_emotion": "playful, creative, dynamic",
        "aesthetic_neural_score": {"score": 8, "explanation": "Unique and artistic composition."}
    }
    dummy_image_analysis_golden_ratio = {
        "symmetry": {"horizontal": 0.9, "vertical": 0.9},
        "whitespace_percentage": 60.0,
        "aspect_ratio": 1.62,
        "golden_ratio_aspect_match": True,
        "fractal_dimension": 1.55,
        "entropy": 5.0,
        "visual_balance_score": 0.95,
        "typography_inference": "geometric",
        "mood_emotion": "balanced, professional",
        "aesthetic_neural_score": {"score": 9, "explanation": "Harmonious proportions."}
    }

    # Dummy theme.css content for inlining
    dummy_theme_css = """
    /* Dummy theme.css content for testing inlining */
    body { background-color: #f0f8ff; color: #333; }
    h1 { color: #007bff; }
    """

    # Test 1: Minimal Layout Style (influenced by calm image)
    print("\n--- Test 1: Minimal Layout (Calm Image) ---")
    html_minimal, bg_minimal = generate_layout([dummy_image_analysis_minimal_calm], {}, "minimal", test_output_dir, dummy_theme_css)
    print("Generated HTML for minimal layout (saved to outputs/layout_test_output/themed-layout.html).")

    # Test 2: Dense Layout Style (influenced by vibrant image)
    print("\n--- Test 2: Dense Layout (Vibrant Image) ---")
    html_dense, bg_dense = generate_layout([dummy_image_analysis_dense_vibrant], {}, "dense", test_output_dir, dummy_theme_css)
    print("Generated HTML for dense layout (saved to outputs/layout_test_output/themed-layout.html).")

    # Test 3: Creative Layout Style (influenced by creative image)
    print("\n--- Test 3: Creative Layout (Creative Image) ---")
    html_creative, bg_creative = generate_layout([dummy_image_analysis_creative_playful], {}, "creative", test_output_dir, dummy_theme_css)
    print("Generated HTML for creative layout (saved to outputs/layout_test_output/themed-layout.html).")

    # Test 4: Layout influenced by Brand Guidelines (minimalist preference)
    print("\n--- Test 4: Layout with Brand Guidelines (minimalist preference) ---")
    brand_guidelines_minimal = {"layoutPreference": "minimalist"}
    html_bg_minimal, bg_bg_minimal = generate_layout([dummy_image_analysis_dense_vibrant], brand_guidelines_minimal, "dense", test_output_dir, dummy_theme_css)
    print("Generated HTML for BG-influenced minimal layout (saved to outputs/layout_test_output/themed-layout.html).")

    # Test 5: Layout influenced by Golden Ratio Aspect Match
    print("\n--- Test 5: Layout with Golden Ratio Aspect Match ---")
    html_golden, bg_golden = generate_layout([dummy_image_analysis_golden_ratio], {}, "minimal", test_output_dir, dummy_theme_css)
    print("Generated HTML for Golden Ratio influenced layout (saved to outputs/layout_test_output/themed-layout.html).")

    # Test 6: Layout influenced by Brand Guidelines with "structured" principle
    print("\n--- Test 6: Layout with Brand Guidelines (structured principle) ---")
    brand_guidelines_structured = {"designPrinciples": ["structured"]}
    html_bg_structured, bg_bg_structured = generate_layout([dummy_image_analysis_minimal_calm], brand_guidelines_structured, "minimal", test_output_dir, dummy_theme_css)
    print("Generated HTML for BG-influenced structured layout (saved to outputs/layout_test_output/themed-layout.html).")

    # Test 7: Layout influenced by Brand Guidelines with "organic" principle
    print("\n--- Test 7: Layout with Brand Guidelines (organic principle) ---")
    # Corrected: Added missing closing bracket and brace
    brand_guidelines_organic = {"designPrinciples": ["organic"]}
    html_bg_organic, bg_bg_organic = generate_layout([dummy_image_analysis_creative_playful], brand_guidelines_organic, "creative", test_output_dir, dummy_theme_css)
    print("Generated HTML for BG-influenced organic layout (saved to outputs/layout_test_output/themed-layout.html).")

    # Test 8: Layout with NO Brand Guidelines (should infer from image analysis - e.g., calm image)
    print("\n--- Test 8: Layout with NO Brand Guidelines (inferred from calm image) ---")
    html_inferred_calm, bg_inferred_calm = generate_layout([dummy_image_analysis_minimal_calm], {}, "minimal", test_output_dir, dummy_theme_css)
    print("Generated HTML for inferred (calm) layout (saved to outputs/layout_test_output/themed-layout.html).")

    # Test 9: Layout with NO Brand Guidelines (should infer from image analysis - e.g., vibrant image)
    print("\n--- Test 9: Layout with NO Brand Guidelines (inferred from vibrant image) ---")
    html_inferred_vibrant, bg_inferred_vibrant = generate_layout([dummy_image_analysis_dense_vibrant], {}, "dense", test_output_dir, dummy_theme_css)
    print("Generated HTML for inferred (vibrant) layout (saved to outputs/layout_test_output/themed-layout.html).")

    print("\nCheck the 'outputs/layout_test_output/' directory for the generated HTML files and observe the differences.")
