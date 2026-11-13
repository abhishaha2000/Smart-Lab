import streamlit as st
import math

st.set_page_config(page_title="Smart Electronics Lab Assistant", page_icon="⚡", layout="wide")

st.title("⚡ Smart Electronics Lab Assistant & Advanced Calculators")
st.markdown("A professional digital lab tool for E&TC students and electronics hobbyists.")

# Expanded Sidebar Navigation for All Lab Tools
tool = st.sidebar.selectbox("Select Lab Tool", [
    "🎨 Resistor Color Code Calculator",
    "💡 LED Series Resistor Calculator",
    "🔋 Capacitor Code Decoder",
    "⏱️ 555 Timer Frequency Calculator",
    "⚡ Voltage Divider Calculator",
    "🎛️ RC Filter Cutoff Frequency Calculator",
    "📈 Op-Amp Gain Calculator (Inverting/Non-Inverting)",
    "🔌 Transistor & IC Pinout Reference"
])

# 1. Resistor Calculator
if tool == "🎨 Resistor Color Code Calculator":
    st.subheader("🎨 4-Band Resistor Value Calculator")
    st.write("Select the color bands below to calculate the exact resistance value:")
    
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
            
        st.success(f"🎯 Calculated Resistor Value: **{val_str}** ({tolerance})")

# 2. LED Series Resistor Calculator
elif tool == "💡 LED Series Resistor Calculator":
    st.subheader("💡 LED Current Limiting Resistor Calculator")
    st.write("Calculate the exact resistor value required to protect an LED in your circuit:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        v_source = st.number_input("Supply Voltage (Vcc in Volts)", value=5.0)
    with col2:
        v_led = st.number_input("LED Forward Voltage (Vf in Volts)", value=2.0)
    with col3:
        i_led = st.number_input("LED Current (Iled in mA)", value=20.0)
        
    if st.button("Calculate LED Resistor"):
        if v_source > v_led:
            resistor_ohms = (v_source - v_led) / (i_led / 1000.0)
            st.success(f"🎯 Required Resistor Value: **{resistor_ohms:.2f} Ω** (Standard closest value: {round(resistor_ohms, -1)} Ω)")
        else:
            st.error("Supply Voltage must be greater than LED Forward Voltage!")

# 3. Capacitor Code Decoder
elif tool == "🔋 Capacitor Code Decoder":
    st.subheader("🔋 Ceramic Capacitor Code Decoder")
    st.write("Enter the 3-digit code printed on the ceramic capacitor:")
    
    code_input = st.text_input("Enter Capacitor Code (e.g., 104, 222):", value="104")
    
    if st.button("Decode Capacitor"):
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

# 4. 555 Timer Frequency Calculator
elif tool == "⏱️ 555 Timer Frequency Calculator":
    st.subheader("⏱️ 555 Astable Multivibrator Calculator")
    st.write("Calculate output frequency and time period for IC 555 in Astable mode:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        r1_k = st.number_input("Resistor R1 (in kΩ)", value=1.0)
    with col2:
        r2_k = st.number_input("Resistor R2 (in kΩ)", value=10.0)
    with col3:
        c_uf = st.number_input("Capacitor C (in µF)", value=0.1)
        
    if st.button("Calculate Frequency"):
        r1 = r1_k * 1000
        r2 = r2_k * 1000
        c = c_uf / 1000000
        
        frequency = 1.44 / ((r1 + (2 * r2)) * c)
        
        if frequency >= 1000:
            freq_str = f"{frequency / 1000:.2f} kHz"
        else:
            freq_str = f"{frequency:.2f} Hz"
            
        st.success(f"🎯 Output Frequency: **{freq_str}**")
        st.info(f"Time Period (T): {1/frequency:.4f} seconds")

# 5. Voltage Divider Calculator (NEW)
elif tool == "⚡ Voltage Divider Calculator":
    st.subheader("⚡ Voltage Divider Circuit Calculator")
    st.write("Calculate the output voltage ($V_{out}$) across resistor $R_2$:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        vin = st.number_input("Input Voltage ($V_{in}$ in Volts)", value=12.0)
    with col2:
        r1_val = st.number_input("Resistor $R_1$ (in kΩ)", value=10.0)
    with col3:
        r2_val = st.number_input("Resistor $R_2$ (in kΩ)", value=10.0)
        
    if st.button("Calculate Vout"):
        # Vout = Vin * (R2 / (R1 + R2))
        vout = vin * (r2_val / (r1_val + r2_val))
        st.success(f"🎯 Output Voltage ($V_{out}$): **{vout:.3f} V**")
        st.info(f"Current flowing through circuit: **{(vin / ((r1_val + r2_val) * 1000)) * 1000:.3f} mA**")

# 6. RC Filter Cutoff Frequency Calculator (NEW)
elif tool == "🎛️ RC Filter Cutoff Frequency Calculator":
    st.subheader("🎛️ RC Low-Pass / High-Pass Filter Calculator")
    st.write("Calculate the cutoff (corner) frequency ($f_c$) for an RC filter:")
    
    col1, col2 = st.columns(2)
    with col1:
        r_ohms = st.number_input("Resistor $R$ (in Ohms)", value=1000.0)
    with col2:
        c_nf = st.number_input("Capacitor $C$ (in nanofarads - nF)", value=100.0)
        
    if st.button("Calculate Cutoff Frequency"):
        r = r_ohms
        c = c_nf * 1e-9 # Convert nF to Farads
        # fc = 1 / (2 * pi * R * C)
        fc = 1 / (2 * math.pi * r * c)
        
        if fc >= 1000000:
            fc_str = f"{fc / 1000000:.2f} MHz"
        elif fc >= 1000:
            fc_str = f"{fc / 1000:.2f} kHz"
        else:
            fc_str = f"{fc:.2f} Hz"
            
        st.success(f"🎯 Cutoff Frequency ($f_c$): **{fc_str}**")

# 7. Op-Amp Gain Calculator (NEW)
elif tool == "📈 Op-Amp Gain Calculator (Inverting/Non-Inverting)":
    st.subheader("📈 Operational Amplifier (Op-Amp) Gain Calculator")
    mode = st.radio("Select Configuration", ["Inverting Amplifier", "Non-Inverting Amplifier"])
    
    col1, col2 = st.columns(2)
    with col1:
        rin_k = st.number_input("Input Resistor ($R_{in}$ / $R_1$ in kΩ)", value=10.0)
    with col2:
        rf_k = st.number_input("Feedback Resistor ($R_f$ in kΩ)", value=100.0)
        
    if st.button("Calculate Voltage Gain"):
        if mode == "Inverting Amplifier":
            # Gain = - (Rf / Rin)
            gain = - (rf_k / rin_k)
            st.success(f"🎯 Voltage Gain ($A_v$): **{gain:.2f}**")
            st.info("Note: Negative sign indicates phase inversion (180° phase shift).")
        else:
            # Gain = 1 + (Rf / R1)
            gain = 1 + (rf_k / rin_k)
            st.success(f"🎯 Voltage Gain ($A_v$): **{gain:.2f}**")
            st.info("Note: Non-inverting amplifier output is in phase with input.")

# 8. Transistor & IC Pinout Reference
elif tool == "🔌 Transistor & IC Pinout Reference":
    st.subheader("🔌 Transistor & IC Pinout Reference Guide")
    st.write("Select a component to view its exact pin configuration and maximum ratings:")
    
    comp = st.selectbox("Select Component", [
        "BC547 / BC557 Transistor", 
        "2N2222 Transistor", 
        "IC 555 Timer", 
        "IC 741 Operational Amplifier", 
        "IC 7805 / 7812 Voltage Regulator"
    ])
    
    if "BC547" in comp:
        st.write("**Type:** BC547 (NPN) / BC557 (PNP) BJT")
        st.write("**Pinout Configuration (Left to Right, flat face facing you):** Collector (C) - Base (B) - Emitter (E)")
        st.write("**Maximum Ratings:** V_CEO = 45V, I_C = 100mA")
    elif "2N2222" in comp:
        st.write("**Type:** 2N2222 NPN Transistor")
        st.write("**Pinout Configuration:** Emitter - Base - Collector")
        st.write("**Maximum Ratings:** V_CEO = 30V, I_C = 800mA")
    elif "555" in comp:
        st.write("**Description:** Precision Timing Circuit")
        st.write("**Pinout (8-Pin DIP):** 1: GND, 2: Trigger, 3: Output, 4: Reset, 5: Control Voltage, 6: Threshold, 7: Discharge, 8: VCC")
    elif "741" in comp:
        st.write("**Description:** General Purpose Operational Amplifier")
        st.write("**Pinout (8-Pin DIP):** 1: Offset Null, 2: Inverting Input (-), 3: Non-Inverting Input (+), 4: VEE, 5: Offset Null, 6: Output, 7: VCC, 8: NC")
    elif "7805" in comp:
        st.write("**Description:** Fixed Voltage Regulators (+5V / +12V)")
        st.write("**Pinout (TO-220 3-Pin):** 1: Input (VIN), 2: Ground (GND), 3: Output (VOUT)")
