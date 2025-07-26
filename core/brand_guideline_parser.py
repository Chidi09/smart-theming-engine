import json
import os

def parse_brand_guidelines(guidelines_path: str) -> dict:
    """
    Parses a JSON file containing user-defined brand guidelines.

    Args:
        guidelines_path (str): Path to the JSON file containing brand guidelines.

    Returns:
        dict: A dictionary containing the parsed brand guidelines.
              Returns an empty dictionary if the file is not found or invalid.
    """
    if not os.path.exists(guidelines_path):
        print(f"Warning: Brand guidelines file not found at '{guidelines_path}'. Skipping brand guideline application.")
        return {}

    try:
        with open(guidelines_path, 'r', encoding='utf-8') as f:
            guidelines = json.load(f)

        # Basic validation of expected keys and types
        parsed_guidelines = {}

        # Colors (hex codes)
        for color_key in ["primaryColor", "secondaryColor", "accentColor"]:
            if color_key in guidelines and isinstance(guidelines[color_key], str) and guidelines[color_key].startswith("#") and len(guidelines[color_key]) in [7, 4]: # #RRGGBB or #RGB
                parsed_guidelines[color_key] = guidelines[color_key]
            elif color_key in guidelines:
                print(f"Warning: Invalid format for '{color_key}' in brand guidelines. Expected hex string (e.g., #RRGGBB). Skipping.")

        # Fonts (Google Font names)
        for font_key in ["headingFont", "bodyFont"]:
            if font_key in guidelines and isinstance(guidelines[font_key], str) and guidelines[font_key]:
                parsed_guidelines[font_key] = guidelines[font_key]
            elif font_key in guidelines:
                print(f"Warning: Invalid format for '{font_key}' in brand guidelines. Expected non-empty string. Skipping.")

        # Layout Preference
        if "layoutPreference" in guidelines and isinstance(guidelines["layoutPreference"], str) and guidelines["layoutPreference"] in ["minimalist", "bold", "classic", "modern"]: # Add more as needed
            parsed_guidelines["layoutPreference"] = guidelines["layoutPreference"]
        elif "layoutPreference" in guidelines:
            print(f"Warning: Invalid value for 'layoutPreference' in brand guidelines. Skipping.")

        print(f"Brand guidelines loaded successfully from '{guidelines_path}'.")
        return parsed_guidelines

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{guidelines_path}'. Please check the file content.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred while parsing brand guidelines: {e}")
        return {}

if __name__ == "__main__":
    print("--- Testing Brand Guideline Parser ---")

    # Create a dummy brand guidelines JSON file for testing
    dummy_guidelines_content = {
        "primaryColor": "#1A73E8",
        "secondaryColor": "#F0F0F0",
        "accentColor": "#EA4335",
        "headingFont": "Roboto",
        "bodyFont": "Open Sans",
        "layoutPreference": "minimalist",
        "invalidKey": 123 # This should be ignored with a warning
    }
    dummy_guidelines_path = "config/test_brand_guidelines.json"
    os.makedirs(os.path.dirname(dummy_guidelines_path), exist_ok=True)
    with open(dummy_guidelines_path, 'w', encoding='utf-8') as f:
        json.dump(dummy_guidelines_content, f, indent=4)
    print(f"Dummy brand guidelines file created at '{dummy_guidelines_path}'.")

    # Test 1: Valid guidelines file
    print("\n--- Test 1: Valid Guidelines ---")
    guidelines = parse_brand_guidelines(dummy_guidelines_path)
    print("Parsed Guidelines:", guidelines)

    # Test 2: Non-existent file
    print("\n--- Test 2: Non-existent File ---")
    non_existent_path = "config/non_existent.json"
    guidelines_non_existent = parse_brand_guidelines(non_existent_path)
    print("Parsed Guidelines (Non-existent):", guidelines_non_existent)

    # Test 3: Invalid JSON
    print("\n--- Test 3: Invalid JSON ---")
    invalid_json_path = "config/invalid_syntax.json"
    with open(invalid_json_path, 'w', encoding='utf-8') as f:
        f.write("{'primaryColor': '#ABC'") # Invalid JSON syntax
    guidelines_invalid_json = parse_brand_guidelines(invalid_json_path)
    print("Parsed Guidelines (Invalid JSON):", guidelines_invalid_json)

    # Test 4: Invalid data types/values
    print("\n--- Test 4: Invalid Data Types/Values ---")
    invalid_data_path = "config/invalid_data.json"
    invalid_data_content = {
        "primaryColor": "not_a_hex",
        "headingFont": "",
        "layoutPreference": "unknown_style"
    }
    with open(invalid_data_path, 'w', encoding='utf-8') as f:
        json.dump(invalid_data_content, f, indent=4)
    guidelines_invalid_data = parse_brand_guidelines(invalid_data_path)
    print("Parsed Guidelines (Invalid Data):", guidelines_invalid_data)
