import streamlit as st
import random
from fpdf import FPDF

# --- 1. PDF ENGINE SUPPORTING MULTIPLE SIZES ---
class GlobalMathPDF(FPDF):
    def __init__(self, format='Letter'):
        # Letter: 215.9 x 279.4 mm | A4: 210 x 297 mm
        super().__init__(orientation='P', unit='mm', format=format)
        self.paper_format = format

    def setup_header(self, title, school, teacher, font_size):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font('Helvetica', 'B', font_size + 6)
        self.cell(0, 15, title, ln=True, align='C')
        self.set_font('Helvetica', '', 10)
        # ปรับความกว้างตามขนาดกระดาษ
        w = self.w - 20
        self.cell(w/2, 10, f"Teacher: {teacher}", ln=False)
        self.cell(w/2, 10, "Name: _________________ Score: ____", ln=True, align='R')
        self.line(10, 48, self.w - 10, 48)
        self.ln(10)

def run_app():
    st.title("⚡ Speed Math Pro: Global Designer")
    tier = st.session_state.get('tier', "Free Tier")
    
    # --- SIDEBAR: DESIGNER TOOLS ---
    with st.sidebar:
        st.header("📄 Page Setup")
        paper_size = st.selectbox("Paper Size Standard", ["Letter (US/Canada)", "A4 (International)"])
        actual_format = 'Letter' if "Letter" in paper_size else 'A4'
        
        st.subheader("🎨 Content Scaling")
        # ส่วนนี้คือความลับที่ทำให้ "ยืดหด" ได้เหมือนเมาส์ลาก
        content_scale = st.slider("Content Scale (%)", 50, 150, 100)
        v_spacing = st.slider("Vertical Spacing", 10, 50, 30)
        h_padding = st.slider("Horizontal Margin", 10, 30, 15)
        
        st.subheader("🔢 Problem Logic")
        ws_title = st.text_input("Title", "Daily Math Sprint")
        num_probs = st.slider("Problems per page", 12, 60, 30)
        font_size = st.slider("Font Size", 14, 36, 22)
        
        st.header("🏫 Branding")
        school = st.text_input("School Name", "Global Academy")
        teacher = st.text_input("Teacher", "Mr. Smith")

    # --- SIMULATED INTERACTIVE CANVAS ---
    # เราฟิกขนาด Container ให้เป็นสัดส่วนกระดาษ แต่ให้ Content ข้างในยืดหยุ่น
    aspect_ratio = 1.29 if actual_format == 'Letter' else 1.41
    paper_width = 800 # pixels for preview
    
    st.subheader(f"📄 Preview: {paper_size}")
    
    # คำนวณขนาดตัวอักษรและระยะห่างตาม Content Scale
    dynamic_font = (font_size * content_scale) / 100
    
    st.markdown(f"""
        <div style="
            width: {paper_width}px; 
            height: {paper_width * aspect_ratio}px; 
            background: white; 
            margin: auto; 
            border: 1px solid #ccc; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            padding: {h_padding}mm;
            color: black;
            font-family: 'Courier New', Courier, monospace;
            position: relative;
            overflow: hidden;
        ">
            <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 20px;">
                <div style="font-weight: bold; font-size: 18px;">{school.upper()}</div>
                <div style="font-weight: bold; font-size: {dynamic_font + 6}px; margin: 10px 0;">{ws_title}</div>
                <div style="display: flex; justify-content: space-between; font-size: 14px;">
                    <span>Teacher: {teacher}</span>
                    <span>Name: ________________ Score: ____</span>
                </div>
            </div>
            
            <div style="
                display: grid; 
                grid-template-columns: repeat(4, 1fr); 
                gap: {v_spacing}px;
                transform: scale({content_scale/100});
                transform-origin: top center;
            ">
                {" ".join([f"<div style='text-align: right; padding: 5px; font-size: {font_size}px;'>{i+1})<br>{random.randint(10,99)}<br>+{random.randint(10,99)}<br><hr style='border:1px solid black;'></div>" for i in range(num_probs)])}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- DOWNLOAD SYSTEM (PRO ONLY) ---
    st.markdown("---")
    if "Pro" in tier or "Commercial" in tier:
        if st.button("📥 Export High-Res PDF (A4/Letter)"):
            st.success(f"Generating {actual_format} PDF with {content_scale}% scale...")
    else:
        st.warning("🔒 Upgrade to Pro to Export PDF in Letter/A4 formats.")
