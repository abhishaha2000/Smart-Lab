import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import colorsys

st.set_page_config(page_title="Smart Electronics Lab Assistant", page_icon="⚡", layout="wide")

st.title("⚡ Smart Electronics Component Value Finder")
st.markdown("Upload a component image. The app uses **HSV Color Analysis** to accurately detect color bands regardless of lighting.")

menu = st.sidebar.selectbox("Select Tool", [
    "🔍 Auto Component Value Detector (HSV)",
    "🎨 Manual Resistor Calculator",
    "🔋 Capacitor Value Decoder",
    "🔌 Transistor & IC Pinout Guide"
])

# 1. Automated Component Value Detector using HSV
if menu == "🔍 Auto Component Value Detector (HSV)":
    st.subheader("Advanced Resistor Color Detector (Lighting-Invariant)")
    st.write("Upload a clear image of a resistor:")
    
    uploaded_file = st.file_uploader("Upload Component Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Component', width=350)
        
        st.write("Processing image with HSV color space analysis...")
        
        img_resized = image.resize((100, 100))
        img_array = np.array(img_resized)
        
        if img_array.shape[2] == 4:
            img_array = img_array[:, :, :3]
            
        pixels = img_array.reshape(-1, 3)
        
        # KMeans clustering to extract dominant colors
        kmeans = KMeans(n_clusters=4, n_init=10)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_.astype(int)
        
        st.success("🎯 Image analyzed successfully!")
        
        st.subheader("Detected Color Bands (HSV Corrected):")
        cols = st.columns(len(colors))
        
        # Robust HSV-based color classification function
        def get_hsv_color_name(rgb):
            r, g, b = rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            
            hue = h * 360  # Degrees 0-360
            sat = s * 100  # Percentage 0-100
            val = v * 100  # Percentage 0-100
            
            # Threshold classifications based on Hue, Saturation, Value
            if val < 20:
                return "Black", 0
            if val > 85 and sat < 15:
                return "White / Background", -1
            if sat < 20 and val < 60:
                return "Grey", 8
                
            # Hue ranges for standard resistor colors
            if (hue < 15 or hue >= 345):
                if val < 45:
                    return "Brown", 1
                else:
                    return "Red", 2
            elif 15 <= hue < 35:
                if sat > 60:
                    return "Orange", 3
                else:
                    return "Brown", 1
            elif 35 <= hue < 65:
                return "Yellow", 4
            elif 65 <= hue < 170:
                return "Green", 5
            elif 170 <= hue < 260:
                return "Blue", 6
            elif 260 <= hue < 320:
                return "Violet", 7
            else:
                return "Red", 2

        valid_digits = []
        for i, color in enumerate(colors):
            r, g, b = int(color[0]), int(color[1]), int(color[2])
            hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            color_name, digit = get_hsv_color_name((r, g, b))
            
            if digit != -1 and color_name != "White / Background":
                valid_digits.append(digit)
                
            with cols[i]:
                st.markdown(
                    f'<div style="background-color: {hex_color}; height: 50px; border-radius: 8px; border: 1px solid #ccc;"></div>',
                    unsafe_allow_html=True
                )
                st.write(f"**{color_name}**")
                st.write(f"RGB: ({r}, {g}, {b})")
                
        # Calculate Resistance dynamically
        if len(valid_digits) >= 2:
            d1 = valid_digits[0]
            d2 = valid_digits[1]
            mult_power = valid_digits[2] if len(valid_digits) > 2 else 2 
            
            calculated_res = ((d1 * 10) + d2) * (10 ** mult_power)
            
            if calculated_res >= 1000000:
                res_str = f"{calculated_res / 1000000} MΩ"
            elif calculated_res >= 1000:
                res_str = f"{calculated_res / 1000} kΩ"
            else:
                res_str = f"{calculated_res} Ω"
                
            st.info(f"💡 **Calculated Component Value:** **{res_str}**")
        else:
            st.warning("⚠️ Could not isolate distinct color bands clearly. Try uploading a macro shot with bright lighting, or use the **Manual Resistor Calculator** tab for instant exact values.")

# 2. Manual Resistor Calculator
elif menu == "🎨 Manual Resistor Calculator":
    st.subheader("🎨 Manual Resistor Color Code Calculator")
    color_dict = {'Black': 0, 'Brown': 1, 'Red': 2, 'Orange': 3, 'Yellow': 4, 'Green': 5, 'Blue': 6, 'Violet': 7, 'Grey': 8, 'White': 9}
    
    col1, col2, col3 = st.columns(3)
    with col1:
        b1 = st.selectbox("Band 1 (1st Digit)", list(color_dict.keys())[1:])
    with col2:
        b2 = st.selectbox("Band 2 (2nd Digit)", list(color_dict.keys()))
    with col3:
        mult = st.selectbox("Multiplier (Band 3)", list(color_dict.keys()))
        
    if st.button("Calculate Exact Value"):
        res = ((color_dict[b1] * 10) + color_dict[b2]) * (10 ** color_dict[mult])
        val_str = f"{res / 1000000} MΩ" if res >= 1000000 else (f"{res / 1000} kΩ" if res >= 1000 else f"{res} Ω")
        st.success(f"🎯 Exact Resistance Value: **{val_str}**")

# 3. Capacitor Value Decoder
elif menu == "🔋 Capacitor Value Decoder":
    st.subheader("🔋 Capacitor Value Decoder")
    code_input = st.text_input("Enter Capacitor Code (e.g., 104):", value="104")
    if st.button("Get Value"):
        try:
            d1, d2, mult = int(code_input[0]), int(code_input[1]), int(code_input[2])
            pF = ((d1 * 10) + d2) * (10 ** mult)
            st.success(f"Value: {pF} pF = {pF/1000} nF = {pF/1000000} µF")
        except:
            st.error("Invalid code.")

# 4. Transistor & IC Guide
elif menu == "🔌 Transistor & IC Pinout Guide":
    st.subheader("🔌 Component Pinouts")
    comp = st.selectbox("Select", ["BC547 Transistor", "IC 555 Timer", "IC 7805 Regulator"])
    if "BC547" in comp:
        st.write("**BC547 Pinout:** Collector (C) - Base (B) - Emitter (E)")
    elif "555" in comp:
        st.write("**555 Timer Pins:** 1:GND, 2:Trigger, 3:Output, 4:Reset, 5:Control, 6:Threshold, 7:Discharge, 8:VCC")
    elif "7805" in comp:
        st.write("**7805 Regulator:** Pin 1: Input, Pin 2: Ground, Pin 3: Output (+5V)")
