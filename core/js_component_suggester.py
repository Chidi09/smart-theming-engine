import numpy as np # For aggregation

def suggest_js_components(image_analysis_results: list, layout_style: str, brand_guidelines: dict = None) -> list:
    """
    Suggests interactive JavaScript components based on image analysis results,
    layout style, and brand guidelines.

    Args:
        image_analysis_results (list): List of analysis results from image_analyzer.
        layout_style (str): 'minimal', 'dense', or 'creative'.
        brand_guidelines (dict): Parsed brand guidelines, potentially with 'designPrinciples'.

    Returns:
        list: A list of dictionaries, each suggesting a component, variation, and rationale.
    """
    suggestions = []

    # --- Aggregate Image Analysis Results ---
    avg_whitespace = 0.5
    avg_h_symmetry = 0.5
    avg_v_symmetry = 0.5
    avg_fractal_dimension = 1.5 # Typical mid-range for 2D
    avg_entropy = 4.0 # Mid-range for 8-bit image
    avg_visual_balance = 0.5
    avg_aesthetic_score = 5 # Default neutral
    avg_golden_ratio_match = False # True if any image matches
    
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

    # --- Brand Guideline Revamp: Infer if not provided (similar to layout_generator) ---
    active_brand_guidelines = brand_guidelines.copy() if brand_guidelines else {}

    if not active_brand_guidelines: # If no brand guidelines are provided
        print("No brand guidelines provided to JS suggester. Inferring from image analysis...")
        inferred_layout_preference = "classic" # Default
        inferred_design_principles = set()

        # Infer layoutPreference (simplified for JS context)
        if "minimalist" in inferred_mood_tags or avg_whitespace > 0.75:
            inferred_layout_preference = "minimalist"
        elif "dense" in inferred_mood_tags or avg_whitespace < 0.25:
            inferred_layout_preference = "bold"
        elif "creative" in inferred_mood_tags or "dynamic" in inferred_mood_tags or avg_entropy > 6.5:
            inferred_layout_preference = "modern"
        
        active_brand_guidelines["layoutPreference"] = inferred_layout_preference
        
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
            inferred_design_principles.add("clean")
        if avg_fractal_dimension > 1.7 or avg_entropy > 7.0:
            inferred_design_principles.add("complex")
        
        active_brand_guidelines["designPrinciples"] = list(inferred_design_principles)
        print(f"Inferred brand guidelines for JS components: Layout='{inferred_layout_preference}', Principles='{', '.join(inferred_design_principles)}'")

    # Extract design principles from active brand guidelines
    design_principles_from_bg = set()
    if "designPrinciples" in active_brand_guidelines and isinstance(active_brand_guidelines["designPrinciples"], list):
        for principle in active_brand_guidelines["designPrinciples"]:
            design_principles_from_bg.add(principle.strip().lower())

    # --- Component Suggestion Logic ---

    # General suggestions based on layout style and overall image characteristics
    if layout_style == "minimal":
        suggestions.append({
            "component": "Modal/Dialog",
            "variation": "Simple, clean overlay for calls to action or notifications.",
            "rationale": f"Minimal layouts benefit from focused interactions. High whitespace ({avg_whitespace*100:.1f}%) and aesthetic score ({avg_aesthetic_score}/10) support a polished, unobtrusive modal. (Consider using a lightweight library like 'Micromodal.js' or building with pure CSS/JS for minimal footprint.)"
        })
        if avg_h_symmetry > 0.8 and avg_v_symmetry > 0.8:
            suggestions.append({
                "component": "Accordion/Collapse",
                "variation": "Structured content expansion for FAQs or detailed sections.",
                "rationale": f"High symmetry ({avg_h_symmetry:.2f}/{avg_v_symmetry:.2f}) and a 'structured' principle (if present) align with organized content display. (Ensure ARIA attributes for accessibility.)"
            })
        if avg_aesthetic_score >= 8 and avg_fractal_dimension < 1.3: # High aesthetic, low complexity
            suggestions.append({
                "component": "Smooth Scroll/Scroll-to-Top Button",
                "variation": "Subtle, polished navigation enhancements.",
                "rationale": f"A 'clean' design principle or high aesthetic score ({avg_aesthetic_score}/10) suggests attention to detail and refined user experience. (Implement with `window.scrollTo` behavior or a small library like 'ScrollReveal.js' for subtle animations.)"
            })
    elif layout_style == "dense":
        suggestions.append({
            "component": "Tabbed Interface",
            "variation": "Compact navigation for organizing multiple content panes.",
            "rationale": f"Dense layouts require efficient space usage. Tabs help categorize information without clutter. High entropy ({avg_entropy:.2f}) suggests varied content that benefits from organization. (Consider 'headless UI' libraries like Headless UI or Radix UI for accessible, customizable tabs.)"
        })
        if avg_fractal_dimension > 1.7 or "complex" in design_principles_from_bg:
            suggestions.append({
                "component": "Interactive Chart/Graph",
                "variation": "Complex data visualization with hover effects, zooming, and drill-down capabilities (e.g., D3.js, Chart.js).",
                "rationale": f"High fractal dimension ({avg_fractal_dimension:.2f}) and 'complex' principle indicate data-rich or intricate visuals, suitable for in-depth interactive data exploration. (Prioritize performance for large datasets.)"
            })
        if avg_entropy > 6.0 or "complex" in design_principles_from_bg:
            suggestions.append({
                "component": "Advanced Search with Autocomplete/Filtering",
                "variation": "Enhanced search functionality for large datasets or content, with real-time suggestions and faceted filters.",
                "rationale": f"High entropy ({avg_entropy:.2f}) or 'complex' principle implies a need for robust content discovery and navigation within a dense information architecture. (Consider libraries like 'Algolia' or 'Fuse.js' for client-side search.)"
            })
    elif layout_style == "creative":
        suggestions.append({
            "component": "Image Carousel/Slider",
            "variation": "Full-width, auto-playing carousel with subtle transitions and parallax effects.",
            "rationale": f"Creative layouts often feature strong visuals. A dynamic carousel complements a 'creative' or 'dynamic' mood. Aesthetic score ({avg_aesthetic_score}/10) encourages smooth, high-quality animations. (Libraries like 'Swiper.js' or 'Slick Carousel' are good starting points.)"
        })
        if avg_h_symmetry < 0.6 or avg_v_symmetry < 0.6 or "organic" in design_principles_from_bg:
            suggestions.append({
                "component": "Interactive Background/Canvas Animation",
                "variation": "Subtle particle effects, generative art, or a WebGL-based 3D scene (e.g., Three.js) as a background.",
                "rationale": f"Low symmetry ({avg_h_symmetry:.2f}/{avg_v_symmetry:.2f}) or an 'organic' principle suggests a more fluid, layered, and visually engaging experience. (Be mindful of performance and accessibility for motion-sensitive users.)"
            })
        if "playful" in inferred_mood_tags or "expressive" in design_principles_from_bg:
            suggestions.append({
                "component": "Lottie Animation (JSON-based)",
                "variation": "Lightweight, scalable vector animations for micro-interactions, hero sections, or loading states.",
                "rationale": "A 'playful' mood or 'expressive' principle is perfectly matched by vector-based animations for engaging user experience. (Integrate with 'Lottie-web' library.)"
            })
        if avg_aesthetic_score >= 8 and avg_golden_ratio_match:
            suggestions.append({
                "component": "Interactive Grid with Hover Effects",
                "variation": "Image grid with subtle zoom, overlay, or reveal animations on hover, emphasizing visual harmony.",
                "rationale": f"High aesthetic score ({avg_aesthetic_score}/10) and Golden Ratio alignment suggest a focus on visual perfection, making interactive grids a compelling choice. (Consider 'Masonry.js' for layout and custom CSS/JS for effects.)"
            })

    # Cross-cutting suggestions based on aggregated metrics and design principles
    if avg_aesthetic_score >= 8 and "professional" in inferred_mood_tags:
        suggestions.append({
            "component": "Tooltip/Popover System",
            "variation": "Contextual information display on hover or click, with smooth transitions.",
            "rationale": "For a highly polished and professional site, precise and unobtrusive information delivery is key. (Libraries like 'Popper.js' or 'Tippy.js' are excellent.)"
        })
    
    if avg_visual_balance >= 0.9 and "structured" in design_principles_from_bg:
        suggestions.append({
            "component": "Sticky Navigation with Scroll-based Transformations",
            "variation": "Header that changes size, opacity, or background on scroll, maintaining a structured feel.",
            "rationale": f"High visual balance ({avg_visual_balance:.2f}) and 'structured' principle support stable yet dynamic UI elements that enhance navigation. (Implement with Intersection Observer API or scroll event listeners.)"
        })
    
    if "vibrant" in inferred_mood_tags or "energetic" in inferred_mood_tags or "bold" in design_principles_from_bg:
        suggestions.append({
            "component": "Animated Call-to-Action (CTA) Button",
            "variation": "Eye-catching button with subtle scaling, ripple effect, or gradient shift on hover/click.",
            "rationale": "A 'vibrant', 'energetic', or 'bold' aesthetic benefits from dynamic, attention-grabbing interactive elements to drive user engagement. (Pure CSS animations combined with JS event listeners.)"
        })
    
    if avg_fractal_dimension < 1.3 and "clean" in design_principles_from_bg:
        suggestions.append({
            "component": "Minimalist Image Lightbox",
            "variation": "Clean, full-screen image viewer with simple navigation and subtle fade transitions.",
            "rationale": f"Low fractal dimension ({avg_fractal_dimension:.2f}) and a 'clean' principle suggest a preference for uncluttered visuals, making a minimalist lightbox ideal for showcasing images. (Build with pure JS or a very light library.)"
        })

    if avg_entropy > 7.0 and "complex" in design_principles_from_bg:
        suggestions.append({
            "component": "Infinite Scroll/Load More Button",
            "variation": "Dynamically load content as the user scrolls or clicks a 'Load More' button, suitable for large content feeds.",
            "rationale": f"Very high entropy ({avg_entropy:.2f}) or a 'complex' principle implies a large volume of diverse content, which benefits from efficient loading strategies. (Implement with Intersection Observer API.)"
        })

    return suggestions

if __name__ == "__main__":
    print("--- Testing JS Component Suggester (Peak Tech) ---")

    # Dummy image analysis results (mimicking actual output from advanced image_analyzer)
    dummy_image_analysis_minimal_calm = {
        "symmetry": {"horizontal": 0.95, "vertical": 0.95}, # High symmetry
        "whitespace_percentage": 85.0, # High whitespace
        "aspect_ratio": 1.5,
        "golden_ratio_aspect_match": False,
        "fractal_dimension": 1.1, # Low complexity
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
        "fractal_dimension": 1.8, # High complexity
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


    # Test 1: Minimal layout, calm image (should suggest modals, accordions, smooth scroll, tooltip)
    print("\n--- Test 1: Minimal Layout, Calm Image (Inferred BG) ---")
    suggestions_1 = suggest_js_components([dummy_image_analysis_minimal_calm], "minimal", {})
    for s in suggestions_1:
        print(f"- {s['component']}: {s['variation']} (Rationale: {s['rationale']})")

    # Test 2: Dense layout, vibrant image (should suggest tabs, interactive charts, search, infinite scroll)
    print("\n--- Test 2: Dense Layout, Vibrant Image (Inferred BG) ---")
    suggestions_2 = suggest_js_components([dummy_image_analysis_dense_vibrant], "dense", {})
    for s in suggestions_2:
        print(f"- {s['component']}: {s['variation']} (Rationale: {s['rationale']})")

    # Test 3: Creative layout, playful image (should suggest carousel, parallax, lottie, interactive grid)
    print("\n--- Test 3: Creative Layout, Playful Image (Inferred BG) ---")
    suggestions_3 = suggest_js_components([dummy_image_analysis_creative_playful], "creative", {})
    for s in suggestions_3:
        print(f"- {s['component']}: {s['variation']} (Rationale: {s['rationale']})")

    # Test 4: Minimal layout, with explicit structured brand guidelines (should reinforce structured components)
    print("\n--- Test 4: Minimal Layout, Explicit Structured BG ---")
    structured_bg = {"designPrinciples": ["structured"]}
    suggestions_4 = suggest_js_components([dummy_image_analysis_minimal_calm], "minimal", structured_bg)
    for s in suggestions_4:
        print(f"- {s['component']}: {s['variation']} (Rationale: {s['rationale']})")

    # Test 5: Dense layout, with explicit complex brand guidelines (should reinforce complex components)
    print("\n--- Test 5: Dense Layout, Explicit Complex BG ---")
    complex_bg = {"designPrinciples": ["complex"]}
    suggestions_5 = suggest_js_components([dummy_image_analysis_dense_vibrant], "dense", complex_bg)
    for s in suggestions_5:
        print(f"- {s['component']}: {s['variation']} (Rationale: {s['rationale']})")

    # Test 6: Empty image analysis (should return minimal suggestions)
    print("\n--- Test 6: Empty Image Analysis ---")
    suggestions_6 = suggest_js_components([], "minimal", {})
    for s in suggestions_6:
        print(f"- {s['component']}: {s['variation']} (Rationale: {s['rationale']})")

    # Test 7: Golden Ratio matched image in creative layout (should suggest interactive grid)
    print("\n--- Test 7: Creative Layout, Golden Ratio Matched Image ---")
    suggestions_7 = suggest_js_components([dummy_image_analysis_golden_ratio], "creative", {})
    for s in suggestions_7:
        print(f"- {s['component']}: {s['variation']} (Rationale: {s['rationale']})")
