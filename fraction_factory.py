import streamlit as st
import matplotlib.pyplot as plt

def run_app():
    tier = st.session_state.get('tier', "Free Tier (Teaching Only)")
    
    st.title("🧩 Fraction Factory: Ultimate")

    # --- SETUP GOOGLE FONTS (CSS) ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Comic+Neue:wght@700&family=Lexend:wght@400;700&family=Playfair+Display:ital,wght@0,700;1,700&family=Patrick+Hand&display=swap');
        </style>
    """, unsafe_allow_html=True)

    col_config, col_preview = st.columns([1, 1.2])

    with col_config:
        st.subheader("🔠 Typography & Style")
        
        # คลังฟอนต์ยอดนิยม 10 แบบ
        fonts = {
            "Standard (Sans-Serif)": "sans-serif",
            "Montserrat (Modern)": "'Montserrat', sans-serif",
            "Playfair (Academic)": "'Playfair Display', serif",
            "Comic Neue (Friendly)": "'Comic Neue', cursive",
            "Patrick Hand (Handwriting)": "'Patrick Hand', cursive",
            "Lexend (Dyslexia Friendly)": "'Lexend', sans-serif"
        }

        # การคุมสิทธิ์เข้าถึงฟอนต์
        if tier == "Free Tier (Teaching Only)":
            selected_font = st.selectbox("Font Style (Free: Standard only)", ["Standard (Sans-Serif)"])
            font_size = 24
            font_color = "#1e293b"
            st.caption("🔒 Upgrade to Pro to unlock 10+ Premium Fonts & Colors")
        else:
            selected_font = st.selectbox("Select Font Style", list(fonts.keys()))
            font_size = st.slider("Heading Size", 18, 48, 28)
            font_color = st.color_picker("Text Color", "#3b82f6")

        st.subheader("🔢 Math Content")
        den = st.number_input("Denominator", 1, 12, 4)
        num = st.number_input("Numerator", 0, den, 1)

    with col_preview:
        st.subheader("🖼️ Professional Preview")
        
        # --- LOGIC: สิทธิ์การใช้งานและลายน้ำ ---
        watermark = ""
        licensing_text = "Personal Use Only"
        
        if tier == "Free Tier (Teaching Only)":
            watermark = '<div style="color:red; opacity:0.3; text-align:center;">Free Version - Teaching Only</div>'
            licensing_text = "Restricted: Classroom Teaching Only"
        elif tier == "Personal Pro (Personal Use)":
            licensing_text = "Licensed to: [User Name] - No Redistribution"
        else: # Commercial
            licensing_text = "Commercial License: Authorized for Resale (TpT/Etsy)"

        # --- PREVIEW RENDER ---
        font_family = fonts[selected_font]
        
        st.markdown(f"""
            <div style="border: 2px solid {font_color}; padding: 20px; border-radius: 5px; background: white;">
                <h1 style="font-family: {font_family}; color: {font_color}; font-size: {font_size}px; text-align: center;">
                    Fraction Practice
                </h1>
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 20px;">
                    <span>Name: ____________________</span>
                    <span>Date: __________</span>
                </div>
                {watermark}
                <div style="text-align: center; margin: 30px 0;">
                    <p style="font-family: {font_family};">Shade the circle to show <b>{num}/{den}</b></p>
                </div>
                <hr>
                <div style="font-size: 10px; color: gray; text-align: right;">
                    {licensing_text} | MathPrepAI Pro
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- EXPORT ACTIONS ---
    st.markdown("---")
    if tier == "Commercial Enterprise (Full Access)":
        st.success("✅ Commercial Rights Active: High-Resolution SVG/PDF Export Unlocked")
        st.button("📥 Download Multi-Page Commercial Package")
    elif tier == "Personal Pro (Personal Use)":
        st.info("✅ Personal Pro: Clean PDF Export (No Watermark)")
        st.button("📥 Download PDF Worksheet")
    else:
        st.warning("⚠️ Free Tier: Downloads Disabled. Upgrade for PDF access.")
        st.button("📥 Download (Locked)", disabled=True)
