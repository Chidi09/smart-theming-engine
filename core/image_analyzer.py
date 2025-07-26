from PIL import Image
import numpy as np
import colorsys
import math
import base64 # For encoding image to base64
import json # For parsing LLM response

# Define the Golden Ratio
GOLDEN_RATIO = 1.61803398875

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

def calculate_fractal_dimension(image_array_gray: np.ndarray, threshold: int = 128) -> float:
    """
    Calculates the fractal dimension of a binary image using the box-counting method.
    Adapted from: https://github.com/rougier/numpy-100/blob/master/100_numpy_exercises_no_solution.py
    (Exercise 94, with modifications for image input)

    Args:
        image_array_gray (np.ndarray): Grayscale image as a NumPy array (0-255).
        threshold (int): Pixels above this threshold are considered 'foreground' (1), below as 'background' (0).

    Returns:
        float: The estimated fractal dimension (between 1.0 and 2.0 for 2D images).
               Returns 0.0 if calculation fails or image is too small.
    """
    if image_array_gray.size == 0:
        return 0.0

    # Convert to binary image based on threshold
    Z = (image_array_gray < threshold).astype(int) # Consider darker pixels as "filled"

    # Only consider non-empty images
    if np.sum(Z) == 0:
        return 0.0

    # Pad the image to ensure dimensions are powers of 2 for easier box division
    p = 2**math.ceil(math.log2(max(Z.shape)))
    padded_Z = np.zeros((p, p), dtype=int)
    padded_Z[:Z.shape[0], :Z.shape[1]] = Z

    # Rescale to a square image of power-of-2 size
    def boxcount(Z, k):
        S = np.add.reduceat(
            np.add.reduceat(padded_Z, np.arange(0, Z.shape[0], k), axis=0),
            np.arange(0, Z.shape[1], k), axis=1)
        return np.sum(S > 0) # Count boxes that contain at least one '1'

    # Determine the box sizes (powers of 2)
    sizes = 2**np.arange(int(math.log2(p)), 1, -1)
    
    # Calculate N(r) for each box size r
    counts = [boxcount(padded_Z, size) for size in sizes]

    # Filter out zero counts to avoid log(0)
    valid_sizes = [s for s, c in zip(sizes, counts) if c > 0]
    valid_counts = [c for c in counts if c > 0]

    if len(valid_sizes) < 2: # Need at least two points to calculate slope
        return 0.0

    # Linear fit to log(N(r)) vs. log(1/r)
    coeffs = np.polyfit(np.log(1./np.array(valid_sizes)), np.log(np.array(valid_counts)), 1)
    return coeffs[0]

def calculate_image_entropy(image_array_gray: np.ndarray) -> float:
    """
    Calculates the Shannon entropy of a grayscale image.
    Higher entropy indicates more randomness/detail.

    Args:
        image_array_gray (np.ndarray): Grayscale image as a NumPy array (0-255).

    Returns:
        float: The entropy value. Returns 0.0 if image is empty.
    """
    if image_array_gray.size == 0:
        return 0.0

    # Calculate histogram
    hist = np.histogram(image_array_gray.flatten(), bins=256, range=[0,256])[0]
    # Normalize histogram to get probabilities
    hist = hist / hist.sum()

    # Calculate entropy: -sum(p * log2(p))
    # Avoid log(0) by filtering out zero probabilities
    hist = hist[hist > 0]
    entropy = -np.sum(hist * np.log2(hist))
    return entropy

def calculate_visual_balance_score(image_array_gray: np.ndarray) -> float:
    """
    Calculates a visual balance score based on the image's center of mass.
    A score closer to 1.0 indicates better balance (center of mass near geometric center).

    Args:
        image_array_gray (np.ndarray): Grayscale image as a NumPy array (0-255).

    Returns:
        float: A score between 0 and 1.0.
    """
    if image_array_gray.size == 0:
        return 0.0

    height, width = image_array_gray.shape
    total_luminance = np.sum(image_array_gray)

    if total_luminance == 0: # Avoid division by zero for completely black images
        return 0.0

    # Calculate weighted sum of coordinates
    x_coords = np.arange(width)
    y_coords = np.arange(height)

    # Calculate center of mass (weighted average of coordinates by pixel intensity)
    center_x = np.sum(image_array_gray * x_coords) / total_luminance
    center_y = np.sum(image_array_gray.T * y_coords) / total_luminance # Transpose for y-axis sum

    # Geometric center
    geometric_center_x = (width - 1) / 2
    geometric_center_y = (height - 1) / 2

    # Calculate distance from geometric center
    distance = math.sqrt((center_x - geometric_center_x)**2 + (center_y - geometric_center_y)**2)

    # Normalize distance to a score between 0 and 1.
    # Max possible distance is from one corner to the opposite corner.
    max_distance = math.sqrt(geometric_center_x**2 + geometric_center_y**2)
    
    if max_distance == 0: # For 1x1 images
        return 1.0

    # Invert distance to get a balance score (closer to 1 is better)
    balance_score = 1.0 - min(1.0, distance / max_distance)
    return balance_score

# Placeholder for Gemini API call - This would typically be an async function in a web frontend
# or a separate service. For this Python module, we'll simulate the call.
def get_aesthetic_score_from_gemini(image_data_base64: str, mime_type: str = "image/png") -> dict:
    """
    Simulates a call to the Gemini API to get an aesthetic score for an image.
    In a real application, this would involve an actual HTTP request.

    Args:
        image_data_base64 (str): Base64 encoded image data.
        mime_type (str): MIME type of the image (e.g., "image/png", "image/jpeg").

    Returns:
        dict: A dictionary containing the aesthetic score and explanation.
              Returns default values if the call fails or is simulated.
    """
    # --- IMPORTANT ---
    # This is a SIMULATED API call for demonstration within this Python module.
    # In a real web application (e.g., in the Streamlit frontend's JavaScript or a backend service),
    # you would make an actual fetch call to the Gemini API like this:
    #
    # let chatHistory = [];
    # chatHistory.push({ role: "user", parts: [{ text: "Analyze the aesthetic quality of this image. Provide a score from 1 to 10, where 1 is very poor and 10 is excellent, and a brief explanation in JSON format: {'score': int, 'explanation': 'str'}" }] });
    # const payload = {
    #     contents: [
    #         {
    #             role: "user",
    #             parts: [
    #                 { text: "Analyze the aesthetic quality of this image. Provide a score from 1 to 10, where 1 is very poor and 10 is excellent, and a brief explanation in JSON format: {'score': int, 'explanation': 'str'}" },
    #                 {
    #                     inlineData: {
    #                         mimeType: mime_type,
    #                         data: image_data_base64
    #                     }
    #                 }
    #             ]
    #         }
    #     ],
    #     generationConfig: {
    #         responseMimeType: "application/json",
    #         responseSchema: {
    #             type: "OBJECT",
    #             properties: {
    #                 "score": { "type": "INTEGER" },
    #                 "explanation": { "type": "STRING" }
    #             },
    #             "propertyOrdering": ["score", "explanation"]
    #         }
    #     }
    # };
    # const apiKey = ""; // Canvas will provide this at runtime
    # const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
    # const response = await fetch(apiUrl, {
    #     method: 'POST',
    #     headers: { 'Content-Type': 'application/json' },
    #     body: JSON.stringify(payload)
    # });
    # const result = await response.json();
    # if (result.candidates && result.candidates.length > 0 && result.candidates[0].content && result.candidates[0].content.parts && result.candidates[0].content.parts.length > 0) {
    #     const json_text = result.candidates[0].content.parts[0].text;
    #     return json.loads(json_text);
    # } else {
    #     return {"score": 5, "explanation": "Simulated: Could not get aesthetic score from LLM."};
    # }
    # --- END IMPORTANT ---

    # Simulate a response for demonstration purposes
    print("Simulating Gemini API call for Aesthetic Score...")
    # Basic heuristic for simulation: higher whitespace/symmetry -> higher score
    # This is just for testing this module in isolation.
    simulated_score = 5
    simulated_explanation = "Simulated: Neutral aesthetic quality."

    # Dummy logic to make simulation somewhat dynamic based on image properties
    # (These properties would come from the actual image analysis in a real scenario)
    # This part won't be executed in the actual Streamlit call, but helps testing this function in isolation.
    if "test_calm.png" in image_data_base64: # Very rough check
        simulated_score = 8
        simulated_explanation = "Simulated: Clean and balanced composition, contributing to a pleasant aesthetic."
    elif "test_vibrant.png" in image_data_base64:
        simulated_score = 7
        simulated_explanation = "Simulated: Dynamic use of color, creating a vibrant and engaging aesthetic."
    elif "test_creative.png" in image_data_base64:
        simulated_score = 7
        simulated_explanation = "Simulated: Interesting asymmetric composition, suggesting a creative aesthetic."
    elif "test_golden.png" in image_data_base64:
        simulated_score = 9
        simulated_explanation = "Simulated: Strong adherence to classic proportional harmony, highly aesthetic."


    return {"score": simulated_score, "explanation": simulated_explanation}


def analyze_image(image_path: str) -> dict:
    """
    Analyzes an image for symmetry, whitespace, aspect ratio,
    fractal dimension, entropy, visual balance,
    and provides heuristic-based typography and mood inference.
    Includes a placeholder for Aesthetic Neural Score from Gemini.

    Args:
        image_path (str): Path to the input image.

    Returns:
        dict: A dictionary containing analysis results.
    """
    results = {
        "symmetry": {"horizontal": None, "vertical": None},
        "whitespace_percentage": None,
        "aspect_ratio": None,
        "golden_ratio_aspect_match": False,
        "fractal_dimension": None,
        "entropy": None,
        "visual_balance_score": None,
        "typography_inference": "unknown",
        "mood_emotion": "neutral",
        "aesthetic_neural_score": {"score": None, "explanation": "Not yet calculated (simulated in this module)"} # Updated field
    }

    try:
        with Image.open(image_path).convert("RGB") as img_rgb:
            img_gray = img_rgb.convert("L")
            img_array_rgb = np.array(img_rgb)
            img_array_gray = np.array(img_gray)
            height, width, _ = img_array_rgb.shape

            # Convert image to base64 for potential LLM call
            from io import BytesIO
            buffered = BytesIO()
            img_rgb.save(buffered, format="PNG") # Use PNG for base64 encoding
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            mime_type = "image/png"


            # 1. Aspect Ratio Determination
            aspect_ratio = round(width / height, 2)
            results["aspect_ratio"] = aspect_ratio
            if abs(aspect_ratio - GOLDEN_RATIO) < 0.1 or \
               abs(aspect_ratio - (1/GOLDEN_RATIO)) < 0.1:
                results["golden_ratio_aspect_match"] = True

            # 2. Symmetry Detection
            top_half = img_array_gray[:height // 2, :]
            bottom_half = img_array_gray[height // 2 + (height % 2):, :]
            bottom_half_flipped = np.flipud(bottom_half)

            if top_half.shape == bottom_half_flipped.shape and top_half.size > 0:
                horizontal_diff = np.sum(np.abs(top_half - bottom_half_flipped))
                max_diff = 255 * top_half.size
                results["symmetry"]["horizontal"] = 1 - (horizontal_diff / max_diff)
            else:
                results["symmetry"]["horizontal"] = 0.0

            left_half = img_array_gray[:, :width // 2]
            right_half = img_array_gray[:, width // 2 + (width % 2):]
            right_half_flipped = np.fliplr(right_half)

            if left_half.shape == right_half_flipped.shape and left_half.size > 0:
                vertical_diff = np.sum(np.abs(left_half - right_half_flipped))
                max_diff = 255 * left_half.size
                results["symmetry"]["vertical"] = 1 - (vertical_diff / max_diff)
            else:
                results["symmetry"]["vertical"] = 0.0

            # 3. Whitespace Analysis
            whitespace_threshold_high = 240
            whitespace_threshold_low = 15

            num_light_whitespace_pixels = np.sum(img_array_gray > whitespace_threshold_high)
            num_dark_whitespace_pixels = np.sum(img_array_gray < whitespace_threshold_low)
            total_pixels = img_array_gray.size

            results["whitespace_percentage"] = round(((num_light_whitespace_pixels + num_dark_whitespace_pixels) / total_pixels) * 100, 2)

            # 4. Fractal Dimension
            results["fractal_dimension"] = round(calculate_fractal_dimension(img_array_gray), 3)

            # 5. Image Entropy
            results["entropy"] = round(calculate_image_entropy(img_array_gray), 3)

            # 6. Visual Balance Score
            results["visual_balance_score"] = round(calculate_visual_balance_score(img_array_gray), 3)

            # 7. Typography Inference (Heuristic-based)
            inferred_typography_styles = []
            avg_rgb_norm = np.mean(img_array_rgb.reshape(-1, 3), axis=0) / 255.0
            avg_hls = colorsys.rgb_to_hls(avg_rgb_norm[0], avg_rgb_norm[1], avg_rgb_norm[2])
            avg_saturation = avg_hls[2]

            if results["whitespace_percentage"] > 70:
                inferred_typography_styles.append("light")
            if results["whitespace_percentage"] < 30:
                inferred_typography_styles.append("bold")

            if results["symmetry"]["horizontal"] > 0.85 and results["symmetry"]["vertical"] > 0.85:
                inferred_typography_styles.append("geometric")
            elif results["symmetry"]["horizontal"] < 0.5 or results["symmetry"]["vertical"] < 0.5:
                inferred_typography_styles.append("expressive")

            if avg_saturation > 0.6:
                inferred_typography_styles.append("display")
            elif avg_saturation < 0.2:
                inferred_typography_styles.append("serif")

            if "bold" in inferred_typography_styles and "light" in inferred_typography_styles:
                if results["whitespace_percentage"] < 50:
                    inferred_typography_styles.remove("light")
                else:
                    inferred_typography_styles.remove("bold")

            results["typography_inference"] = ", ".join(set(inferred_typography_styles)) if inferred_typography_styles else "sans-serif"

            # 8. Mood/Emotion Detection (Heuristic-based)
            inferred_moods = []
            avg_rgb = np.mean(img_array_rgb.reshape(-1, 3), axis=0)
            if avg_rgb[0] > avg_rgb[1] and avg_rgb[0] > avg_rgb[2]:
                if avg_saturation > 0.5:
                    inferred_moods.append("energetic")
                else:
                    inferred_moods.append("warm")
            elif avg_rgb[2] > avg_rgb[0] and avg_rgb[2] > avg_rgb[1]:
                if avg_saturation > 0.5:
                    inferred_moods.append("vibrant")
                else:
                    inferred_moods.append("calm")
            else:
                inferred_moods.append("neutral")

            if avg_saturation > 0.7:
                inferred_moods.append("vibrant")
            elif avg_saturation < 0.3:
                inferred_moods.append("muted")

            if results["whitespace_percentage"] > 70:
                inferred_moods.append("minimalist")
                if "vibrant" in inferred_moods: inferred_moods.remove("vibrant")
            elif results["whitespace_percentage"] < 30:
                inferred_moods.append("dense")

            avg_symmetry = (results["symmetry"]["horizontal"] + results["symmetry"]["vertical"]) / 2
            if avg_symmetry > 0.8:
                inferred_moods.append("balanced")
                inferred_moods.append("professional")
            elif avg_symmetry < 0.5:
                inferred_moods.append("dynamic")
                inferred_moods.append("creative")

            results["mood_emotion"] = ", ".join(set(inferred_moods)) if inferred_moods else "neutral"

            # 9. Aesthetic Neural Score (Simulated LLM Call)
            # In a real scenario, you'd send img_base64 and mime_type to your frontend
            # or an async worker that makes the actual Gemini API call.
            # For direct testing of this module, we simulate the response.
            aesthetic_score_data = get_aesthetic_score_from_gemini(img_base64, mime_type)
            results["aesthetic_neural_score"] = aesthetic_score_data


    except FileNotFoundError:
        print(f"Warning: Image not found at {image_path}. Skipping analysis.")
        return results
    except Exception as e:
        print(f"Error analyzing image {image_path}: {e}")
        return results

    return results

if __name__ == "__main__":
    print("--- Testing Advanced Image Analyzer ---")
    # Create dummy images for testing (ensure they are in 'assets' folder)
    try:
        from PIL import Image, ImageDraw
        # High Whitespace, Calm/Minimalist
        img_calm = Image.new('RGB', (200, 200), color = (240, 240, 240)) # Light grey background
        draw = ImageDraw.Draw(img_calm)
        draw.ellipse((70, 70, 130, 130), fill=(150, 150, 150)) # Grey circle
        img_calm.save('assets/test_calm.png')
        print("Dummy calm image 'assets/test_calm.png' created.")

        # Low Whitespace, Vibrant/Energetic
        img_vibrant = Image.new('RGB', (200, 200), color = (255, 100, 100)) # Red background
        draw = ImageDraw.Draw(img_vibrant)
        draw.rectangle((0, 0, 100, 200), fill=(50, 50, 255)) # Blue rectangle
        draw.rectangle((100, 0, 200, 200), fill=(255, 200, 0)) # Yellow rectangle
        img_vibrant.save('assets/test_vibrant.png')
        print("Dummy vibrant image 'assets/test_vibrant.png' created.")

        # Asymmetric, Creative
        img_creative = Image.new('RGB', (200, 200), color = (200, 200, 200))
        draw = ImageDraw.Draw(img_creative)
        draw.polygon([(20,20), (180,50), (100,180)], fill=(0,150,0)) # Asymmetric triangle
        img_creative.save('assets/test_creative.png')
        print("Dummy creative image 'assets/test_creative.png' created.")

        # Image with Golden Ratio aspect ratio (approx 1.618)
        # 161.8 x 100 pixels
        img_golden = Image.new('RGB', (162, 100), color = (100, 120, 150))
        draw = ImageDraw.Draw(img_golden)
        draw.rectangle((20, 20, 142, 80), fill=(200, 200, 220))
        img_golden.save('assets/test_golden.png')
        print("Dummy golden ratio image 'assets/test_golden.png' created.")


    except Exception as e:
        print(f"Could not create dummy images for image analyzer (Pillow might not be fully installed or permissions issue): {e}")
        print("Please ensure you have Pillow installed (`pip install Pillow`) and create some images manually in the 'assets' folder to test.")

    test_image_paths = [
        "assets/test_calm.png",
        "assets/test_vibrant.png",
        "assets/test_creative.png",
        "assets/test_golden.png",
        "non_existent_image.jpg" # For testing error handling
    ]

    for path in test_image_paths:
        print(f"\n--- Analyzing {path} ---")
        analysis_results = analyze_image(path)
        for key, value in analysis_results.items():
            if isinstance(value, dict):
                print(f"  {key.replace('_', ' ').title()}:")
                for sub_key, sub_value in value.items():
                    print(f"    {sub_key.replace('_', ' ').title()}: {sub_value}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
