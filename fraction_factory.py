import streamlit as st
import matplotlib.pyplot as plt
import random
import io

# --- 1. ENGINE: ฟังก์ชันวาดรูป (รองรับทั้งรูปเดียวและตาราง) ---
def draw_fraction_circle(num, den, color='#3b82f6', size=(3, 3)):
    fig, ax = plt.subplots(figsize=size)
    ax.pie([1]*den, colors=[color if i < num else '#ffffff' for i in range(den)], 
           startangle=90, wedgeprops={'edgecolor': 'black', 'linewidth': 1.2})
    plt.axis('off')
    return fig

def draw_fraction_grid(num_items, color):
    # คำนวณแถวและคอลัมน์ (Max 2 คอลัมน์สำหรับ A4)
    rows = (num_items + 1) // 2
    fig, axes = plt.subplots(rows, 2, figsize=(8, 3 * rows))
    axes = axes.flatten()
    
    answers = []
    for i in range(num_items):
        d = random.randint(2, 12)
        n = random.randint(1, d)
        answers.append(f"Q{i+1}: {n}/{d}")
        
        axes[i].pie([1]*d, colors=[color if j < n else '#ffffff' for j in range(d)], 
                    startangle=90, wedgeprops={'edgecolor': 'black', 'linewidth': 1})
        axes[i].set_title(f"Question {i+1}", fontsize=10)
    
    # ซ่อนแกนที่ไม่ได้ใช้
    for j in range(num_items, len(axes)):
        axes[j].axis('off')
        
    plt.tight_layout()
    return fig, answers

# --- 2. MAIN APP FUNCTION ---
def run_app():
    tier = st.session_state.get('tier', "Free Tier (Teaching Only)")
    is_pro = tier != "Free Tier (Teaching Only)"
    is_commercial = tier == "Commercial Enterprise (Full Access)"
    
    st.title("🧩 Fraction Factory: Ultimate Pro")

    # --- SETUP FONTS ---
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

    # --- SIDEBAR: DESIGN & LOGIC ---
    with st.sidebar:
        st.header("🎨 Worksheet Design")
        
        # โหมดการจัดหน้า (Pro Only)
        if is_pro:
            layout_mode = st.radio("Layout Mode", ["Single (Slide)", "Grid (Worksheet)"])
            num_probs = st.slider("Problems per page", 4, 12, 6) if layout_mode == "Grid (Worksheet)" else 1
            selected_font = st.selectbox("Font Style", list(fonts.keys()))
            font_color = st.color_picker("Brand Color", "#3b82f6")
        else:
            st.info("🔒 Grid Mode & Custom Fonts are Pro Features")
            layout_mode = "Single (Slide)"
            num_probs = 1
            selected_font = "Standard"
            font_color = "#1e293b"

    # --- MAIN INTERFACE ---
    col_config, col_preview = st.columns([1, 1.5])

    with col_config:
        st.subheader("🔢 Content Settings")
        if layout_mode == "Single (Slide)":
            den = st.number_input("Denominator", 1, 12, 4)
            num = st.number_input("Numerator", 0, den, 1)
            ws_title = st.text_input("Title", "Fraction Fun")
        else:
            st.write("🎲 Problems will be auto-generated.")
            ws_title = st.text_input("Worksheet Title", "Mixed Fractions Practice")
            if st.button("🔀 Reshuffle Problems"):
                st.rerun()

    with col_preview:
        st.subheader("🖼️ Live Preview")
        
        # --- UI RENDER ---
        font_family = fonts[selected_font]
        licensing = "Commercial License" if is_commercial else ("Personal Pro" if is_pro else "Free - Teaching Only")
        
        # Header Container
        st.markdown(f"""
            <div style="border: 2px solid {font_color}; padding: 15px; border-radius: 10px; background: white; font-family: {font_family};">
                <h2 style="color: {font_color}; text-align: center;">{ws_title}</h2>
                <p style="text-align: right; font-size: 10px; color: gray;">{licensing} | MathPrepAI</p>
                <hr>
            </div>
        """, unsafe_allow_html=True)

        # Drawing Logic
        if layout_mode == "Single (Slide)":
            st.pyplot(draw_fraction_circle(num, den, font_color))
            st.write(f"<p style='text-align:center; font-family:{font_family}'>Shade: {num}/{den}</p>", unsafe_allow_html=True)
        else:
            fig, answers = draw_fraction_grid(num_probs, font_color)
            st.pyplot(fig)
            if is_pro:
                with st.expander("🔑 View Answer Key"):
                    st.write(", ".join(answers))

    # --- 3. EXPORT & CREDIT SYSTEM ---
    st.markdown("---")
    
    if is_pro:
        # ส่วนของสมาชิก Pro หรือ Commercial
        st.success(f"Verified: {tier}")
        if is_commercial:
            st.button("📥 Download Commercial Bundle (Bulk + SVG)")
        else:
            st.button("📥 Download Pro PDF (No Watermark)")
    else:
        # ส่วนของ Free Tier -> แสดง Modal จำลองการเติมเครดิต
        st.warning("⚠️ Free Tier: Customization & Downloads are locked.")
        
        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            if st.button("💳 Use 1 Credit to Download"):
                st.error("You have 0 Credits. Please top up at MathPrepAI.com")
        
        with col_pay2:
            if st.button("💎 Upgrade to Pro (Unlimited)"):
                st.info("Redirecting to Stripe Payment Gateway...")
