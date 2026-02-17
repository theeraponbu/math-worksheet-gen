import streamlit as st
import random

def generate_problems(count, digits, carry):
    problems = []
    for _ in range(count):
        if digits == 1:
            a, b = random.randint(1, 9), random.randint(1, 9)
        else:
            if not carry:
                # Logic for no-carry addition
                a_u, b_u = random.randint(0, 4), random.randint(0, 4)
                a_t, b_t = random.randint(1, 4), random.randint(1, 4)
                a, b = (a_t * 10 + a_u), (b_t * 10 + b_u)
            else:
                a, b = random.randint(10, 99), random.randint(10, 99)
        problems.append({"a": a, "b": b, "ans": a + b})
    return problems

def run_app():
    st.title("⚡ Speed Math Drills: Ultimate Pro")
    tier = st.session_state.get('tier', "Free Tier")
    is_pro = tier != "Free Tier (Teaching Only)"

    # --- 1. SETUP GOOGLE FONTS ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Comic+Neue:wght@700&family=Lexend:wght@400;700&family=Patrick+Hand&display=swap');
        </style>
    """, unsafe_allow_html=True)

    fonts = {
        "Standard": "sans-serif",
        "Montserrat": "'Montserrat', sans-serif",
        "Comic Neue": "'Comic Neue', cursive",
        "Patrick Hand": "'Patrick Hand', cursive",
        "Lexend": "'Lexend', sans-serif"
    }

    # --- 2. SIDEBAR SETTINGS ---
    with st.sidebar:
        st.header("⚙️ Worksheet Config")
        ws_title = st.text_input("Worksheet Title", "Vertical Addition Practice")
        instruction = st.text_area("Instruction", "Solve the following addition problems.")
        
        st.subheader("🔢 Math Settings")
        num_probs = st.slider("Number of Problems", 12, 60, 24)
        digit_type = st.selectbox("Difficulty", ["1-Digit", "2-Digits"])
        allow_carry = st.checkbox("Allow Carry Over", value=True)
        
        st.subheader("🎨 Typography")
        selected_font = st.selectbox("Font Style", list(fonts.keys()))
        font_size = st.slider("Font Size (px)", 14, 32, 20)
        main_color = st.color_picker("Theme Color", "#2e7d32")

    # --- 3. LOGIC & PREVIEW ---
    if 'math_problems' not in st.session_state or st.button("🔀 Reshuffle Problems"):
        digits = 1 if "1" in digit_type else 2
        st.session_state.math_problems = generate_problems(num_probs, digits, allow_carry)

    # Simulated A4 Page Preview
    st.subheader("📄 Worksheet Preview (A4 Layout)")
    font_family = fonts[selected_font]
    
    with st.container():
        # Professional Header
        st.markdown(f"""
            <div style="border: 2px solid {main_color}; padding: 25px; border-radius: 5px; background-color: white; font-family: {font_family};">
                <div style="display: flex; justify-content: space-between; font-weight: bold; color: {main_color};">
                    <span>Name: __________________________</span>
                    <span>Score: ________ / {num_probs}</span>
                </div>
                <h1 style="text-align: center; color: {main_color}; margin-top: 15px;">{ws_title}</h1>
                <p style="text-align: center; font-style: italic;">{instruction}</p>
                <hr style="border: 1px solid {main_color};">
            </div>
        """, unsafe_allow_html=True)

        # Problem Grid (4 items per row)
        cols = st.columns(4)
        for idx, p in enumerate(st.session_state.math_problems):
            with cols[idx % 4]:
                st.markdown(f"""
                    <div style="text-align: right; font-family: monospace; font-size: {font_size}px; padding: 15px; border-bottom: 1px solid #ddd; margin-bottom: 10px;">
                        <span style="float: left; font-size: 12px; color: gray;">{idx+1})</span>
                        &nbsp;&nbsp;{p['a']}<br>
                        +&nbsp;{p['b']}<br>
                        <hr style="margin: 5px 0; border: 1px solid black;">
                        <br>
                    </div>
                """, unsafe_allow_html=True)

    # --- 4. EXPORT & DOWNLOAD ---
    st.markdown("---")
    if is_pro:
        st.success(f"Verified: {tier}")
        if st.button("📥 Download PDF Worksheet"):
            with st.spinner("Generating High-Quality PDF..."):
                # In actual deployment, this connects to the ReportLab/FPDF engine
                st.balloons()
                st.info("PDF Engine: Creating 1 Page Worksheet + 1 Page Answer Key...")
    else:
        st.warning("🔒 PDF Download is locked. Upgrade to Pro to export.")
        st.button("📥 Download (Locked)", disabled=True)
