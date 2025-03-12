import streamlit as st
from PIL import Image
import io

st.title("Photo Compressor")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_container_width=True)

    # Choose compression mode
    mode = st.radio("Compression Mode", ["By Quality", "By Target Size"])

    if mode == "By Quality":
        quality = st.slider("Select compression quality (higher = better quality, larger size)", 1, 100, 75)
    else:
        target_size = st.number_input("Target size (in KB)", min_value=1, value=100)

    # Function to compress by target size
    def compress_to_target_size(image, target_size_kb):
        quality = 95
        step = 2
        target_size_bytes = target_size_kb * 1024
        
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="JPEG", quality=quality)
        
        while img_bytes.tell() > target_size_bytes and quality > 5:
            quality -= step
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="JPEG", quality=quality)
        
        return img_bytes, quality

    if st.button("Compress"):
        format = image.format if image.format != "PNG" else "JPEG"
        compressed_image = io.BytesIO()

        if mode == "By Quality":
            image.save(compressed_image, format=format, quality=quality)
            compressed_image.seek(0)
            st.success(f"Compressed with quality: {quality}")
        else:
            compressed_image, final_quality = compress_to_target_size(image.convert("RGB"), target_size)
            st.success(f"Compressed to ~{target_size} KB at quality: {final_quality}")

        # Display compressed image size
        compressed_size_kb = len(compressed_image.getvalue()) / 1024
        st.write(f"**Compressed size:** {compressed_size_kb:.2f} KB")

        # Show compressed image
        st.image(compressed_image, caption="Compressed Image", use_container_width=True)

        # Download button
        st.download_button(
            label="Download Compressed Image",
            data=compressed_image,
            file_name=f"compressed_image.{format.lower()}",
            mime=f"image/{format.lower()}"
        )
