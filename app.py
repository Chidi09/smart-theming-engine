import streamlit as st
import os
import zipfile
from io import BytesIO
import json
import uuid # For generating unique session directories

# Import your enhanced core modules
import core.image_analyzer as image_analyzer
import core.palette_extractor as palette_extractor
import core.font_suggester as font_suggester
import core.layout_generator as layout_generator
import core.js_component_suggester as js_component_suggester
import core.theme_builder as theme_builder

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="Smart Theming Engine",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Smart Theming Engine: Generate Bespoke Web Themes")
st.markdown("""
Upload an image, provide optional brand guidelines, and let our AI-powered engine
generate a comprehensive, responsive web theme tailored to your visual content!
""")

# --- Session State Initialization ---
if 'generated_theme_data' not in st.session_state:
    st.session_state['generated_theme_data'] = None
if 'current_output_dir' not in st.session_state:
    st.session_state['current_output_dir'] = None
if 'image_analysis_results' not in st.session_state:
    st.session_state['image_analysis_results'] = []
if 'brand_guidelines' not in st.session_state:
    st.session_state['brand_guidelines'] = {}


# --- Input Section ---
st.header("1. Upload Image & Define Preferences")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

st.subheader("Optional: Brand Guidelines (JSON)")
brand_guidelines_json = st.text_area(
    "Enter your brand guidelines as JSON (e.g., {'primaryColor': '#FF0000', 'layoutPreference': 'minimalist', 'designPrinciples': ['clean', 'modern']})",
    value=json.dumps(st.session_state['brand_guidelines'], indent=2),
    height=150,
    help="Define specific colors, fonts, layout preferences, or design principles."
)

try:
    if brand_guidelines_json:
        st.session_state['brand_guidelines'] = json.loads(brand_guidelines_json)
    else:
        st.session_state['brand_guidelines'] = {} # Reset if text area is empty
except json.JSONDecodeError:
    st.error("Invalid JSON in Brand Guidelines. Please correct it.")
    st.session_state['brand_guidelines'] = {} # Clear invalid input

layout_style_options = ["minimal", "dense", "creative"]
selected_layout_style = st.selectbox(
    "Choose a base layout style:",
    options=layout_style_options,
    index=layout_style_options.index("minimal") # Default to minimal
)

# --- Theme Generation Button ---
if st.button("🚀 Generate Theme"):
    if uploaded_file is None:
        st.warning("Please upload an image to generate a theme.")
    else:
        with st.spinner("Analyzing image and generating theme... This may take a moment."):
            # Create a unique temporary directory for this session's output
            session_id = str(uuid.uuid4())
            output_base_dir = "generated_themes"
            current_output_dir = os.path.join(output_base_dir, session_id)
            os.makedirs(current_output_dir, exist_ok=True)
            st.session_state['current_output_dir'] = current_output_dir

            # Save the uploaded image temporarily
            image_path = os.path.join(current_output_dir, uploaded_file.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # --- 1. Image Analysis ---
            st.info("Step 1/6: Analyzing image...")
            st.session_state['image_analysis_results'] = [image_analyzer.analyze_image(image_path)]
            if not st.session_state['image_analysis_results'] or st.session_state['image_analysis_results'][0].get("aesthetic_neural_score", {}).get("score") is None:
                st.warning("Image analysis results might be incomplete or failed. Proceeding with defaults.")
                # Provide a fallback for image_analysis_results if analysis fails completely
                st.session_state['image_analysis_results'] = [{
                    "symmetry": {"horizontal": 0.5, "vertical": 0.5},
                    "whitespace_percentage": 50.0,
                    "aspect_ratio": 1.77,
                    "golden_ratio_aspect_match": False,
                    "fractal_dimension": 1.5,
                    "entropy": 4.0,
                    "visual_balance_score": 0.5,
                    "typography_inference": "sans-serif",
                    "mood_emotion": "neutral",
                    "aesthetic_neural_score": {"score": 5, "explanation": "Default score due to analysis issue."}
                }]
            
            first_image_analysis = st.session_state['image_analysis_results'][0] # Use the first one for display

            # --- 2. Palette Extraction ---
            st.info("Step 2/6: Extracting color palette...")
            palette_data = palette_extractor.extract_palette(image_path, st.session_state['brand_guidelines'])

            # --- 3. Font Suggestion ---
            st.info("Step 3/6: Suggesting fonts...")
            font_suggestions = font_suggester.suggest_fonts(st.session_state['image_analysis_results'], st.session_state['brand_guidelines'])

            # --- 4. JS Component Suggestion ---
            st.info("Step 4/6: Suggesting JavaScript components...")
            js_component_suggestions = js_component_suggester.suggest_js_components(
                st.session_state['image_analysis_results'],
                selected_layout_style,
                st.session_state['brand_guidelines']
            )
            # Save JS component suggestions to a file for download
            js_suggestions_path = os.path.join(current_output_dir, "suggested-components.txt")
            with open(js_suggestions_path, "w", encoding="utf-8") as f:
                f.write("Suggested JavaScript Components:\n\n")
                for comp in js_component_suggestions:
                    f.write(f"Component: {comp['component']}\n")
                    f.write(f"  Variation: {comp['variation']}\n")
                    f.write(f"  Rationale: {comp['rationale']}\n\n")
            
            # --- 5. Theme File Building (CSS, Tailwind Config, Guide) ---
            st.info("Step 5/6: Building theme files...")
            theme_files_output = theme_builder.build_theme_files(
                palette_data,
                font_suggestions,
                st.session_state['brand_guidelines'],
                current_output_dir
            )
            
            # Read the generated theme.css content for inlining into the HTML layout
            with open(theme_files_output['theme_css_path'], 'r', encoding='utf-8') as f:
                theme_css_content_for_inlining = f.read()

            # --- 6. Layout Generation (with inlined CSS) ---
            st.info("Step 6/6: Generating HTML layout...")
            generated_html_content, active_brand_guidelines_used = layout_generator.generate_layout(
                st.session_state['image_analysis_results'],
                st.session_state['brand_guidelines'], # Pass original BG, layout_generator will infer if empty
                selected_layout_style,
                current_output_dir, # Pass the output directory for saving themed-layout.html
                theme_css_content=theme_css_content_for_inlining # Pass CSS content to inline
            )

            st.session_state['generated_theme_data'] = {
                "html_content": generated_html_content,
                "palette_data": palette_data,
                "font_suggestions": font_suggestions,
                "js_component_suggestions": js_component_suggestions,
                "theme_files_output": theme_files_output,
                "output_dir": current_output_dir,
                "active_brand_guidelines_used": active_brand_guidelines_used,
                "image_analysis": first_image_analysis # Store first image analysis for display
            }
            st.success("Theme generated successfully!")

# --- Display Results Section ---
if st.session_state['generated_theme_data']:
    st.header("2. Generated Theme Details")

    # Display Image Analysis
    st.subheader("Image Analysis Summary")
    analysis = st.session_state['generated_theme_data']['image_analysis']
    st.json(analysis)

    # Display Color Palette
    st.subheader("Color Palette")
    colors = st.session_state['generated_theme_data']['palette_data']['palette']
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    color_cols = [col1, col2, col3, col4, col5, col6, col7]
    color_names = ['primary', 'secondary', 'accent', 'text_dark', 'text_light', 'background_light', 'background_dark']
    for i, name in enumerate(color_names):
        if name in colors:
            color_cols[i].color_picker(f"{name.replace('_', ' ').title()}", colors[name], disabled=True)
            color_cols[i].write(f"**{colors[name]}**")
    st.markdown(f"**Color Harmony Score:** {st.session_state['generated_theme_data']['palette_data']['color_harmony_score']['score']:.2f} (Rationale: {st.session_state['generated_theme_data']['palette_data']['color_harmony_score']['explanation']})")
    st.markdown(f"**Accessibility Suggestions:** {', '.join(st.session_state['generated_theme_data']['palette_data']['accessibility_suggestions']) if st.session_state['generated_theme_data']['palette_data']['accessibility_suggestions'] else 'None'}")

    # Display Font Suggestions
    st.subheader("Font Suggestions")
    fonts = st.session_state['generated_theme_data']['font_suggestions']
    st.write(f"**Heading Font:** `{fonts['heading_font']}`")
    st.write(f"**Body Font:** `{fonts['body_font']}`")
    st.write("**Font Size Scale (px):**")
    st.json(fonts['font_size_scale'])
    st.write("**Typographic Recommendations:**")
    st.json(fonts['typographic_recommendations'])

    # Display JS Component Suggestions
    st.subheader("JavaScript Component Suggestions")
    for comp in st.session_state['generated_theme_data']['js_component_suggestions']:
        st.markdown(f"**{comp['component']}**: {comp['variation']}")
        st.caption(f"Rationale: {comp['rationale']}")

    # Display Active Brand Guidelines Used
    st.subheader("Active Brand Guidelines Used")
    st.json(st.session_state['generated_theme_data']['active_brand_guidelines_used'])

    # --- Live Preview ---
    st.header("3. Live Theme Preview")
    st.markdown("This is a live preview of your generated HTML layout with the applied theme.")
    
    # Use st.components.v1.html to embed the generated HTML
    # Since theme.css content is now inlined in layout_generator, this should work.
    st.components.v1.html(st.session_state['generated_theme_data']['html_content'], height=800, scrolling=True)

    # --- Download Feature ---
    st.header("4. Download Your Theme Project")
    st.markdown("Download a `.zip` file containing all generated theme assets (HTML layout, CSS, Tailwind config, and integration guide).")

    # Create a BytesIO object to hold the zip file in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        output_dir_for_download = st.session_state['current_output_dir']
        
        # List all files in the generated directory and add them to the zip
        for root, _, files in os.walk(output_dir_for_download):
            for file in files:
                file_path = os.path.join(root, file)
                # Ensure the path inside the zip is relative to the base output_dir
                arcname = os.path.relpath(file_path, output_dir_for_download)
                zf.write(file_path, arcname)

    zip_buffer.seek(0) # Rewind the buffer to the beginning

    st.download_button(
        label="Download Full Theme Project (.zip)",
        data=zip_buffer,
        file_name="smart_theme_project.zip",
        mime="application/zip",
        help="Download a zip archive containing all generated theme files and an integration guide."
    )

    st.markdown("---")
    st.caption("Developed with ❤️ by Your Smart Theming Engine")

