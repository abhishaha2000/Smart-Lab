import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

st.set_page_config(page_title="Smart Electronics Lab Assistant", page_icon="⚡", layout="wide")

st.title("⚡ Smart Electronics Lab Assistant & Value Finder")
st.markdown("A comprehensive digital tool for E&TC students and electronics hobbyists to identify components and calculate values.")

# Sidebar Navigation in English
menu = st.sidebar.selectbox("Select Tool / Calculator", [
    "📷 Component Image & Color Analyzer",
    "🎨 Resistor Color Code Calculator",
    "🔢 SMD Resistor Code Decoder",
    "🔋 Capacitor Code Decoder",
    "🔌 Transistor Pinout Reference",
    "⚡ IC & Voltage Regulator Guide"
])

# 1. Component Image & Color Analyzer
if menu == "📷 Component Image & Color Analyzer":
    st.subheader("Universal Component Image & Color Analyzer")
    st.write("Upload an image of an electronic component to analyze its color distribution and dominant color palette:")
    
    uploaded_file = st.file_uploader("Upload Component Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Electronic Component', width=350)
        
        st.write("Analyzing component features and color bands...")
        
        # Image processing via KMeans for dominant colors
        image_resized = image.resize((100, 100))
        img_array = np.array(image_resized)
        pixels = img_array.reshape(-1, 3)
        
        n_colors = 4
        kmeans = KMeans(n_clusters=n_colors, n_init=10)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_.astype(int)
        
        st.subheader("Extracted Dominant Color Palette:")
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
        st.info("Tip: Use the specialized calculators in the sidebar to get exact resistor or capacitor values based on these colors or printed codes.")

# 2. Resistor Color Code Calculator
elif menu == "🎨 Resistor Color Code Calculator":
    st.subheader("4-Band Resistor Value Calculator")
    st.write("Select the color bands of your resistor to calculate its exact resistance value:")
    
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

# 3. SMD Resistor Code Decoder
elif menu == "🔢 SMD Resistor Code Decoder":
    st.subheader("SMD Resistor Code Decoder")
    st.write("Enter the 3-digit or 4-digit code printed on surface-mount (SMD) resistors:")
    
    smd_code = st.text_input("Enter SMD Code (e.g., 472, 1001):", value="472")
    
    if st.button("Decode SMD Resistor"):
        try:
            code = smd_code.strip()
            if len(code) == 3:
                d1 = int(code[0])
                d2 = int(code[1])
                mult = int(code[2])
                resistance = ((d1 * 10) + d2) * (10 ** mult)
            elif len(code) == 4:
                d1 = int(code[0])
                d2 = int(code[1])
                d3 = int(code[2])
                mult = int(code[3])
                resistance = ((d1 * 100) + (d2 * 10) + d3) * (10 ** mult)
            else:
                resistance = None
                
            if resistance is not None:
                if resistance >= 1000000:
                    val_str = f"{resistance / 1000000} MΩ"
                elif resistance >= 1000:
                    val_str = f"{resistance / 1000} kΩ"
                else:
                    val_str = f"{resistance} Ω"
                st.success(f"Decoded Resistance Value: **{val_str}**")
            else:
                st.error("Please enter a valid 3-digit or 4-digit SMD code.")
        except:
            st.error("Invalid input format. Please try again.")

# 4. Capacitor Code Decoder
elif menu == "🔋 Capacitor Code Decoder":
    st.subheader("Ceramic Capacitor Code Decoder")
    st.write("Enter the 3-digit code printed on ceramic capacitors (e.g., 104, 103):")
    
    code_input = st.text_input("Enter Capacitor Code:", value="104")
    
    if st.button("Decode Capacitor"):
        if len(code_input) >= 3:
            try:
                d1 = int(code_input[0])
                d2 = int(code_input[1])
                mult = int(code_input[2])
                pF = ((d1 * 10) + d2) * (10 ** mult)
                nF = pF / 1000
                uF = pF / 1000000
                
                st.success(f"Decoded Values for Code **{code_input}**:")
                st.write(f"- **Picofarads (pF):** {pF} pF")
                st.write(f"- **Nanofarads (nF):** {nF} nF")
                st.write(f"- **Microfarads (µF):** {uF} µF")
            except:
                st.error("Please enter a valid numeric code.")

# 5. Transistor Pinout Reference
elif menu == "🔌 Transistor Pinout Reference":
    st.subheader("Transistor Pinout & Specifications Guide")
    transistor = st.selectbox("Select Transistor", ["BC547 / BC548 (NPN)", "BC557 / BC558 (PNP)", "2N2222 (NPN)", "TIP121 / TIP122 (Darlington NPN)"])
    
    if "BC547" in transistor:
        st.write("**Type:** NPN BJT (General Purpose)")
        st.write("**Pinout Configuration (Left to Right, flat face forward):** Collector (C) - Base (B) - Emitter (E)")
        st.write("**Maximum Ratings:** $V_{CEO} = 45V$, $I_C = 100mA$")
    elif "BC557" in transistor:
        st.write("**Type:** PNP BJT")
        st.write("**Pinout Configuration (Left to Right, flat face forward):** Collector (C) - Base (B) - Emitter (E)")
        st.write("**Maximum Ratings:** $V_{CEO} = -45V$, $I_C = -100mA$")
    elif "2N2222" in transistor:
        st.write("**Type:** NPN BJT (Switching & Amplification)")
        st.write("**Pinout Configuration:** Emitter - Base - Collector")
        st.write("**Maximum Ratings:** $V_{CEO} = 30V$, $I_C = 800mA$")
    elif "TIP121" in transistor:
        st.write("**Type:** NPN Darlington Transistor")
        st.write("**Pinout Configuration (Left to Right, metal tab on top):** Base (B) - Collector (C) - Emitter (E)")
        st.write("**Maximum Ratings:** $V_{CEO} = 80V$, $I_C = 5A$")

# 6. IC & Voltage Regulator Guide
elif menu == "⚡ IC & Voltage Regulator Guide":
    st.subheader("Integrated Circuits & Voltage Regulators Reference")
    ic_choice = st.selectbox("Select IC", ["IC 555 Timer", "IC 741 Operational Amplifier", "IC 7805 Voltage Regulator (5V)", "IC 7812 Voltage Regulator (12V)"])
    
    if "555" in ic_choice:
        st.write("**Description:** Precision Timing Circuit (Astable, Monostable, Bistable modes)")
        st.write("**Pinout (8-Pin DIP):**")
        st.markdown("1. GND | 2. Trigger | 3. Output | 4. Reset | 5. Control Voltage | 6. Threshold | 7. Discharge | 8. $V_{CC}$")
    elif "741" in ic_choice:
        st.write("**Description:** General Purpose Operational Amplifier")
        st.write("**Pinout (8-Pin DIP):**")
        st.markdown("1. Offset Null | 2. Inverting Input (-) | 3. Non-Inverting Input (+) | 4. $V_{EE}$ (-Supply) | 5. Offset Null | 6. Output | 7. $V_{CC}$ (+Supply) | 8. Not Connected")
    elif "7805" in ic_choice:
        st.write("**Description:** 5V Fixed Positive Voltage Regulator")
        st.write("**Pinout (TO-220 3-Pin):**")
        st.markdown("1. Input ($V_{IN}$) | 2. Ground (GND) | 3. Output ($+5V$ Fixed)")
    elif "7812" in ic_choice:
        st.write("**Description:** 12V Fixed Positive Voltage Regulator")
        st.write("**Pinout (TO-220 3-Pin):**")
        st.markdown("1. Input ($V_{IN}$) | 2. Ground (GND) | 3. Output ($+12V$ Fixed)")
