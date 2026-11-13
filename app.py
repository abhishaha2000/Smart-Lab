import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

st.set_page_config(page_title="Smart Electronics Lab Assistant", page_icon="⚡", layout="wide")

st.title("⚡ Smart Electronics Lab Assistant (All Components)")
st.markdown("E&TC Students, Lecturers, ani Electronics Hobbyists sathi digital lab tool.")

# Sidebar Navigation for All Components
menu = st.sidebar.selectbox("Select Component / Tool", [
    "📷 General Image Color & Component Analyzer",
    "🎨 Resistor Value Calculator",
    "🔋 Capacitor Code Decoder",
    "🔌 Transistor Pinout & Reference",
    "⚡ IC & Regulator Guide (555, 741, 7805)",
    "💡 Diode & LED Voltage Drop Reference"
])

# 1. General Image Color & Component Analyzer
if menu == "📷 General Image Color & Component Analyzer":
    st.subheader("🔍 Universal Component Image Analyzer")
    st.write("Konthya pan electronic component chi image upload kara (Resistor, Capacitor, PCB board, etc.) ani tyatil main color palette/features analyze kara:")
    
    uploaded_file = st.file_uploader("Upload Component Image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Component', width=350)
        
        st.write("Analyzing component colors and pixel distribution...")
        
        # Image processing via KMeans for dominant colors
        image_resized = image.resize((100, 100))
        img_array = np.array(image_resized)
        pixels = img_array.reshape(-1, 3)
        
        n_colors = 5
        kmeans = KMeans(n_clusters=n_colors, n_init=10)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_.astype(int)
        
        st.subheader("Dominant Color Palette (Component Analysis):")
        cols = st.columns(n_colors)
        for i, color in enumerate(colors):
            hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
            with cols[i]:
                st.markdown(
                    f'<div style="background-color: {hex_color}; height: 60px; border-radius: 8px; border: 1px solid #ccc;"></div>',
                    unsafe_allow_html=True
                )
                st.write(f"RGB: {tuple(color)}")
                st.write(f"Hex: {hex_color}")

# 2. Resistor Calculator
elif menu == "🎨 Resistor Value Calculator":
    st.subheader("🎨 Resistor Color Code Calculator (4-Band)")
    
    color_dict = {
        'Black': (0, 1), 'Brown': (1, 10), 'Red': (2, 100), 
        'Orange': (3, 1000), 'Yellow': (4, 10000), 'Green': (5, 100000), 
        'Blue': (6, 1000000), 'Violet': (7, 10000000), 'Grey': (8, 100000000), 'White': (9, 1000000000)
    }
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        band1 = st.selectbox("Band 1", list(color_dict.keys())[1:])
    with col2:
        band2 = st.selectbox("Band 2", list(color_dict.keys()))
    with col3:
        multiplier = st.selectbox("Multiplier", list(color_dict.keys()))
    with col4:
        tolerance = st.selectbox("Tolerance", ["Gold (±5%)", "Silver (±10%)"])
        
    if st.button("Calculate Resistance"):
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
            
        st.success(f"Calculated Resistor Value: **{val_str}** ({tolerance})")

# 3. Capacitor Code Decoder
elif menu == "🔋 Capacitor Code Decoder":
    st.subheader("🔋 Ceramic & Electrolytic Capacitor Decoder")
    code_input = st.text_input("Enter Capacitor Code (e.g., 104, 222):", value="104")
    
    if st.button("Decode Capacitor"):
        if len(code_input) >= 3:
            try:
                d1 = int(code_input[0])
                d2 = int(code_input[1])
                mult = int(code_input[2])
                pF = ((d1 * 10) + d2) * (10 ** mult)
                nF = pF / 1000
                uF = pF / 1000000
                
                st.success(f"Results for code **{code_input}**:")
                st.write(f"- **Picofarads (pF):** {pF} pF")
                st.write(f"- **Nanofarads (nF):** {nF} nF")
                st.write(f"- **Microfarads (µF):** {uF} µF")
            except:
                st.error("Krupaya yogya numeric code taka (eg. 104).")

# 4. Transistor Pinout & Reference
elif menu == "🔌 Transistor Pinout & Reference":
    st.subheader("🔌 Transistor Pinout Guide")
    transistor = st.selectbox("Select Transistor", ["BC547 / BC548 / BC549 (NPN)", "BC557 / BC558 (PNP)", "2N2222 (NPN)", "TIP121 / TIP122 (Darlington NPN)"])
    
    if "BC547" in transistor:
        st.write("**Type:** NPN BJT (General Purpose)")
        st.write("**Pinout (Left to Right, flat face facing you):** Collector (C) - Base (B) - Emitter (E)")
        st.write("**Max Ratings:** $V_{CEO} = 45V$, $I_C = 100mA$")
    elif "BC557" in transistor:
        st.write("**Type:** PNP BJT")
        st.write("**Pinout (Left to Right, flat face facing you):** Collector (C) - Base (B) - Emitter (E)")
        st.write("**Max Ratings:** $V_{CEO} = -45V$, $I_C = -100mA$")
    elif "2N2222" in transistor:
        st.write("**Type:** NPN BJT (Switching & Amplification)")
        st.write("**Pinout (Metal Can / TO-92):** Emitter - Base - Collector (Tab aligned)")
        st.write("**Max Ratings:** $V_{CEO} = 30V$, $I_C = 800mA$")
    elif "TIP121" in transistor:
        st.write("**Type:** NPN Darlington Transistor (High Gain)")
        st.write("**Pinout (Left to Right, metal tab top):** Base (B) - Collector (C) - Emitter (E)")
        st.write("**Max Ratings:** $V_{CEO} = 80V$, $I_C = 5A$")

# 5. IC & Regulator Guide
elif menu == "⚡ IC & Regulator Guide (555, 741, 7805)":
    st.subheader("⚡ Integrated Circuits (ICs) & Regulators Reference")
    ic_choice = st.selectbox("Select IC", ["IC 555 Timer", "IC 741 Operational Amplifier", "IC 7805 Voltage Regulator (5V)", "IC 7812 Voltage Regulator (12V)"])
    
    if "555" in ic_choice:
        st.write("**Description:** Precision Timing Circuit (Astable, Monostable, Bistable modes)")
        st.write("**Pins (8-Pin DIP):**")
        st.markdown("1. GND | 2. Trigger | 3. Output | 4. Reset | 5. Control Voltage | 6. Threshold | 7. Discharge | 8. $V_{CC}$")
    elif "741" in ic_choice:
        st.write("**Description:** General Purpose Operational Amplifier")
        st.write("**Pins (8-Pin DIP):**")
        st.markdown("1. Offset Null | 2. Inverting Input (-) | 3. Non-Inverting Input (+) | 4. $V_{EE}$ (-Supply) | 5. Offset Null | 6. Output | 7. $V_{CC}$ (+Supply) | 8. Not Connected")
    elif "7805" in ic_choice:
        st.write("**Description:** 5V Fixed Positive Voltage Regulator")
        st.write("**Pins (TO-220 3-Pin):**")
        st.markdown("1. Input ($V_{IN}$ - 7V to 35V) | 2. Ground (GND) | 3. Output ($+5V$ Fixed)")
    elif "7812" in ic_choice:
        st.write("**Description:** 12V Fixed Positive Voltage Regulator")
        st.write("**Pins (TO-220 3-Pin):**")
        st.markdown("1. Input ($V_{IN}$ - 14V to 35V) | 2. Ground (GND) | 3. Output ($+12V$ Fixed)")

# 6. Diode & LED Reference
elif menu == "💡 Diode & LED Voltage Drop Reference":
    st.subheader("💡 Diodes & LEDs Characteristics Reference")
    st.write("Electronics madhe vaparlamya mahatvachya diodes ani LEDs che standard forward voltage drops:")
    
    st.markdown("""
    * **1N4007 Rectifier Diode:** $V_F \approx 0.7V$ (Max Current: 1A, Max Reverse Voltage: 1000V)
    * **1N4148 Switching Diode:** $V_F \approx 0.7V$ (High-speed signal switching)
    * **Red LED:** $V_F \approx 1.8V - 2.0V$
    * **Green / Yellow LED:** $V_F \approx 2.0V - 2.2V$
    * **Blue / White LED:** $V_F \approx 3.0V - 3.3V$
    * **Zener Diodes:** Available in various breakdown voltages ($3.3V, 5.1V, 9.1V, 12V$, etc.) for voltage regulation.
    """)
