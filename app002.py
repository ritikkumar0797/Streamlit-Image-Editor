import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import io

st.set_page_config(page_title="Image Editor", layout="wide")
st.title("🖼️ Image Editor")

# -----------------------------
# Step 1: Upload Image
# -----------------------------
uploaded_file = st.file_uploader("Upload an image from your device", type=["png", "jpg", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)
    img = img.convert("RGB")  # Ensure consistent mode
else:
    st.info("Please upload an image to start editing.")
    st.stop()

# -----------------------------
# Step 2: Sidebar Controls
# -----------------------------
st.sidebar.header("Adjustments")

# Sliders for real-time adjustments
brightness = st.sidebar.slider("Brightness", 0.0, 2.0, 1.0, 0.1)
contrast = st.sidebar.slider("Contrast", 0.0, 2.0, 1.0, 0.1)
sharpness = st.sidebar.slider("Sharpness", 0.0, 2.0, 1.0, 0.1)
color = st.sidebar.slider("Color", 0.0, 2.0, 1.0, 0.1)

st.sidebar.header("Operations")
rotate_btn = st.sidebar.button("Rotate 90°")
flip_btn = st.sidebar.button("Flip Horizontally")
blur_btn = st.sidebar.button("Blur")
emboss_btn = st.sidebar.button("Emboss")
edge_btn = st.sidebar.button("Edge Enhance")
reset_btn = st.sidebar.button("Reset")

st.sidebar.header("Resize / Crop")
resize_width = st.sidebar.number_input("Resize Width", min_value=1, value=img.width)
resize_height = st.sidebar.number_input("Resize Height", min_value=1, value=img.height)
resize_btn = st.sidebar.button("Apply Resize")

# -----------------------------
# Step 3: Apply Changes
# -----------------------------
# Create a working copy
output = img.copy()

# Apply sliders
output = ImageEnhance.Brightness(output).enhance(brightness)
output = ImageEnhance.Contrast(output).enhance(contrast)
output = ImageEnhance.Sharpness(output).enhance(sharpness)
output = ImageEnhance.Color(output).enhance(color)

# Apply buttons
if rotate_btn:
    output = output.rotate(90, expand=True)
if flip_btn:
    output = output.transpose(Image.FLIP_LEFT_RIGHT)
if blur_btn:
    output = output.filter(ImageFilter.BLUR)
if emboss_btn:
    output = output.filter(ImageFilter.EMBOSS)
if edge_btn:
    output = output.filter(ImageFilter.FIND_EDGES)
if reset_btn:
    output = img.copy()

if resize_btn:
    output = output.resize((resize_width, resize_height))


# -----------------------------
# Step 4: Display Images
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Image")
    st.image(img, use_container_width=True)

with col2:
    st.subheader("Edited Image")
    st.image(output, use_container_width=True)

# -----------------------------
# Step 5: Save Image
# -----------------------------
buf = io.BytesIO()
output.save(buf, format="PNG")
byte_im = buf.getvalue()

st.download_button(
    label="💾 Save Edited Image",
    data=byte_im,
    file_name="edited_image.png",
    mime="image/png"
)
