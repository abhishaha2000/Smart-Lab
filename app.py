import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

st.set_page_config(page_title="Smart Electronics Lab Assistant", page_icon="⚡", layout="wide")

st.title("⚡ Smart Electronics Component Value Finder")
st.markdown("Upload a component image or use calculators to get the **exact component value** instantly.")

menu = st.sidebar.selectbox("Select Tool", [
    "🎨 Resistor Value Finder (Image + Calculator)",
    "🔋 Capacitor Value Decoder",
    "🔌 Transistor & IC Pinout Guide"
])

# 1. Resistor Value Finder
if menu == "🎨 Resistor Value Finder (Image + Calculator)":
    st.subheader("🎨 Resistor Value Finder")
    st.write("Resistor chi image upload kara ani khali direct color bands select karun **exact resistance value** (`10kΩ`, `470Ω`, etc.) bgha:")
    
    uploaded_file = st.file_uploader("Upload Resistor Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Resistor', width=300)
        st.success("Image uploaded successfully! Now select the color bands below to get the exact value.")

    st.markdown("---")
    st.subheader("🧮 Select Color Bands for Exact Value:")
    
    color_dict = {
        'Black': (0, 1), 'Brown': (1, 10), 'Red': (2, 100), 
        'Orange': (3, 1000), 'Yellow': (4, 10000), 'Green': (5, 100000), 
        'Blue': (6, 1000000), 'Violet': (7, 10000000), 'Grey': (8, 100000000), 'White': (9, 1000000000)
    }
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        band1 = st.selectbox("Band 1 (1st Digit)", list(color_dict.keys())[1:])
    with col2:
        band2 = st.selectbox("Band 2 (2nd Digit)", list(color_dict.keys()))
    with col3:
        multiplier = st.selectbox("Band 3 (Multiplier)", list(color_dict.keys()))
    with col4:
        tolerance = st.selectbox("Band 4 (Tolerance)", ["Gold (±5%)", "Silver (±10%)"])
        
    if st.button("Calculate Exact Resistance Value"):
        d1 = color_dict[band1][0]
        d2 = color_dict[band2][0]
        mult = color_dict[multiplier][1]
        resistance = ((d1 * 10) + d2) * mult
        
        if resistance >= 1000000:
            val_str = f"{resistance / 1000000} MΩ"
        elif resistance >= 1000:
            val_str = f"{resistance / 1000} kΩ"
        else:
            val_str = f"{resistance} Ω"
            
        st.success(f"🎯 Exact Resistor Value: **{val_str}** ({tolerance})")

# 2. Capacitor Value Decoder
elif menu == "🔋 Capacitor Value Decoder":
    st.subheader("🔋 Capacitor Value Decoder")
    st.write("Enter the printed code on the capacitor to get its exact value in pF, nF, and µF:")
    
    code_input = st.text_input("Enter Capacitor Code (e.g., 104, 222, 473):", value="104")
    
    if st.button("Get Exact Capacitor Value"):
        if len(code_input) >= 3:
            try:
                d1 = int(code_input[0])
                d2 = int(code_input[1])
                mult = int(code_input[2])
                pF = ((d1 * 10) + d2) * (10 ** mult)
                nF = pF / 1000
                uF = pF / 1000000
                
                st.success(f"🎯 Exact Capacitor Value for code **{code_input}**:")
                st.write(f"- **Picofarads:** {pF} pF")
                st.write(f"- **Nanofarads:** {nF} nF")
                st.write(f"- **Microfarads:** {uF} µF")
            except:
                st.error("Please enter a valid numeric code.")

# 3. Transistor & IC Pinout Guide
elif menu == "🔌 Transistor & IC Pinout Guide":
    st.subheader("🔌 Component Pinout & Specifications")
    comp_type = st.selectbox("Select Component", ["BC547 Transistor", "2N2222 Transistor", "IC 555 Timer", "IC 7805 Voltage Regulator"])
    
    if "BC547" in comp_type:
        st.write("**Component:** BC547 NPN Transistor")
        st.write("**Exact Pinout (Left to Right):** Collector (C) - Base (B) - Emitter (E)")
        st.write("**Max Voltage/Current:** 45V, 100mA")
    elif "2N2222" in comp_type:
        st.write("**Component:** 2N2222 NPN Transistor")
        st.write("**Exact Pinout:** Emitter - Base - Collector")
        st.write("**Max Voltage/Current:** 30V, 800mA")
    elif "555" in comp_type:
        st.write("**Component:** IC 555 Timer")
        st.write("**Pins:** 1:GND, 2:Trigger, 3:Output, 4:Reset, 5:Control, 6:Threshold, 7:Discharge, 8:VCC")
    elif "7805" in comp_type:
        st.write("**Component:** IC 7805 5V Regulator")
        st.write("**Pins:** 1:Input (VIN), 2:Ground (GND), 3:Output (+5V Fixed)")
