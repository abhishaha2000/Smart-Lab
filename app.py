import streamlit as st
import math

st.set_page_config(page_title="Universal Electronics & Lab Assistant", page_icon="⚡", layout="wide")

st.title("⚡ Comprehensive Digital & Power Electronics Lab Reference")
st.markdown("Search **any Digital IC, Logic Gate, Power Device (SCR/TRIAC/IGBT), or Linear IC** instantly.")

# Comprehensive Master Database for ALL Digital, Linear & Power Electronics Components
master_component_db = {
    # --- DIGITAL LOGIC GATES & ICs (7400 Series) ---
    "7400": {"category": "Digital IC - TTL", "desc": "Quad 2-Input NAND Gate", "pinout": "14-Pin DIP | Pin 7: GND, Pin 14: VCC (+5V)\n- Gate 1: Inputs 1,2 | Output 3\n- Gate 2: Inputs 4,5 | Output 6\n- Gate 3: Inputs 9,10 | Output 8\n- Gate 4: Inputs 12,13 | Output 11"},
    "7402": {"category": "Digital IC - TTL", "desc": "Quad 2-Input NOR Gate", "pinout": "14-Pin DIP | Pin 7: GND, Pin 14: VCC (+5V)\n- Gate 1: Outputs 1 | Inputs 2,3\n- Gate 2: Outputs 4 | Inputs 5,6\n- Gate 3: Outputs 10 | Inputs 8,9\n- Gate 4: Outputs 13 | Inputs 11,12"},
    "7404": {"category": "Digital IC - TTL", "desc": "Hex Inverter (6 NOT Gates)", "pinout": "14-Pin DIP | Pin 7: GND, Pin 14: VCC (+5V)\n- Inverters: Inputs (1, 3, 5, 9, 11, 13) -> Outputs (2, 4, 6, 8, 10, 12)"},
    "7408": {"category": "Digital IC - TTL", "desc": "Quad 2-Input AND Gate", "pinout": "14-Pin DIP | Pin 7: GND, Pin 14: VCC (+5V)\n- Gate 1: Inputs 1,2 | Output 3\n- Gate 2: Inputs 4,5 | Output 6\n- Gate 3: Inputs 9,10 | Output 8\n- Gate 4: Inputs 12,13 | Output 11"},
    "7432": {"category": "Digital IC - TTL", "desc": "Quad 2-Input OR Gate", "pinout": "14-Pin DIP | Pin 7: GND, Pin 14: VCC (+5V)\n- Gate 1: Inputs 1,2 | Output 3\n- Gate 2: Inputs 4,5 | Output 6\n- Gate 3: Inputs 9,10 | Output 8\n- Gate 4: Inputs 12,13 | Output 11"},
    "7486": {"category": "Digital IC - TTL", "desc": "Quad 2-Input Exclusive-OR (XOR) Gate", "pinout": "14-Pin DIP | Pin 7: GND, Pin 14: VCC (+5V)\n- Gate 1: Inputs 1,2 | Output 3\n- Gate 2: Inputs 4,5 | Output 6\n- Gate 3: Inputs 9,10 | Output 8\n- Gate 4: Inputs 12,13 | Output 11"},
    "74266": {"category": "Digital IC - TTL", "desc": "Quad 2-Input Exclusive-NOR (XNOR) Gate", "pinout": "14-Pin DIP | Pin 7: GND, Pin 14: VCC (+5V)"},

    # --- DIGITAL SEQUENTIAL & MSI ICS ---
    "7474": {"category": "Digital IC - Sequential", "desc": "Dual D-Type Positive-Edge-Triggered Flip-Flop", "pinout": "14-Pin DIP | Pin 7: GND, Pin 14: VCC (+5V)\n- Flip-Flop 1: Clear(1), Clock(3), D(2), Preset(4), Q(5), Q'(6)\n- Flip-Flop 2: Clear(13), Clock(11), D(12), Preset(10), Q(9), Q'(8)"},
    "7476": {"category": "Digital IC - Sequential", "desc": "Dual J-K Flip-Flop with Preset and Clear", "pinout": "16-Pin DIP | Pin 8: GND, Pin 16: VCC (+5V)"},
    "7490": {"category": "Digital IC - MSI", "desc": "Decade and Binary Counter", "pinout": "14-Pin DIP | Pin 7: GND, Pin 14: VCC (+5V)\n- Mod-10 ripple counter dividing frequency by 2 and 5."},
    "74138": {"category": "Digital IC - MSI", "desc": "3-to-8 Line Decoder / Demultiplexer", "pinout": "16-Pin DIP | Pin 8: GND, Pin 16: VCC (+5V)"},
    "74151": {"category": "Digital IC - MSI", "desc": "8-to-1 Line Multiplexer (MUX)", "pinout": "16-Pin DIP | Pin 8: GND, Pin 16: VCC (+5V)"},

    # --- CMOS DIGITAL ICS (4000 Series) ---
    "4001": {"category": "Digital IC - CMOS", "desc": "Quad 2-Input NOR Gate", "pinout": "14-Pin DIP | Pin 7: VSS (GND), Pin 14: VDD (VCC: 3V-15V)"},
    "4011": {"category": "Digital IC - CMOS", "desc": "Quad 2-Input NAND Gate", "pinout": "14-Pin DIP | Pin 7: VSS (GND), Pin 14: VDD (VCC)"},
    "4017": {"category": "Digital IC - CMOS", "desc": "Johnson Decade Counter with 10 Decoded Outputs", "pinout": "16-Pin DIP | Pin 8: VSS (GND), Pin 16: VDD (VCC)\n- Outputs Q0-Q9 on pins 3, 2, 4, 7, 10, 1, 5, 6, 9, 11."},

    # --- POWER ELECTRONICS ---
    "SCR": {"category": "Power Electronics", "desc": "Silicon Controlled Rectifier (Thyristor - e.g., TYN616, BT151)", "pinout": "TO-220 Package (Left to Right, front face):\n- Pin 1: Cathode (K)\n- Pin 2: Anode (A)\n- Pin 3: Gate (G)\n- Note: Unidirectional device used for AC power control and rectification."},
    "TRIAC": {"category": "Power Electronics", "desc": "Triode for Alternating Current (e.g., BT136, BTA16)", "pinout": "TO-220 Package (Left to Right):\n- Pin 1: Main Terminal 1 (MT1)\n- Pin 2: Main Terminal 2 (MT2)\n- Pin 3: Gate (G)\n- Note: Bidirectional AC switch for lamp dimmers and fan speed controllers."},
    "IGBT": {"category": "Power Electronics", "desc": "Insulated Gate Bipolar Transistor (e.g., IRG4PC50UD, FGA25N120)", "pinout": "TO-220 / TO-247 Package (Left to Right):\n- Pin 1: Gate (G)\n- Pin 2: Collector (C)\n- Pin 3: Emitter (E)\n- Note: High voltage/current switching in Inverters, SMPS, and EV drives."},
    "MOSFET": {"category": "Power Electronics", "desc": "N-Channel Power MOSFET (e.g., IRF540N)", "pinout": "TO-220 Package (Left to Right, metal tab back):\n- Pin 1: Gate (G)\n- Pin 2: Drain (D)\n- Pin 3: Source (S)\n- Note: High-speed PWM switching and motor drivers."},

    # --- LINEAR & ANALOG ICS ---
    "555": {"category": "Linear IC", "desc": "Precision Timer IC (Astable, Monostable, Bistable)", "pinout": "8-Pin DIP:\n- Pin 1: GND\n- Pin 2: Trigger\n- Pin 3: Output\n- Pin 4: Reset\n- Pin 5: Control Voltage\n- Pin 6: Threshold\n- Pin 7: Discharge\n- Pin 8: VCC"},
    "741": {"category": "Linear IC - Op-Amp", "desc": "General Purpose Operational Amplifier", "pinout": "8-Pin DIP:\n- Pin 1: Offset Null\n- Pin 2: Inverting Input (-)\n- Pin 3: Non-Inverting Input (+)\n- Pin 4: VEE (-Supply)\n- Pin 5: Offset Null\n- Pin 6: Output\n- Pin 7: VCC (+Supply)\n- Pin 8: NC"},
    "324": {"category": "Linear IC - Op-Amp", "desc": "Quad Operational Amplifier (4 independent op-amps)", "pinout": "14-Pin DIP | Pin 7: GND (VEE), Pin 14: VCC"},
    "358": {"category": "Linear IC - Op-Amp", "desc": "Dual Operational Amplifier (2 independent op-amps)", "pinout": "8-Pin DIP | Pin 4: GND, Pin 8: VCC"},
    "7805": {"category": "Voltage Regulator", "desc": "Fixed +5V Positive Voltage Regulator", "pinout": "TO-220: Pin 1: Input (Vin), Pin 2: Ground, Pin 3: Output (+5V)"},
    "7812": {"category": "Voltage Regulator", "desc": "Fixed +12V Positive Voltage Regulator", "pinout": "TO-220: Pin 1: Input (Vin), Pin 2: Ground, Pin 3: Output (+12V)"},

    # --- TRANSISTORS ---
    "BC547": {"category": "Transistor - BJT", "desc": "NPN General Purpose Transistor", "pinout": "TO-92 (Flat face forward, Left to Right): Collector (C) - Base (B) - Emitter (E)"},
    "2N2222": {"category": "Transistor - BJT", "desc": "NPN Switching Transistor", "pinout": "TO-18 / TO-92 (Left to Right): Emitter (E) - Base (B) - Collector (C)"}
}

# Sidebar Navigation Mode
menu_mode = st.sidebar.selectbox("Select Lab Tool", [
    "🔍 Universal IC & Component Search Engine",
    "🔌 Digital Logic Gates & ICs Directory",
    "⚡ Power Electronics (SCR, TRIAC, IGBT)",
    "🎨 Resistor Color Code Calculator",
    "💡 LED Series Resistor Calculator",
    "🔋 Capacitor Code Decoder",
    "⏱️ 555 Timer Frequency Calculator",
    "⚡ Voltage Divider & RC Filters",
    "📈 Op-Amp Gain Calculator"
])

st.sidebar.markdown("---")
st.sidebar.info("E&TC Lab Assistant — All Digital ICs & Power Devices.")

# 1. Universal Search Engine
if menu_mode == "🔍 Universal IC & Component Search Engine":
    st.subheader("🔍 Universal Component & IC Lookup Engine")
    st.write("Type any component name, number, or gate (e.g., `7400`, `7404`, `555`, `SCR`, `TRIAC`, `4017`):")
    
    query = st.text_input("Enter IC Number or Component Name:", value="7400").strip().upper()
    
    match_found = False
    for code, info in master_component_db.items():
        if query in code or query in info["desc"].upper() or query in info["category"].upper():
            match_found = True
            st.success(f"### Component: **{code}**")
            st.write(f"- **Category:** {info['category']}")
            st.write(f"- **Description:** {info['desc']}")
            st.text(f"Pinout & Configuration:\n{info['pinout']}")
            st.markdown("---")
            
    if not match_found and query != "":
        st.warning(f"Component '{query}' not found. Try searching for basic logic gates like 7400, 7404, or power devices like SCR / TRIAC.")

# 2. Digital Logic Gates & ICs Directory
elif menu_mode == "🔌 Digital Logic Gates & ICs Directory":
    st.subheader("🔌 Digital Electronics Logic Gates & IC Directory")
    st.write("Browse standard TTL & CMOS digital integrated circuits:")
    
    digital_keys = [k for k in master_component_db.keys() if "Digital" in master_component_db[k]["category"]]
    selected_ic = st.selectbox("Select Digital IC", digital_keys)
    
    if selected_ic in master_component_db:
        item = master_component_db[selected_ic]
        st.info(f"### **IC {selected_ic}** - {item['desc']}")
        st.write(f"**Category:** {item['category']}")
        st.text(f"**Pinout & Details:**\n{item['pinout']}")

# 3. Power Electronics
elif menu_mode == "⚡ Power Electronics (SCR, TRIAC, IGBT)":
    st.subheader("⚡ Power Electronics Components Guide")
    pwr_keys = [k for k in master_component_db.keys() if master_component_db[k]["category"] == "Power Electronics"]
    selected_pwr = st.selectbox("Select Power Device", pwr_keys)
    
    if selected_pwr in master_component_db:
        item = master_component_db[selected_pwr]
        st.success(f"### **{selected_pwr}** - {item['desc']}")
        st.text(f"**Pinout & Lab Specifications:**\n{item['pinout']}")

# 4. Resistor Calculator
elif menu_mode == "🎨 Resistor Color Code Calculator":
    st.subheader("🎨 4-Band Resistor Value Calculator")
    color_dict = {'Black': (0, 1), 'Brown': (1, 10), 'Red': (2, 100), 'Orange': (3, 1000), 'Yellow': (4, 10000), 'Green': (5, 100000), 'Blue': (6, 1000000), 'Violet': (7, 10000000), 'Grey': (8, 100000000), 'White': (9, 1000000000)}
    c1, c2, c3, c4 = st.columns(4)
    with c1: b1 = st.selectbox("Band 1", list(color_dict.keys())[1:])
    with c2: b2 = st.selectbox("Band 2", list(color_dict.keys()))
    with c3: mult = st.selectbox("Multiplier", list(color_dict.keys()))
    with c4: tol = st.selectbox("Tolerance", ["Gold (±5%)", "Silver (±10%)"])
        
    if st.button("Calculate"):
        res = ((color_dict[b1][0] * 10) + color_dict[b2][0]) * color_dict[mult][1]
        val = f"{res / 1000000} MΩ" if res >= 1000000 else (f"{res / 1000} kΩ" if res >= 1000 else f"{res} Ω")
        st.success(f"🎯 Resistance: **{val}** ({tol})")

# 5. LED Calculator
elif menu_mode == "💡 LED Series Resistor Calculator":
    st.subheader("💡 LED Resistor Calculator")
    vs = st
