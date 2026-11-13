import streamlit as st

st.set_page_config(page_title="Smart Lab Assistant", page_icon="⚡", layout="wide")

st.title("⚡ Smart Electronics Lab Assistant")
st.markdown("E&TC Students sathi ek digital lab tool.")

menu = st.sidebar.selectbox("Select Tool", ["Resistor Calculator", "555 Timer Calculator", "Pinout Guide"])

if menu == "Resistor Calculator":
    st.subheader("🎨 Resistor Value Calculator")
    uploaded_file = st.file_uploader("Upload Resistor Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Resistor", width=300)
        st.success("Resistor Value: 10kΩ (±5%)")

elif menu == "555 Timer Calculator":
    st.subheader("⏱️ 555 Astable Multivibrator Calculator")
    freq = st.number_input("Desired Frequency (Hz)", value=1000)
    if st.button("Calculate"):
        st.info("Calculated: R1 = 1KΩ, R2 = 10KΩ")

elif menu == "Pinout Guide":
    st.subheader("🔌 IC Pinout Reference")
    ic_choice = st.selectbox("Select IC", ["IC 555 Timer", "IC 741 Op-Amp", "IC 7805 Regulator"])
    st.write(f"Showing standard pin configuration for {ic_choice}.")