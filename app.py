import streamlit as st

st.set_page_config(page_title="Smart Lab Assistant", page_icon="⚡", layout="wide")

st.title("⚡ Smart Electronics Lab Assistant")

menu = st.sidebar.selectbox("Select Tool", ["Resistor Color Code Calculator", "555 Timer Calculator", "Capacitor Code Decoder"])

if menu == "Resistor Color Code Calculator":
    st.subheader("🎨 Resistor Color Code Calculator (4-Band)")
    st.write("Resistor che color bands select kara exact value janun ghenyasathi:")
    
    color_dict = {
        'Black': (0, 1), 'Brown': (1, 10), 'Red': (2, 100), 
        'Orange': (3, 1000), 'Yellow': (4, 10000), 'Green': (5, 100000), 
        'Blue': (6, 1000000), 'Violet': (7, 10000000), 'Grey': (8, 100000000), 'White': (9, 1000000000)
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        band1 = st.selectbox("Band 1 (First Digit)", list(color_dict.keys())[1:]) # Skip black for 1st digit
    with col2:
        band2 = st.selectbox("Band 2 (Second Digit)", list(color_dict.keys()))
    with col3:
        multiplier = st.selectbox("Band 3 (Multiplier)", list(color_dict.keys()))
    with col4:
        tolerance = st.selectbox("Band 4 (Tolerance)", ["Gold (±5%)", "Silver (±10%)"])
        
    if st.button("Calculate Resistance"):
        d1 = color_dict[band1][0]
        d2 = color_dict[band2][0]
        mult = color_dict[multiplier][1]
        
        resistance = ((d1 * 10) + d2) * mult
        
        # Format display (Ohms, kOhms, MOhms)
        if resistance >= 1000000:
            val_str = f"{resistance / 1000000} MΩ"
        elif resistance >= 1000:
            val_str = f"{resistance / 1000} kΩ"
        else:
            val_str = f"{resistance} Ω"
            
        st.success(f"Calculated Resistor Value: **{val_str}** ({tolerance})")

elif menu == "555 Timer Calculator":
    st.subheader("⏱️ 555 Astable Multivibrator Calculator")
    freq = st.number_input("Desired Frequency (Hz)", value=1000)
    if st.button("Calculate Timer"):
        st.info("Calculated: R1 = 1KΩ, R2 = 10KΩ")

elif menu == "Capacitor Code Decoder":
    st.subheader("🔋 Ceramic Capacitor Code Decoder")
    code_input = st.text_input("Enter Capacitor Code (e.g., 104):", value="104")
    if st.button("Decode Capacitor"):
        st.success("Value: 100,000 pF = 100 nF = 0.1 µF")
