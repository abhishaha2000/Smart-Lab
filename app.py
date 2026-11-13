import streamlit as st

st.set_page_config(page_title="Smart Electronics Lab Assistant", page_icon="⚡", layout="wide")

st.title("⚡ Smart Electronics Lab Assistant")
st.markdown("Accurate Resistor, Capacitor, and Component Calculator for E&TC Students.")

menu = st.sidebar.selectbox("Select Tool", [
    "🎨 Exact Resistor Color Code Calculator",
    "🔋 Capacitor Value Decoder",
    "🔌 Transistor & IC Pinout Guide"
])

if menu == "🎨 Exact Resistor Color Code Calculator":
    st.subheader("🎨 Exact Resistor Value Calculator (4-Band)")
    st.write("Resistor varil color bands select kara ani **100% accurate exact value** mela:")
    
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
        
    if st.button("Calculate Exact Resistance"):
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
            
        st.success(f"🎯 **Exact Resistance Value:** **{val_str}** ({tolerance})")

elif menu == "🔋 Capacitor Value Decoder":
    st.subheader("🔋 Ceramic Capacitor Code Decoder")
    code_input = st.text_input("Enter Capacitor Code (e.g., 104, 222):", value="104")
    
    if st.button("Decode Capacitor Value"):
        try:
            d1 = int(code_input[0])
            d2 = int(code_input[1])
            mult = int(code_input[2])
            pF = ((d1 * 10) + d2) * (10 ** mult)
            nF = pF / 1000
            uF = pF / 1000000
            
            st.success(f"🎯 Decoded Value for code **{code_input}**:")
            st.write(f"- **Picofarads:** {pF} pF")
            st.write(f"- **Nanofarads:** {nF} nF")
            st.write(f"- **Microfarads:** {uF} µF")
        except:
            st.error("Please enter a valid 3-digit numeric code.")

elif menu == "🔌 Transistor & IC Pinout Guide":
    st.subheader("🔌 Component Pinouts Reference")
    comp = st.selectbox("Select Component", ["BC547 Transistor", "2N2222 Transistor", "IC 555 Timer", "IC 7805 Voltage Regulator"])
    
    if "BC547" in comp:
        st.write("**BC547 Pinout (Left to Right, flat face facing you):** Collector (C) - Base (B) - Emitter (E)")
    elif "2N2222" in comp:
        st.write("**2N2222 Pinout:** Emitter - Base - Collector")
    elif "555" in comp:
        st.write("**IC 555 Timer Pins:** 1:GND, 2:Trigger, 3:Output, 4:Reset, 5:Control, 6:Threshold, 7:Discharge, 8:VCC")
    elif "7805" in comp:
        st.write("**IC 7805 Regulator Pins:** 1:Input (VIN), 2:Ground (GND), 3:Output (+5V Fixed)")
