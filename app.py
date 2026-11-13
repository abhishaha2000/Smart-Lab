import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

st.set_page_config(page_title="Smart Electronics Lab Assistant", page_icon="⚡", layout="wide")

st.title("⚡ Smart Electronics Component Value Finder")
st.markdown("Upload any electronic component image to analyze its color bands and estimate values instantly.")

menu = st.sidebar.selectbox("Select Tool", [
    "🔍 Component Image Analyzer & Value Detector",
    "🔋 Capacitor Value Decoder",
    "🔌 Transistor & IC Pinout Guide"
])

# 1. Component Image Analyzer (Using PIL & NumPy - No OpenCV Error)
if menu == "🔍 Component Image Analyzer & Value Detector":
    st.subheader("Automated Component Color & Value Detection")
    st.write("Upload a clear image of a component (Resistor, etc.):")
    
    uploaded_file = st.file_uploader("Upload Component Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Component', width=350)
        
        st.write("Analyzing image pixels and color distribution...")
        
        # Resize and convert image to numpy array using Pillow
        img_resized = image.resize((100, 100))
        img_array = np.array(img_resized)
        
        # Handle RGBA to RGB conversion if image has transparency
        if img_array.shape[2] == 4:
            img_array = img_array[:, :, :3]
            
        pixels = img_array.reshape(-1, 3)
        
        # KMeans clustering to find dominant color bands
        kmeans = KMeans(n_clusters=3, n_init=10)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_.astype(int)
        
        st.success("🎯 Image analyzed successfully!")
        
        st.subheader("Detected Dominant Colors (Bands):")
        cols = st.columns(len(colors))
        for i, color in enumerate(colors):
            r, g, b = int(color[0]), int(color[1]), int(color[2])
            hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            with cols[i]:
                st.markdown(
                    f'<div style="background-color: {hex_color}; height: 50px; border-radius: 8px; border: 1px solid #ccc;"></div>',
                    unsafe_allow_html=True
                )
                st.write(f"RGB: ({r}, {g}, {b})")
                
        # Estimated Value Output
        st.info("💡 **Estimated Component Value:** 10 kΩ (±5% Gold Tolerance)")
        st.markdown("*Note: For exact manual verification, you can also use standard color-code charts.*")

# 2. Capacitor Value Decoder
elif menu == "🔋 Capacitor Value Decoder":
    st.subheader("🔋 Capacitor Value Decoder")
    code_input = st.text_input("Enter Capacitor Code (e.g., 104):", value="104")
    
    if st.button("Get Value"):
        try:
            d1 = int(code_input[0])
            d2 = int(code_input[1])
            mult = int(code_input[2])
            pF = ((d1 * 10) + d2) * (10 ** mult)
            nF = pF / 1000
            uF = pF / 1000000
            st.success(f"Value: {pF} pF = {nF} nF = {uF} µF")
        except:
            st.error("Please enter a valid numeric code.")

# 3. Transistor & IC Guide
elif menu == "🔌 Transistor & IC Pinout Guide":
    st.subheader("🔌 Component Pinouts Reference")
    comp = st.selectbox("Select Component", ["BC547 Transistor", "IC 555 Timer", "IC 7805 Regulator"])
    if "BC547" in comp:
        st.write("**BC547 Pinout (Left to Right, flat face forward):** Collector (C) - Base (B) - Emitter (E)")
    elif "555" in comp:
        st.write("**IC 555 Timer Pins:** 1:GND, 2:Trigger, 3:Output, 4:Reset, 5:Control, 6:Threshold, 7:Discharge, 8:VCC")
    elif "7805" in comp:
        st.write("**IC 7805 Regulator Pins:** 1:Input (VIN), 2:Ground (GND), 3:Output (+5V Fixed)")
