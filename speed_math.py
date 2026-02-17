import streamlit as st
import random
from fpdf import FPDF

# --- PROFESSIONAL PDF CLASS ---
class ProMathPDF(FPDF):
    def worksheet_header(self, title, school, teacher, font_size):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font('Helvetica', 'B', font_size + 6)
        self.cell(0, 15, title, ln=True, align='C')
        self.set_font('Helvetica', '', 10)
        self.cell(100, 10, f"Teacher: {teacher}", ln=False)
        self.cell(0, 10, "Name: __________________________  Score: ______", ln=True, align='R')
        self.line(10, 48, 200, 48) # Professional Divider Line
        self.ln(12)

def run_app():
    st.title("⚡ Speed Math Pro: Ultimate Designer")
    tier = st.session_state.get('tier', "Free Tier")
    is_pro = tier != "Free Tier (Teaching Only)"

    # --- ADVANCED SIDEBAR (เหมือนในรูป image_facce2) ---
    with st.sidebar:
        st.header("🎨 Page Settings")
        ws_title = st.text_input("Worksheet Title", "Vertical Addition Mastery")
        school = st.text_input("School / Academy Name", "Global Math Prep")
        teacher = st.text_input("Teacher Name", "Prof. Anderson")
        
        st.subheader("🔢 Logic & Grid")
        num_probs = st.slider("Total Problems", 12, 60, 40)
        cols_count = st.radio("Columns per Row", [3, 4, 5], index=1)
        
        st.subheader("📏 Spacing & Font")
        font_size = st.slider("Math Font Size", 14, 32, 22)
        row_padding = st.slider("Vertical Padding (mm)", 10, 50, 30)

    # --- RENDER PROFESSIONAL PREVIEW ---
    st.subheader("📄 Worksheet Live Preview")
    
    # วาดกระดาษจำลอง (Simulation)
    st.markdown(f"""
        <div style="border: 1px solid #ddd; padding: 40px; background: white; color: black; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <div style="text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px;">
                <h3 style="margin:0;">{school.upper()}</h3>
                <h1 style="margin: 10px 0; font-size: {font_size + 10}px;">{ws_title}</h1>
                <div style="display: flex; justify-content: space-between; font-weight: bold;">
                    <span>Teacher: {teacher}</span>
                    <span>Name: ____________________ Score: ____</span>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat({cols_count}, 1fr); gap: {row_padding}px;">
                {" ".join([f"<div style='text-align: right; font-family: Courier; font-size: {font_size}px;'>{i+1})<br>44<br>+13<br><hr style='border:1px solid black;'></div>" for i in range(num_probs)])}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- INSTANT PDF EXPORT ---
    st.markdown("---")
    if is_pro:
        # (ตรรกะสร้าง PDF 2 หน้าเหมือนเดิม แต่ปรับ Layout ให้เป๊ะตาม Preview)
        st.button("📥 Download Professional PDF (Worksheet + Key)")
