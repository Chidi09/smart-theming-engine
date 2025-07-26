import math
import numpy as np # For aggregation

# Define the Golden Ratio
GOLDEN_RATIO = 1.61803398875

# Curated list of harmonious Google Font pairings
# Each tuple contains (heading_font, body_font, mood_tags, style_tags, complexity_score, readability_score)
# complexity_score: 0 (simple) to 1 (complex) - reflects visual busyness/detail of the font
# readability_score: 0 (low) to 1 (high) - reflects how easy it is to read, especially for body text
FONT_PAIRINGS = [
    ("Roboto", "Open Sans", ["modern", "professional", "calm", "balanced", "clean", "structured", "subtle"], ["sans-serif", "light", "geometric", "clean"], 0.2, 0.9),
    ("Playfair Display", "Lora", ["elegant", "calm", "professional", "balanced", "subtle", "structured"], ["serif", "light", "classic"], 0.4, 0.8),
    ("Montserrat", "Lato", ["vibrant", "modern", "playful", "energetic", "dynamic", "bold", "complex"], ["sans-serif", "bold", "geometric", "display"], 0.6, 0.7),
    ("Oswald", "Merriweather", ["bold", "professional", "modern", "dense", "structured", "complex"], ["sans-serif", "serif", "bold"], 0.7, 0.75),
    ("Pacifico", "Quicksand", ["playful", "creative", "vibrant", "dynamic", "organic", "expressive"], ["script", "sans-serif", "expressive"], 0.8, 0.6),
    ("Space Mono", "IBM Plex Sans", ["techy", "modern", "professional", "dense", "structured", "complex"], ["monospace", "sans-serif", "geometric"], 0.7, 0.8),
    ("Merriweather", "Open Sans", ["classic", "professional", "calm", "balanced", "subtle", "clean"], ["serif", "sans-serif", "light"], 0.3, 0.9),
    ("Lato", "Roboto", ["modern", "professional", "vibrant", "balanced", "clean", "structured"], ["sans-serif", "light"], 0.25, 0.85),
    ("Rubik", "Noto Sans", ["modern", "clean", "minimalist", "balanced", "structured", "subtle"], ["sans-serif", "geometric"], 0.3, 0.88),
    ("Source Code Pro", "Inter", ["techy", "modern", "professional", "dense", "structured", "complex"], ["monospace", "sans-serif"], 0.65, 0.82),
    ("Dancing Script", "Josefin Sans", ["elegant", "creative", "playful", "organic", "expressive"], ["script", "sans-serif", "expressive"], 0.9, 0.55),
    ("Bitter", "PT Sans", ["classic", "professional", "balanced", "structured"], ["serif", "sans-serif"], 0.45, 0.8),
    ("Nunito Sans", "Fira Sans", ["modern", "clean", "light", "minimalist", "subtle", "structured"], ["sans-serif", "light"], 0.2, 0.92),
    ("Anton", "Open Sans", ["bold", "energetic", "vibrant", "dynamic", "complex"], ["sans-serif", "bold", "display"], 0.85, 0.65),
    ("Comfortaa", "Muli", ["playful", "modern", "clean", "organic", "subtle"], ["sans-serif", "geometric", "light"], 0.35, 0.8),
    ("Fjalla One", "Roboto Condensed", ["bold", "dense", "energetic", "structured", "complex"], ["sans-serif", "bold"], 0.75, 0.7),
    ("Poppins", "Raleway", ["modern", "clean", "minimalist", "balanced", "structured"], ["sans-serif", "geometric", "light"], 0.3, 0.9), # Added
    ("Lora", "Noto Serif", ["elegant", "classic", "calm", "balanced", "subtle"], ["serif", "classic"], 0.4, 0.85), # Added
    ("Bebas Neue", "Montserrat", ["bold", "modern", "energetic", "dense", "complex"], ["sans-serif", "display", "bold"], 0.8, 0.68), # Added
    ("Permanent Marker", "Indie Flower", ["creative", "playful", "expressive", "organic"], ["script", "display", "expressive"], 0.95, 0.5), # Added for extreme creative
]

def suggest_fonts(image_analysis_results: list, brand_guidelines: dict) -> dict:
    """
    Suggests harmonious font pairings based on image analysis and brand guidelines.
    Applies the Golden Rule for font sizing.

    Args:
        image_analysis_results (list): List of analysis results from image_analyzer.
                                      Expected to contain 'typography_inference' and 'mood_emotion'.
        brand_guidelines (dict): Parsed brand guidelines, potentially with 'headingFont', 'bodyFont',
                                 'layoutPreference', and 'designPrinciples'.

    Returns:
        dict: A dictionary containing suggested 'heading_font', 'body_font',
              'font_size_scale', and 'typographic_recommendations'.
    """
    suggested_heading_font = "Roboto" # Default
    suggested_body_font = "Open Sans"  # Default
    base_font_size_px = 16 # A common base font size for web

    # --- Brand Guideline Revamp: Infer if not provided (similar to layout_generator) ---
    active_brand_guidelines = brand_guidelines.copy() # Work with a mutable copy

    # Aggregate image analysis results for inference
    avg_whitespace = 0.5
    avg_h_symmetry = 0.5
    avg_v_symmetry = 0.5
    avg_fractal_dimension = 1.5
    avg_entropy = 4.0
    avg_visual_balance = 0.5
    avg_aesthetic_score = 5
    
    inferred_mood_tags_from_image = set()
    inferred_typography_tags_from_image = set()

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

        for analysis in image_analysis_results:
            if "mood_emotion" in analysis and analysis["mood_emotion"] and analysis["mood_emotion"] != "neutral":
                for mood in analysis["mood_emotion"].split(','):
                    inferred_mood_tags_from_image.add(mood.strip())
            if "typography_inference" in analysis and analysis["typography_inference"] and analysis["typography_inference"] != "unknown":
                for typo in analysis["typography_inference"].split(','):
                    inferred_typography_tags_from_image.add(typo.strip())

    if not active_brand_guidelines: # If no brand guidelines are provided
        print("No brand guidelines provided to font suggester. Inferring from image analysis...")
        inferred_layout_preference = "classic" # Default
        inferred_design_principles = set()

        # Infer layoutPreference (simplified for font context)
        if "minimalist" in inferred_mood_tags_from_image or avg_whitespace > 0.75:
            inferred_layout_preference = "minimalist"
        elif "dense" in inferred_mood_tags_from_image or avg_whitespace < 0.25:
            inferred_layout_preference = "bold"
        elif "creative" in inferred_mood_tags_from_image or "dynamic" in inferred_mood_tags_from_image or avg_entropy > 6.5:
            inferred_layout_preference = "modern"
        
        active_brand_guidelines["layoutPreference"] = inferred_layout_preference
        
        # Infer designPrinciples
        if avg_h_symmetry > 0.85 and avg_v_symmetry > 0.85 and avg_visual_balance > 0.9:
            inferred_design_principles.add("structured")
        if "creative" in inferred_mood_tags_from_image or "dynamic" in inferred_mood_tags_from_image or avg_entropy > 6.0:
            inferred_design_principles.add("organic")
        if "bold" in inferred_typography_tags_from_image or avg_whitespace < 0.3:
            inferred_design_principles.add("bold")
        if "light" in inferred_typography_tags_from_image or avg_whitespace > 0.7:
            inferred_design_principles.add("subtle")
        if avg_aesthetic_score >= 8 and avg_fractal_dimension < 1.3:
            inferred_design_principles.add("clean")
        if avg_fractal_dimension > 1.7 or avg_entropy > 7.0:
            inferred_design_principles.add("complex")
        
        active_brand_guidelines["designPrinciples"] = list(inferred_design_principles)
        print(f"Inferred brand guidelines for fonts: Layout='{inferred_layout_preference}', Principles='{', '.join(inferred_design_principles)}'")

    # Extract design principles from active brand guidelines
    design_principles_from_bg = set()
    if "designPrinciples" in active_brand_guidelines and isinstance(active_brand_guidelines["designPrinciples"], list):
        for principle in active_brand_guidelines["designPrinciples"]:
            design_principles_from_bg.add(principle.strip().lower())

    # 1. Apply Brand Guidelines first (highest priority)
    # Check if brand guidelines explicitly define fonts
    brand_guideline_heading_font = active_brand_guidelines.get("headingFont")
    brand_guideline_body_font = active_brand_guidelines.get("bodyFont")

    if brand_guideline_heading_font and brand_guideline_body_font:
        print("Brand guidelines fully dictate font choices. Skipping image-based font inference.")
        # Calculate font size scale based on image analysis even if fonts are explicit
        font_size_scale = calculate_golden_ratio_font_scale(base_font_size_px, avg_whitespace, avg_aesthetic_score, avg_fractal_dimension, avg_entropy)
        typographic_recommendations = get_typographic_recommendations(
            font_suggestions={"heading_font": brand_guideline_heading_font, "body_font": brand_guideline_body_font},
            avg_whitespace=avg_whitespace,
            avg_aesthetic_score=avg_aesthetic_score,
            avg_fractal_dimension=avg_fractal_dimension,
            avg_entropy=avg_entropy,
            design_principles=design_principles_from_bg
        )
        return {
            "heading_font": brand_guideline_heading_font,
            "body_font": brand_guideline_body_font,
            "font_size_scale": font_size_scale,
            "typographic_recommendations": typographic_recommendations
        }

    # 2. Infer from Image Analysis and Brand Principles (if not dictated by brand guidelines)
    inferred_mood_tags = set()
    inferred_style_tags = set()

    for analysis in image_analysis_results:
        if "mood_emotion" in analysis and analysis["mood_emotion"] and analysis["mood_emotion"] != "neutral":
            for mood in analysis["mood_emotion"].split(','):
                inferred_mood_tags.add(mood.strip())
        if "typography_inference" in analysis and analysis["typography_inference"] and analysis["typography_inference"] != "unknown":
            for style in analysis["typography_inference"].split(','):
                inferred_style_tags.add(style.strip())

    # Add inferred design principles from brand guidelines to the mix for matching
    inferred_mood_tags.update(design_principles_from_bg)
    inferred_style_tags.update(design_principles_from_bg)


    best_match_pairing = None
    max_matches = -1

    # Find the best matching font pairing from our curated list
    for heading, body, moods_in_pairing, styles_in_pairing, pairing_complexity, pairing_readability in FONT_PAIRINGS:
        current_matches = 0
        
        # Score based on mood and style tag intersections
        current_matches += len(inferred_mood_tags.intersection(moods_in_pairing)) * 2 # Moods are important
        current_matches += len(inferred_style_tags.intersection(styles_in_pairing)) * 1.5 # Styles are also important

        # Add bonus for specific image analysis metrics alignment
        # Clean/Geometric for low complexity images
        if "clean" in inferred_style_tags and "geometric" in styles_in_pairing and avg_fractal_dimension < 1.3:
            current_matches += 2.0
        # Complex/Expressive for high entropy images
        if "complex" in inferred_style_tags and "expressive" in styles_in_pairing and avg_entropy > 6.5:
            current_matches += 2.0
        # Structured for high symmetry/balance
        if "structured" in inferred_style_tags and avg_h_symmetry > 0.7 and avg_v_symmetry > 0.7 and avg_visual_balance > 0.8:
            current_matches += 1.5
        # Organic for low symmetry/dynamic mood
        if "organic" in inferred_style_tags and (avg_h_symmetry < 0.6 or avg_v_symmetry < 0.6) and "dynamic" in inferred_mood_tags:
            current_matches += 1.5
        # High aesthetic score favors professional/balanced fonts
        if avg_aesthetic_score >= 7 and ("professional" in moods_in_pairing or "balanced" in moods_in_pairing):
            current_matches += 1.0
        # Prioritize readability for body text, especially if whitespace is low (dense content)
        if avg_whitespace < 0.4 and pairing_readability > 0.8:
            current_matches += 1.0
        # Prioritize visual complexity match
        current_matches -= abs(avg_fractal_dimension - pairing_complexity * 2) * 0.5 # Penalize mismatch
        current_matches += (1 - abs(avg_entropy - pairing_complexity * 8)) * 0.2 # Entropy aligns with complexity

        # Prioritize if the current brand guideline fonts match any in the pairing
        # (Only if brand guidelines partially dictate fonts)
        if brand_guideline_heading_font and brand_guideline_heading_font == heading:
            current_matches += 3 # Stronger match
        if brand_guideline_body_font and brand_guideline_body_font == body:
            current_matches += 3 # Stronger match

        if current_matches > max_matches:
            max_matches = current_matches
            best_match_pairing = (heading, body)
        elif current_matches == max_matches and best_match_pairing:
            # Tie-breaking: prefer pairings that are already in brand_guidelines (if any)
            # or those with higher readability for body text if avg_whitespace is low
            current_pairing_readability = next((r for h, b, m, s, c, r in FONT_PAIRINGS if h == heading and b == body), 0)[5]
            best_pairing_readability = next((r for h, b, m, s, c, r in FONT_PAIRINGS if h == best_match_pairing[0] and b == best_match_pairing[1]), 0)[5]

            if (brand_guideline_heading_font and brand_guideline_heading_font == heading) or \
               (brand_guideline_body_font and brand_guideline_body_font == body):
                best_match_pairing = (heading, body)
            elif avg_whitespace < 0.4 and current_pairing_readability > best_pairing_readability:
                best_match_pairing = (heading, body)


    if best_match_pairing:
        if not brand_guideline_heading_font: # Only update if not overridden by brand guidelines
            suggested_heading_font = best_match_pairing[0]
        if not brand_guideline_body_font: # Only update if not overridden by brand guidelines
            suggested_body_font = best_match_pairing[1]
        print(f"Inferred font pairing from image analysis and brand principles: Heading='{suggested_heading_font}', Body='{suggested_body_font}'")
    else:
        print("No strong font pairing inferred. Using defaults.")


    # 3. Apply Golden Rule for Font Sizing
    # Adjust base font size based on whitespace, aesthetic score, fractal dimension, and entropy
    # More whitespace or higher aesthetic score could mean slightly larger, more comfortable text
    base_font_size_px = 16 + (avg_whitespace * 6) + (avg_aesthetic_score / 10 * 4) # Range from 16 to 26px

    # Adjust base font size based on complexity/density:
    # Simpler images (low fractal dim/entropy) might allow slightly larger text for elegance
    if avg_fractal_dimension < 1.3 or avg_entropy < 3.0:
        base_font_size_px *= 1.05 # Slightly larger
    # Complex/dense images might benefit from slightly smaller text for readability
    elif avg_fractal_dimension > 1.7 or avg_entropy > 6.5:
        base_font_size_px *= 0.95 # Slightly smaller

    font_size_scale = calculate_golden_ratio_font_scale(base_font_size_px, avg_whitespace, avg_aesthetic_score, avg_fractal_dimension, avg_entropy)

    # 4. Micro-Typographic Recommendations
    typographic_recommendations = get_typographic_recommendations(
        font_suggestions={"heading_font": suggested_heading_font, "body_font": suggested_body_font},
        avg_whitespace=avg_whitespace,
        avg_aesthetic_score=avg_aesthetic_score,
        avg_fractal_dimension=avg_fractal_dimension,
        avg_entropy=avg_entropy,
        design_principles=design_principles_from_bg
    )

    return {
        "heading_font": suggested_heading_font,
        "body_font": suggested_body_font,
        "font_size_scale": font_size_scale,
        "typographic_recommendations": typographic_recommendations
    }

def calculate_golden_ratio_font_scale(base_size: int = 16, avg_whitespace: float = 0.5, avg_aesthetic_score: float = 5, avg_fractal_dimension: float = 1.5, avg_entropy: float = 4.0) -> dict:
    """
    Calculates a harmonious font size scale based on the Golden Ratio.
    Provides sizes for heading levels and body text.
    Adjusts slightly based on whitespace, aesthetic score, fractal dimension, and entropy
    for better readability/polish.

    Args:
        base_size (int): The base font size in pixels (e.g., for body text).
        avg_whitespace (float): Aggregated whitespace percentage (0-1).
        avg_aesthetic_score (float): Aggregated aesthetic score (1-10).
        avg_fractal_dimension (float): Aggregated fractal dimension.
        avg_entropy (float): Aggregated image entropy.

    Returns:
        dict: A dictionary with font sizes for H1-H6, body, and small text.
    """
    # Subtle adjustment to the golden ratio multiplier based on aesthetic score and complexity
    adjusted_golden_ratio = GOLDEN_RATIO
    if avg_aesthetic_score >= 8:
        adjusted_golden_ratio = GOLDEN_RATIO + 0.07 # More pronounced scale for high aesthetic
    elif avg_aesthetic_score <= 4:
        adjusted_golden_ratio = GOLDEN_RATIO - 0.07 # More compact scale for low aesthetic
    
    # Adjust based on whitespace: more whitespace might allow for a slightly larger scale
    adjusted_golden_ratio += (avg_whitespace * 0.03) # Small adjustment

    # Adjust based on fractal dimension and entropy for visual density
    if avg_fractal_dimension > 1.7 or avg_entropy > 6.5: # Complex/dense images
        adjusted_golden_ratio *= 0.98 # Slightly reduce scale for compactness
    elif avg_fractal_dimension < 1.3 or avg_entropy < 3.0: # Simpler images
        adjusted_golden_ratio *= 1.02 # Slightly increase scale for more visual separation

    scale = {
        "body": round(base_size),
        "small": round(base_size / adjusted_golden_ratio),
        "caption": round(base_size / (adjusted_golden_ratio ** 1.5)), # New: for very small text
        "h6": round(base_size * adjusted_golden_ratio),
        "h5": round(base_size * (adjusted_golden_ratio ** 2)),
        "h4": round(base_size * (adjusted_golden_ratio ** 3)),
        "h3": round(base_size * (adjusted_golden_ratio ** 4)),
        "h2": round(base_size * (adjusted_golden_ratio ** 5)),
        "h1": round(base_size * (adjusted_golden_ratio ** 6)),
        "display": round(base_size * (adjusted_golden_ratio ** 7)) # New: for very large display text
    }
    # Ensure all sizes are at least 1px to avoid 0
    for key in scale:
        scale[key] = max(1, scale[key])

    return scale

def get_typographic_recommendations(
    font_suggestions: dict,
    avg_whitespace: float,
    avg_aesthetic_score: float,
    avg_fractal_dimension: float,
    avg_entropy: float,
    design_principles: set
) -> dict:
    """
    Provides micro-typographic recommendations (line-height, letter-spacing)
    based on the suggested fonts, image analysis, and design principles.

    Args:
        font_suggestions (dict): Dictionary with 'heading_font' and 'body_font'.
        avg_whitespace (float): Aggregated whitespace percentage (0-1).
        avg_aesthetic_score (float): Aggregated aesthetic score (1-10).
        avg_fractal_dimension (float): Aggregated fractal dimension.
        avg_entropy (float): Aggregated image entropy.
        design_principles (set): Set of active design principles.

    Returns:
        dict: Recommendations for line-height and letter-spacing.
    """
    recommendations = {
        "line_height": "normal", # CSS 'normal' is usually 1.2
        "letter_spacing": "normal" # CSS 'normal' is usually 0
    }

    # Line-height adjustments
    # More whitespace or higher aesthetic score -> more relaxed line-height
    if avg_whitespace > 0.6 or avg_aesthetic_score >= 8 or "minimalist" in design_principles or "clean" in design_principles:
        recommendations["line_height"] = "relaxed" # e.g., 1.6 - 1.8
    # Dense content or complex images -> tighter line-height for compactness
    elif avg_whitespace < 0.4 or avg_fractal_dimension > 1.7 or avg_entropy > 6.5 or "dense" in design_principles or "complex" in design_principles:
        recommendations["line_height"] = "tight" # e.g., 1.2 - 1.4
    # Default for balanced/professional
    elif "professional" in design_principles or "balanced" in design_principles:
        recommendations["line_height"] = "normal" # e.g., 1.4 - 1.6

    # Letter-spacing adjustments
    # Display fonts or bold/expressive moods -> wider letter-spacing
    if "display" in font_suggestions["heading_font"].lower() or "bold" in design_principles or "expressive" in design_principles or "vibrant" in design_principles:
        recommendations["letter_spacing"] = "wide" # e.g., 0.05em - 0.1em
    # Light/geometric fonts or minimalist/clean moods -> tighter letter-spacing
    elif "light" in design_principles or "geometric" in design_principles or "minimalist" in design_principles or "clean" in design_principles:
        recommendations["letter_spacing"] = "tight" # e.g., -0.02em - 0.02em
    # Script fonts -> often tighter or normal depending on flow
    elif "script" in font_suggestions["heading_font"].lower() or "script" in font_suggestions["body_font"].lower():
        recommendations["letter_spacing"] = "normal"
    # Default for general body text
    else:
        recommendations["letter_spacing"] = "normal"

    return recommendations


if __name__ == "__main__":
    print("--- Testing Font Suggester (Peak Tech) ---")

    # Dummy image analysis results (mimicking actual output from advanced image_analyzer)
    dummy_image_analysis_minimal_calm = {
        "symmetry": {"horizontal": 0.95, "vertical": 0.95}, # High symmetry
        "whitespace_percentage": 85.0, # High whitespace
        "aspect_ratio": 1.5,
        "golden_ratio_aspect_match": False,
        "fractal_dimension": 1.1, # Low complexity (simple image)
        "entropy": 2.0, # Low randomness
        "visual_balance_score": 0.98, # High balance
        "typography_inference": "light, geometric",
        "mood_emotion": "calm, minimalist, balanced",
        "aesthetic_neural_score": {"score": 9, "explanation": "Very clean and balanced."}
    }
    dummy_image_analysis_dense_vibrant = {
        "symmetry": {"horizontal": 0.6, "vertical": 0.5}, # Lower symmetry
        "whitespace_percentage": 25.0, # Low whitespace
        "aspect_ratio": 1.33,
        "golden_ratio_aspect_match": False,
        "fractal_dimension": 1.8, # High complexity (busy image)
        "entropy": 7.5, # High randomness
        "visual_balance_score": 0.7, # Moderate balance
        "typography_inference": "sans-serif, bold",
        "mood_emotion": "vibrant, energetic, dense",
        "aesthetic_neural_score": {"score": 7, "explanation": "Dynamic and engaging."}
    }
    dummy_image_analysis_creative_playful = {
        "symmetry": {"horizontal": 0.4, "vertical": 0.7}, # Asymmetric
        "whitespace_percentage": 50.0, # Medium whitespace
        "aspect_ratio": 1.0, # Square
        "golden_ratio_aspect_match": False,
        "fractal_dimension": 1.6, # Medium-high complexity
        "entropy": 6.0, # Medium randomness
        "visual_balance_score": 0.85, # Good balance despite asymmetry
        "typography_inference": "script, expressive",
        "mood_emotion": "playful, creative, dynamic",
        "aesthetic_neural_score": {"score": 8, "explanation": "Unique and artistic composition."}
    }
    dummy_image_analysis_golden_ratio = {
        "symmetry": {"horizontal": 0.9, "vertical": 0.9},
        "whitespace_percentage": 60.0,
        "aspect_ratio": 1.62, # Close to golden ratio
        "golden_ratio_aspect_match": True,
        "fractal_dimension": 1.55,
        "entropy": 5.0,
        "visual_balance_score": 0.95,
        "typography_inference": "geometric",
        "mood_emotion": "balanced, professional",
        "aesthetic_neural_score": {"score": 9, "explanation": "Harmonious proportions."}
    }


    # Test 1: No brand guidelines, minimal/calm image -> should infer minimal/clean fonts
    print("\n--- Test 1: No Brand Guidelines, Minimal/Calm Image ---")
    suggested_fonts_1 = suggest_fonts([dummy_image_analysis_minimal_calm], {})
    print("Suggested Fonts:", suggested_fonts_1)

    # Test 2: No brand guidelines, dense/vibrant image -> should infer bold/complex fonts
    print("\n--- Test 2: No Brand Guidelines, Dense/Vibrant Image ---")
    suggested_fonts_2 = suggest_fonts([dummy_image_analysis_dense_vibrant], {})
    print("Suggested Fonts:", suggested_fonts_2)

    # Test 3: With brand guidelines (explicit fonts)
    print("\n--- Test 3: With Explicit Brand Guidelines ---")
    explicit_bg = {"headingFont": "Georgia", "bodyFont": "Verdana"}
    suggested_fonts_3 = suggest_fonts([dummy_image_analysis_minimal_calm], explicit_bg)
    print("Suggested Fonts (Explicit BG):", suggested_fonts_3)

    # Test 4: With brand guidelines (designPrinciples: structured)
    print("\n--- Test 4: With Brand Guidelines (Design Principles: structured) ---")
    structured_bg = {"designPrinciples": ["structured"]}
    suggested_fonts_4 = suggest_fonts([dummy_image_analysis_dense_vibrant], structured_bg)
    print("Suggested Fonts (Structured BG):", suggested_fonts_4)

    # Test 5: With brand guidelines (designPrinciples: organic)
    print("\n--- Test 5: With Brand Guidelines (Design Principles: organic) ---")
    organic_bg = {"designPrinciples": ["organic"]}
    suggested_fonts_5 = suggest_fonts([dummy_image_analysis_creative_playful], organic_bg)
    print("Suggested Fonts (Organic BG):", suggested_fonts_5)

    # Test 6: Empty image analysis (should use defaults and base font size)
    print("\n--- Test 6: Empty Image Analysis ---")
    suggested_fonts_6 = suggest_fonts([], {})
    print("Suggested Fonts (Empty Analysis):", suggested_fonts_6)

    # Test 7: Golden Ratio Scale adjustment check (high aesthetic, high whitespace)
    print("\n--- Test 7: Golden Ratio Scale (High Aesthetic, High Whitespace) ---")
    scale_high_aesthetic = calculate_golden_ratio_font_scale(16, 0.9, 9, 1.2, 2.5)
    print("Golden Ratio Font Scale (High Aesthetic):", scale_high_aesthetic)

    # Test 8: Golden Ratio Scale adjustment check (low aesthetic, low whitespace)
    print("\n--- Test 8: Golden Ratio Scale (Low Aesthetic, Low Whitespace) ---")
    scale_low_aesthetic = calculate_golden_ratio_font_scale(16, 0.1, 3, 1.9, 7.0)
    print("Golden Ratio Font Scale (Low Aesthetic):", scale_low_aesthetic)

    # Test 9: Check typographic recommendations for a clean/minimalist scenario
    print("\n--- Test 9: Typographic Recommendations (Clean/Minimalist) ---")
    recs_clean = get_typographic_recommendations(
        {"heading_font": "Roboto", "body_font": "Open Sans"},
        avg_whitespace=0.8, avg_aesthetic_score=9, avg_fractal_dimension=1.1, avg_entropy=2.0,
        design_principles={"clean", "minimalist"}
    )
    print("Typographic Recommendations (Clean):", recs_clean)

    # Test 10: Check typographic recommendations for a dense/complex scenario
    print("\n--- Test 10: Typographic Recommendations (Dense/Complex) ---")
    recs_dense = get_typographic_recommendations(
        {"heading_font": "Oswald", "body_font": "Merriweather"},
        avg_whitespace=0.2, avg_aesthetic_score=6, avg_fractal_dimension=1.9, avg_entropy=7.8,
        design_principles={"dense", "complex"}
    )
    print("Typographic Recommendations (Dense):", recs_dense)
