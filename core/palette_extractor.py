from PIL import Image
import colorsys
import math
import numpy as np
from sklearn.cluster import MiniBatchKMeans # Using MiniBatchKMeans for efficiency with large images

# You might need to install 'Pillow', 'numpy', and 'scikit-learn'
# pip install Pillow numpy scikit-learn

def hex_to_rgb(hex_color: str) -> tuple:
    """Converts a hex color string (e.g., '#RRGGBB') to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color: tuple) -> str:
    """Converts an RGB tuple to a hex color string."""
    return f"#{int(rgb_color[0]):02x}{int(rgb_color[1]):02x}{int(rgb_color[2]):02x}"

def get_luminance(rgb: tuple) -> float:
    """
    Calculates the relative luminance of an RGB color using WCAG 2.0 formula.
    RGB values should be between 0 and 255.
    Returns a value between 0 and 1.
    """
    R, G, B = [x / 255.0 for x in rgb] # Normalize to 0-1 range

    # Apply gamma correction
    R = R / 12.92 if R <= 0.03928 else ((R + 0.055) / 1.055) ** 2.4
    G = G / 12.92 if G <= 0.03928 else ((G + 0.055) / 1.055) ** 2.4
    B = B / 12.92 if B <= 0.03928 else ((B + 0.055) / 1.055) ** 2.4

    return 0.2126 * R + 0.7152 * G + 0.0722 * B

def get_contrast_ratio(rgb1: tuple, rgb2: tuple) -> float:
    """
    Calculates the contrast ratio between two RGB colors (0-255).
    Returns a ratio between 1 (no contrast) and 21 (max contrast).
    """
    L1 = get_luminance(rgb1)
    L2 = get_luminance(rgb2)

    # Ensure L1 is the lighter of the two for the formula
    if L2 > L1:
        L1, L2 = L2, L1

    return (L1 + 0.05) / (L2 + 0.05)

def check_wcag_compliance(contrast_ratio: float) -> dict:
    """
    Checks WCAG compliance for a given contrast ratio.
    Returns a dictionary with compliance levels (AA, AAA for normal and large text).
    """
    compliance = {
        "AA_normal_text": contrast_ratio >= 4.5,
        "AA_large_text": contrast_ratio >= 3.0,
        "AAA_normal_text": contrast_ratio >= 7.0,
        "AAA_large_text": contrast_ratio >= 4.5
    }
    return compliance

def suggest_accessible_color(original_rgb: tuple, background_rgb: tuple, target_contrast: float) -> tuple:
    """
    Suggests an adjusted color to meet a target contrast ratio against a background.
    This is a basic heuristic and might not always find the perfect color.
    It attempts to lighten/darken the original color.
    """
    original_hls = colorsys.rgb_to_hls(original_rgb[0]/255, original_rgb[1]/255, original_rgb[2]/255)
    hue, lightness, saturation = original_hls

    # Try adjusting lightness
    step = 0.05 # Small step for adjustment
    max_attempts = 20 # Limit attempts to prevent infinite loops

    current_rgb = original_rgb
    current_contrast = get_contrast_ratio(current_rgb, background_rgb)

    for _ in range(max_attempts):
        if current_contrast >= target_contrast:
            return current_rgb

        # Determine if we need to lighten or darken
        if get_luminance(current_rgb) < get_luminance(background_rgb):
            new_lightness = lightness + step
        else:
            new_lightness = lightness - step

        new_lightness = max(0.0, min(1.0, new_lightness)) # Clamp lightness between 0 and 1
        lightness = new_lightness # Update for next iteration

        adjusted_rgb_norm = colorsys.hls_to_rgb(hue, lightness, saturation)
        current_rgb = tuple(int(x * 255) for x in adjusted_rgb_norm)
        current_contrast = get_contrast_ratio(current_rgb, background_rgb)

    return current_rgb # Return best attempt

def calculate_color_harmony_score(colors_rgb: list) -> dict:
    """
    Calculates a color harmony score for a list of RGB colors.
    Scores based on common color harmony rules (monochromatic, analogous, complementary, triadic).
    Returns a score from 0-10 and an explanation.

    Args:
        colors_rgb (list): A list of RGB color tuples (0-255).

    Returns:
        dict: A dictionary with 'score' (float) and 'explanation' (str).
    """
    if not colors_rgb:
        return {"score": 0.0, "explanation": "No colors provided for harmony analysis."}
    if len(colors_rgb) == 1:
        return {"score": 7.0, "explanation": "Single color palette is inherently harmonious (monochromatic)."}

    # Convert RGB to HSL for hue analysis
    hues = []
    saturations = []
    lightnesses = []
    for r, g, b in colors_rgb:
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        hues.append(h * 360) # Convert hue to degrees (0-360)
        saturations.append(s)
        lightnesses.append(l)

    # Sort hues to make angular calculations easier
    hues.sort()

    harmony_score = 0.0
    explanation = []

    # Rule 1: Monochromatic (all hues are very close)
    if len(hues) > 1 and (max(hues) - min(hues) < 15 or (360 - (max(hues) - min(hues))) < 15):
        harmony_score += 2.0 # Base score for monochromatic
        explanation.append("Monochromatic (hues are very close).")

    # Rule 2: Analogous (hues are close on the color wheel, typically within 30-60 degrees)
    # Check if all hues are within a small angular range (e.g., 60 degrees)
    is_analogous = True
    if len(hues) > 1:
        for i in range(len(hues)):
            h1 = hues[i]
            h2 = hues[(i + 1) % len(hues)] # Wrap around for last and first hue
            angular_diff = min(abs(h1 - h2), 360 - abs(h1 - h2))
            if angular_diff > 60: # Max 60 degrees difference
                is_analogous = False
                break
        if is_analogous:
            harmony_score += 3.0 # Stronger score for analogous
            explanation.append("Analogous (hues are close on the color wheel).")

    # Rule 3: Complementary (two hues directly opposite, or close to opposite)
    if len(hues) == 2:
        diff = min(abs(hues[0] - hues[1]), 360 - abs(hues[0] - hues[1]))
        if abs(diff - 180) < 15: # Close to 180 degrees apart
            harmony_score += 4.0 # High score for complementary
            explanation.append("Complementary (two main hues are opposite).")
    elif len(hues) > 2: # Check for a dominant complementary pair
        for i in range(len(hues)):
            for j in range(i + 1, len(hues)):
                diff = min(abs(hues[i] - hues[j]), 360 - abs(hues[i] - hues[j]))
                if abs(diff - 180) < 15:
                    harmony_score += 1.5 # Smaller bonus if it's one pair in a larger set
                    explanation.append(f"Contains a complementary pair (hues {round(hues[i])}° and {round(hues[j])}°).")
                    break # Only count one pair for now

    # Rule 4: Triadic (three hues equally spaced, 120 degrees apart)
    if len(hues) >= 3:
        # Check if there are 3 dominant hues roughly 120 degrees apart
        # This is complex to do robustly with arbitrary number of colors.
        # Simple heuristic: look for 3 distinct hues that are roughly 120 degrees apart
        # For a more advanced system, you'd find the 3 most dominant hues and check their relation.
        if len(hues) == 3:
            hues_sorted = sorted(hues)
            diff1 = min(abs(hues_sorted[1] - hues_sorted[0]), 360 - abs(hues_sorted[1] - hues_sorted[0]))
            diff2 = min(abs(hues_sorted[2] - hues_sorted[1]), 360 - abs(hues_sorted[2] - hues_sorted[1]))
            diff3 = min(abs(hues_sorted[0] - hues_sorted[2]), 360 - abs(hues_sorted[0] - hues_sorted[2])) # Wrap around
            
            # Check if all are roughly 120 +/- 15 degrees
            if abs(diff1 - 120) < 15 and abs(diff2 - 120) < 15 and abs(diff3 - 120) < 15:
                harmony_score += 5.0 # Highest score for triadic
                explanation.append("Triadic (three main hues are equally spaced).")


    # Normalize score to 0-10 range (max possible score depends on rules applied)
    # A simple way is to cap and scale. Max possible score from above rules is 5 (triadic) + 4 (complementary) = 9
    # We'll cap at 10 and ensure it's not negative.
    final_score = max(0.0, min(10.0, harmony_score))
    
    if not explanation:
        explanation.append("No specific harmony pattern detected, but colors are present.")
        if len(colors_rgb) > 0: # If colors exist but no pattern, give a base score
            final_score = max(final_score, 3.0) # Base score for just having colors

    return {"score": round(final_score, 2), "explanation": ". ".join(explanation)}


def extract_palette(image_paths: list, color_palette_style: str = "vibrant", mode: str = "light") -> dict:
    """
    Extracts dominant and complementary color palettes from input images using K-means,
    performs WCAG accessibility checks, and calculates color harmony.

    Args:
        image_paths (list): List of paths to input images.
        color_palette_style (str): 'vibrant', 'muted', or 'pastel'.
        mode (str): 'light' or 'dark' theme bias.

    Returns:
        dict: A dictionary containing the extracted palette (hex codes),
              accessibility suggestions, and color harmony score.
    """
    if not image_paths:
        print("No image paths provided for palette extraction.")
        return {
            "palette": {"primary": "#FFFFFF", "secondary": "#CCCCCC", "accent": "#000000"},
            "accessibility_suggestions": [],
            "color_harmony_score": {"score": 0.0, "explanation": "No images provided for color analysis."} # Default for no images
        }

    all_pixels = []
    for img_path in image_paths:
        try:
            with Image.open(img_path).convert("RGB") as img:
                # Resize for faster processing and consistent sampling
                img.thumbnail((200, 200)) # Max 200x200 pixels
                pixels = list(img.getdata())
                all_pixels.extend(pixels)
        except FileNotFoundError:
            print(f"Warning: Image not found at {img_path}. Skipping.")
            continue
        except Exception as e:
            print(f"Error processing image {img_path}: {e}. Skipping.")
            continue

    if not all_pixels:
        print("No valid pixels extracted from images. Returning default palette.")
        return {
            "palette": {"primary": "#FFFFFF", "secondary": "#CCCCCC", "accent": "#000000"},
            "accessibility_suggestions": [],
            "color_harmony_score": {"score": 0.0, "explanation": "No valid pixels extracted for color analysis."} # Default for no pixels
        }

    # Convert pixel list to NumPy array for K-means
    pixels_np = np.array(all_pixels, dtype=np.float32) / 255.0 # Normalize to 0-1 for K-means

    # Use MiniBatchKMeans for efficiency. Determine number of clusters.
    n_clusters = 5 # Can be adjusted based on desired palette complexity
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(pixels_np)

    # Get the cluster centers (dominant colors)
    dominant_colors_norm = kmeans.cluster_centers_
    dominant_rgbs = [tuple(int(x * 255) for x in color) for color in dominant_colors_norm]

    # Sort dominant colors by their "dominance" (e.g., by the number of pixels in each cluster)
    labels = kmeans.predict(pixels_np)
    label_counts = np.bincount(labels)
    sorted_indices = np.argsort(label_counts)[::-1] # Sort in descending order of count

    # Select primary, secondary, accent based on sorted dominance
    primary_rgb = dominant_rgbs[sorted_indices[0]] if len(sorted_indices) > 0 else (255, 255, 255)
    secondary_rgb = dominant_rgbs[sorted_indices[1]] if len(sorted_indices) > 1 else (204, 204, 204)
    accent_rgb = dominant_rgbs[sorted_indices[2]] if len(sorted_indices) > 2 else (0, 0, 0)

    # Apply mode bias (more nuanced adjustment possible here)
    if mode == "dark":
        # Darken primary/secondary, lighten accent for contrast
        primary_rgb = tuple(max(0, x - 50) for x in primary_rgb)
        secondary_rgb = tuple(max(0, x - 30) for x in secondary_rgb)
        accent_rgb = tuple(min(255, x + 50) for x in accent_rgb)
    else: # light mode
        # Lighten primary/secondary, darken accent for contrast
        primary_rgb = tuple(min(255, x + 20) for x in primary_rgb)
        secondary_rgb = tuple(min(255, x + 10) for x in secondary_rgb)
        accent_rgb = tuple(max(0, x - 20) for x in accent_rgb)

    # Apply color palette style (more sophisticated logic for vibrancy, mutedness, pastel)
    if color_palette_style == "muted":
        primary_hls = colorsys.rgb_to_hls(primary_rgb[0]/255, primary_rgb[1]/255, primary_rgb[2]/255)
        secondary_hls = colorsys.rgb_to_hls(secondary_rgb[0]/255, secondary_rgb[1]/255, secondary_rgb[2]/255)
        accent_hls = colorsys.rgb_to_hls(accent_rgb[0]/255, accent_rgb[1]/255, accent_rgb[2]/255)

        primary_rgb = tuple(int(x * 255) for x in colorsys.hls_to_rgb(primary_hls[0], primary_hls[1], max(0, primary_hls[2] * 0.7)))
        secondary_rgb = tuple(int(x * 255) for x in colorsys.hls_to_rgb(secondary_hls[0], secondary_hls[1], max(0, secondary_hls[2] * 0.7)))
        accent_rgb = tuple(int(x * 255) for x in colorsys.hls_to_rgb(accent_hls[0], accent_hls[1], max(0, accent_hls[2] * 0.7)))
    elif color_palette_style == "pastel":
        primary_hls = colorsys.rgb_to_hls(primary_rgb[0]/255, primary_rgb[1]/255, primary_rgb[2]/255)
        secondary_hls = colorsys.rgb_to_hls(secondary_rgb[0]/255, secondary_rgb[1]/255, secondary_rgb[2]/255)
        accent_hls = colorsys.rgb_to_hls(accent_rgb[0]/255, accent_rgb[1]/255, accent_rgb[2]/255)

        primary_rgb = tuple(int(x * 255) for x in colorsys.hls_to_rgb(primary_hls[0], min(1, primary_hls[1] * 1.2), primary_hls[2] * 0.8))
        secondary_rgb = tuple(int(x * 255) for x in colorsys.hls_to_rgb(secondary_hls[0], min(1, secondary_hls[1] * 1.2), secondary_hls[2] * 0.8))
        accent_rgb = tuple(int(x * 255) for x in colorsys.hls_to_rgb(accent_hls[0], min(1, accent_hls[1] * 1.2), accent_hls[2] * 0.8))
    # 'vibrant' is default, no specific adjustment here for now

    extracted_palette = {
        "primary": rgb_to_hex(primary_rgb),
        "secondary": rgb_to_hex(secondary_rgb),
        "accent": rgb_to_hex(accent_rgb),
    }

    accessibility_suggestions = []

    # WCAG Accessibility Checks
    text_color_for_contrast = (0, 0, 0) if get_luminance(primary_rgb) > 0.5 else (255, 255, 255)

    contrast_primary_text = get_contrast_ratio(primary_rgb, text_color_for_contrast)
    compliance_primary = check_wcag_compliance(contrast_primary_text)
    if not compliance_primary["AA_normal_text"]:
        suggested_text_rgb = suggest_accessible_color(text_color_for_contrast, primary_rgb, 4.5)
        accessibility_suggestions.append({
            "issue": "Primary color contrast with text",
            "context": f"Primary background ({extracted_palette['primary']}) vs. text ({rgb_to_hex(text_color_for_contrast)})",
            "current_ratio": round(contrast_primary_text, 2),
            "required_AA": 4.5,
            "suggestion": f"Consider adjusting text color to {rgb_to_hex(suggested_text_rgb)} or primary background for better contrast.",
            "compliant_AA_normal": compliance_primary["AA_normal_text"]
        })

    contrast_secondary_on_primary = get_contrast_ratio(secondary_rgb, primary_rgb)
    compliance_secondary_on_primary = check_wcag_compliance(contrast_secondary_on_primary)
    if not compliance_secondary_on_primary["AA_normal_text"]:
        suggested_secondary_rgb = suggest_accessible_color(secondary_rgb, primary_rgb, 4.5)
        accessibility_suggestions.append({
            "issue": "Secondary color contrast with Primary background",
            "context": f"Secondary element ({extracted_palette['secondary']}) on Primary background ({extracted_palette['primary']})",
            "current_ratio": round(contrast_secondary_on_primary, 2),
            "required_AA": 4.5,
            "suggestion": f"Consider adjusting secondary color to {rgb_to_hex(suggested_secondary_rgb)} for better contrast.",
            "compliant_AA_normal": compliance_secondary_on_primary["AA_normal_text"]
        })

    contrast_accent_on_primary = get_contrast_ratio(accent_rgb, primary_rgb)
    compliance_accent_on_primary = check_wcag_compliance(contrast_accent_on_primary)
    if not compliance_accent_on_primary["AA_normal_text"]:
        suggested_accent_rgb = suggest_accessible_color(accent_rgb, primary_rgb, 4.5)
        accessibility_suggestions.append({
            "issue": "Accent color contrast with Primary background",
            "context": f"Accent element ({extracted_palette['accent']}) on Primary background ({extracted_palette['primary']})",
            "current_ratio": round(contrast_accent_on_primary, 2),
            "required_AA": 4.5,
            "suggestion": f"Consider adjusting accent color to {rgb_to_hex(suggested_accent_rgb)} for better contrast.",
            "compliant_AA_normal": compliance_accent_on_primary["AA_normal_text"]
        })

    # Calculate Color Harmony Score
    # Use the three main extracted colors for harmony analysis
    colors_for_harmony = [primary_rgb, secondary_rgb, accent_rgb]
    color_harmony_score = calculate_color_harmony_score(colors_for_harmony)


    # Combine palette and suggestions
    result = {
        "palette": extracted_palette,
        "accessibility_suggestions": accessibility_suggestions,
        "color_harmony_score": color_harmony_score # New field
    }

    return result

if __name__ == "__main__":
    # Example Usage (for testing this module directly)
    # You'll need to create some dummy images in the 'assets' folder for this to run.
    # e.g., a red.png, blue.png etc. or copy some actual images.
    print("--- Testing Palette Extractor ---")
    # Create dummy image files for testing
    try:
        from PIL import Image, ImageDraw
        img1 = Image.new('RGB', (60, 30), color = 'red')
        img1.save('assets/test_red.png')
        img2 = Image.new('RGB', (60, 30), color = 'blue')
        img2.save('assets/test_blue.png')
        img3 = Image.new('RGB', (60, 30), color = 'green')
        img3.save('assets/test_green.png')
        print("Dummy images 'assets/test_red.png', 'assets/test_blue.png', 'assets/test_green.png' created for testing.")

        # Create images for specific harmony tests
        # Monochromatic (shades of blue)
        img_mono = Image.new('RGB', (100, 100), color = (0, 0, 200))
        draw = ImageDraw.Draw(img_mono)
        draw.rectangle((0, 0, 50, 100), fill=(0, 0, 150))
        draw.rectangle((50, 0, 100, 100), fill=(0, 0, 250))
        img_mono.save('assets/test_monochromatic.png')
        print("Dummy monochromatic image 'assets/test_monochromatic.png' created.")

        # Complementary (red and green)
        img_comp = Image.new('RGB', (100, 100), color = (255, 0, 0))
        draw = ImageDraw.Draw(img_comp)
        draw.rectangle((0, 0, 50, 100), fill=(0, 255, 0))
        img_comp.save('assets/test_complementary.png')
        print("Dummy complementary image 'assets/test_complementary.png' created.")

        # Triadic (red, green, blue)
        img_triadic = Image.new('RGB', (100, 100), color = (255, 0, 0))
        draw = ImageDraw.Draw(img_triadic)
        draw.rectangle((0, 0, 33, 100), fill=(0, 255, 0))
        draw.rectangle((66, 0, 100, 100), fill=(0, 0, 255))
        img_triadic.save('assets/test_triadic.png')
        print("Dummy triadic image 'assets/test_triadic.png' created.")


    except Exception as e:
        print(f"Could not create dummy images (Pillow might not be fully installed or permissions issue): {e}")
        print("Please ensure you have Pillow installed (`pip install Pillow`) and create some images manually in the 'assets' folder to test.")

    test_image_paths = ["assets/test_red.png", "assets/test_blue.png", "assets/test_green.png"]

    print("\n--- Testing with default settings (vibrant, light) ---")
    palette_data = extract_palette(test_image_paths)
    print("Extracted Palette:", palette_data["palette"])
    print("Accessibility Suggestions:")
    for suggestion in palette_data["accessibility_suggestions"]:
        print(f"  - {suggestion['issue']}: {suggestion['suggestion']} (Current ratio: {suggestion['current_ratio']})")
    print("Color Harmony Score:", palette_data["color_harmony_score"])

    print("\n--- Testing with dark mode ---")
    palette_data_dark = extract_palette(test_image_paths, mode="dark")
    print("Extracted Palette (Dark Mode):", palette_data_dark["palette"])
    print("Accessibility Suggestions (Dark Mode):")
    for suggestion in palette_data_dark["accessibility_suggestions"]:
        print(f"  - {suggestion['issue']}: {suggestion['suggestion']} (Current ratio: {suggestion['current_ratio']})")
    print("Color Harmony Score (Dark Mode):", palette_data_dark["color_harmony_score"])

    print("\n--- Testing with pastel color palette ---")
    palette_data_pastel = extract_palette(test_image_paths, color_palette_style="pastel")
    print("Extracted Palette (Pastel):", palette_data_pastel["palette"])
    print("Accessibility Suggestions (Pastel):")
    for suggestion in palette_data_pastel["accessibility_suggestions"]:
        print(f"  - {suggestion['issue']}: {suggestion['suggestion']} (Current ratio: {suggestion['current_ratio']})")
    print("Color Harmony Score (Pastel):", palette_data_pastel["color_harmony_score"])

    print("\n--- Testing with monochromatic image ---")
    palette_data_mono = extract_palette(["assets/test_monochromatic.png"])
    print("Extracted Palette (Monochromatic):", palette_data_mono["palette"])
    print("Color Harmony Score (Monochromatic):", palette_data_mono["color_harmony_score"])

    print("\n--- Testing with complementary image ---")
    palette_data_comp = extract_palette(["assets/test_complementary.png"])
    print("Extracted Palette (Complementary):", palette_data_comp["palette"])
    print("Color Harmony Score (Complementary):", palette_data_comp["color_harmony_score"])

    print("\n--- Testing with triadic image ---")
    palette_data_triadic = extract_palette(["assets/test_triadic.png"])
    print("Extracted Palette (Triadic):", palette_data_triadic["palette"])
    print("Color Harmony Score (Triadic):", palette_data_triadic["color_harmony_score"])

    print("\n--- Testing with no images ---")
    palette_data_no_images = extract_palette([])
    print("Extracted Palette (No Images):", palette_data_no_images["palette"])
    print("Accessibility Suggestions (No Images):", palette_data_no_images["accessibility_suggestions"])
    print("Color Harmony Score (No Images):", palette_data_no_images["color_harmony_score"])
