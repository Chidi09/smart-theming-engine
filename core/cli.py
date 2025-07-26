import argparse
import os
import sys
from datetime import datetime

# Add the project root to sys.path to allow importing modules from 'core'
# This is necessary when running the script directly from the project root (e.g., python core/cli.py)
# If running as a module (e.g., python -m core.cli), this might not be strictly needed,
# but it provides robustness.
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import all necessary modules
from core.palette_extractor import extract_palette
from core.image_analyzer import analyze_image
from core.brand_guideline_parser import parse_brand_guidelines
from core.font_suggester import suggest_fonts
from core.layout_generator import generate_layout
from core.theme_builder import build_theme_files
from core.js_component_suggester import suggest_js_components

def main():
    """
    Main function to parse command-line arguments for the Smart Theming Engine.
    This serves as the entry point for the CLI.
    """
    parser = argparse.ArgumentParser(
        description="Smart Theming Engine: Automate and intelligently generate web themes from input images."
    )

    # Required argument: input image(s)
    parser.add_argument(
        "input_images",
        nargs="+",  # Allows one or more image paths
        help="Path(s) to input image(s) for theme generation."
    )

    # New Optional Flags
    parser.add_argument(
        "--mode",
        choices=["light", "dark"],
        default="light",
        help="Biases the color palette and layout towards a light or dark theme. (default: light)"
    )
    parser.add_argument(
        "--layout-style",
        choices=["minimal", "dense", "creative"],
        default="minimal",
        help="Influences the generated HTML layout's complexity and spacing. (default: minimal)"
    )
    parser.add_argument(
        "--color-palette",
        choices=["vibrant", "muted", "pastel"],
        default="vibrant",
        help="Guides the color extraction towards specific aesthetic preferences. (default: vibrant)"
    )
    parser.add_argument(
        "--brand-guidelines",
        type=str,
        help="Specifies a path to a JSON file containing pre-defined brand colors, fonts, or other constraints."
    )
    parser.add_argument(
        "--version-output",
        action="store_true", # This flag does not require a value; its presence is enough
        help="Saves generated outputs into a timestamped directory for version control."
    )
    parser.add_argument(
        "--launch-ui",
        action="store_true", # This flag does not require a value; its presence is enough
        help="Automatically launches the interactive refinement web interface after initial generation."
    )

    args = parser.parse_args()

    # --- Print the parsed arguments ---
    print("\n--- Smart Theming Engine CLI Arguments ---")
    print(f"Input Images: {args.input_images}")
    print(f"Mode: {args.mode}")
    print(f"Layout Style: {args.layout_style}")
    print(f"Color Palette: {args.color_palette}")
    print(f"Brand Guidelines Path: {args.brand_guidelines}")
    print(f"Version Output: {args.version_output}")
    print(f"Launch UI: {args.launch_ui}")
    print("------------------------------------------\n")

    # --- Integrate Brand Guideline Parsing ---
    brand_guidelines = {}
    if args.brand_guidelines:
        print("\n--- Parsing Brand Guidelines ---")
        brand_guidelines = parse_brand_guidelines(args.brand_guidelines)
        if brand_guidelines:
            print("Parsed Brand Guidelines:")
            for key, value in brand_guidelines.items():
                print(f"  {key}: {value}")
        else:
            print("No valid brand guidelines were loaded.")
        print("------------------------------------------\n")
    else:
        print("\n--- No Brand Guidelines path provided. Skipping parsing. ---\n")


    # --- Integrate Palette Extraction ---
    print("\n--- Extracting Color Palette ---")
    palette_data = extract_palette(
        image_paths=args.input_images,
        color_palette_style=args.color_palette,
        mode=args.mode
    )

    print("Extracted Palette:")
    for key, value in palette_data["palette"].items():
        print(f"  {key.capitalize()}: {value}")

    if palette_data["accessibility_suggestions"]:
        print("\nAccessibility Suggestions:")
        for suggestion in palette_data["accessibility_suggestions"]:
            print(f"  - Issue: {suggestion['issue']}")
            print(f"    Context: {suggestion['context']}")
            print(f"    Current Ratio: {suggestion['current_ratio']}")
            print(f"    Suggestion: {suggestion['suggestion']}")
            print(f"    WCAG AA Normal Compliant: {suggestion['compliant_AA_normal']}")
    else:
        print("\nNo accessibility suggestions needed for the extracted palette (or compliance met).")
    
    # Print Color Harmony Score
    print("\nColor Harmony Score:")
    print(f"  Score: {palette_data['color_harmony_score']['score']}")
    print(f"  Explanation: {palette_data['color_harmony_score']['explanation']}")

    print("------------------------------------------\n")

    # --- Integrate Image Analysis ---
    print("\n--- Analyzing Input Images ---")
    all_image_analysis_results = []
    for img_path in args.input_images:
        print(f"\n  Analyzing: {img_path}")
        analysis_results = analyze_image(img_path)
        all_image_analysis_results.append(analysis_results)

        for key, value in analysis_results.items():
            if isinstance(value, dict):
                print(f"    {key.replace('_', ' ').title()}:")
                for sub_key, sub_value in value.items():
                    print(f"      {sub_key.replace('_', ' ').title()}: {sub_value}")
            else:
                print(f"    {key.replace('_', ' ').title()}: {value}")
    print("\n------------------------------------------\n")

    # --- Integrate Font Suggestion ---
    print("\n--- Suggesting Fonts ---")
    font_suggestions = suggest_fonts(all_image_analysis_results, brand_guidelines)
    print("Suggested Heading Font:", font_suggestions["heading_font"])
    print("Suggested Body Font:", font_suggestions["body_font"])
    print("Font Size Scale (px):")
    for size_level, size_value in font_suggestions["font_size_scale"].items():
        print(f"  {size_level.capitalize()}: {size_value}px")
    print("------------------------------------------\n")

    # Determine output directory
    output_dir = "outputs"
    if args.version_output:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = os.path.join(output_dir, timestamp)
    os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

    # --- Integrate Layout Generation ---
    print("\n--- Generating HTML Layout ---")
    generated_html_content = generate_layout(
        image_analysis_results=all_image_analysis_results,
        brand_guidelines=brand_guidelines,
        layout_style=args.layout_style
    )
    html_output_path = os.path.join(output_dir, "themed-layout.html")
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(generated_html_content)
    print(f"Generated HTML layout saved to: {html_output_path}")
    print("------------------------------------------\n")

    # --- Integrate Theme Building (Tailwind config, CSS variables, Integration Guide) ---
    print("\n--- Building Theme Files ---")
    generated_theme_files = build_theme_files(
        palette_data=palette_data,
        font_suggestions=font_suggestions,
        brand_guidelines=brand_guidelines,
        output_dir=output_dir
    )
    print(f"Tailwind config saved to: {generated_theme_files['tailwind_config_path']}")
    print(f"CSS variables saved to: {generated_theme_files['theme_css_path']}")
    print(f"Integration guide saved to: {generated_theme_files['integration_guide_path']}")
    print("------------------------------------------\n")

    # --- Integrate JS Component Suggestion ---
    print("\n--- Suggesting JS Components ---")
    js_component_suggestions = suggest_js_components(
        image_analysis_results=all_image_analysis_results,
        layout_style=args.layout_style
    )
    if js_component_suggestions:
        with open(os.path.join(output_dir, "suggested-components.txt"), "w", encoding="utf-8") as f:
            for suggestion in js_component_suggestions:
                f.write(f"Component: {suggestion['component']}\n")
                f.write(f"Variation: {suggestion['variation']}\n")
                f.write(f"Rationale: {suggestion['rationale']}\n")
                f.write("---\n")
        print(f"Suggested JS components saved to: {os.path.join(output_dir, 'suggested-components.txt')}")
        for suggestion in js_component_suggestions:
            print(f"  - {suggestion['component']}: {suggestion['variation']}")
    else:
        print("No specific JS component suggestions based on analysis.")
    print("------------------------------------------\n")


    # Placeholder for launching UI
    if args.launch_ui:
        print("\n--- Launching Interactive UI (Feature to be implemented) ---")
        print("Please run 'python app.py' manually once the UI module is developed.")
        print("------------------------------------------\n")


if __name__ == "__main__":
    main()
