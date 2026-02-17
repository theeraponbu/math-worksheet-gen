import streamlit as st
import random
from fpdf import FPDF
import io

# --- 1. PDF ENGINE ---
class GlobalMathPDF(FPDF):
    def __init__(self, format='Letter'):
        super().__init__(orientation='P', unit='mm', format=format)

    def draw_page(self, title, school, teacher, problems, font_size, scale):
        self.add_page()
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font('Helvetica', 'B', font_size + 4)
        self.cell(0, 15, title, ln=True, align='C')
        self.set_font('Helvetica', '', 10)
        self.cell(95, 10, f"Teacher: {teacher}", ln=False)
        self.cell(0, 10, "Name: _________________ Score: ____", ln=True, align='R')
        self.line(10, 48, self.w - 10, 48)
        self.ln(10)

        col_w = (self.w - 30) / 4
        row_h = 35 * (scale/100) # ระยะห่างระหว่างข้อ
        
        for idx, p in enumerate(problems):
            x = 15 + (idx % 4) * col_w
            y = 60 + (idx // 4) * row_h
            if y > self.h - 30: break # ป้องกันหลุดขอบกระดาษ
            
            self.set_xy(x, y)
            self.set_font('Helvetica', '', 8)
            self.cell(5, 5, f"{idx+1})")
            self.set_font('Helvetica', 'B', font_size)
            self.set_xy(x + 5, y)
            self.cell(20, 10, f"{p['a']:>3}", ln=True, align='R')
            self.set_xy(x + 5, y + 8)
            self.cell(20, 10, f"+ {p['b']:>2}", ln=True, align='R')
            self.line(x + 10, y + 18, x + 28, y + 18)

# --- 2. APP LOGIC ---
def run_app():
    st.title("⚡ Speed Math Pro: Global Designer")
    tier = st.session_state.get('tier', "Commercial Enterprise (Full Access)")

    with st.sidebar:
        st.header("📄 Page & Design")
        paper_size = st.selectbox("Standard", ["Letter", "A4"])
        content_scale = st.slider("Content Scale (%)", 70, 130, 100)
        num_probs = st.slider("Problems", 12, 48, 24)
        font_size = st.slider("Math Font Size", 16, 32, 22)
        
        st.header("🏫 Branding")
        school = st.text_input("School", "Global Academy")
        teacher = st.text_input("Teacher", "Mr. Smith")
        ws_title = st.text_input("Title", "Vertical Addition")

    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle"):
        st.session_state.current_math = [{"a": random.randint(10, 99), "b": random.randint(10, 99)} for _ in range(num_probs)]

    # --- 3. LIVE PREVIEW CANVAS (ส่วนที่หายไป) ---
    st.subheader("📄 Live Designer Preview")
    
    # คำนวณสัดส่วนกระดาษ
    aspect_ratio = 1.29 if paper_size == "Letter" else 1.41
    preview_width = 700 
    
    st.markdown(f"""
        <div style="
            width: {preview_width}px; 
            height: {preview_width * aspect_ratio}px; 
            background: white; 
            margin: auto; 
            border: 1px solid #ddd; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            padding: 40px;
            color: black;
            font-family: 'Courier New', Courier, monospace;
            overflow: hidden;
        ">
            <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 20px;">
                <div style="font-weight: bold; font-size: 18px;">{school.upper()}</div>
                <div style="font-weight: bold; font-size: 26px; margin: 10px 0;">{ws_title}</div>
                <div style="display: flex; justify-content: space-between; font-size: 14px;">
                    <span>Teacher: {teacher}</span>
                    <span>Name: ________________ Score: ____</span>
                </div>
            </div>
            
            <div style="
                display: grid; 
                grid-template-columns: repeat(4, 1fr); 
                gap: 30px;
                transform: scale({content_scale/100});
                transform-origin: top center;
            ">
                {" ".join([f"<div style='text-align: right; padding: 10px; font-size: {font_size}px;'>{i+1})<br>{p['a']}<br>+{p['b']}<br><hr style='border:1px solid black;'></div>" for i, p in enumerate(st.session_state.current_math)])}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- 4. DOWNLOAD SYSTEM ---
    st.markdown("---")
    pdf = GlobalMathPDF(format=paper_size)
    pdf.draw_page(ws_title, school, teacher, st.session_state.current_math, font_size, content_scale)
    
    try:
        pdf_bytes = bytes(pdf.output())
        st.download_button(
            label="📥 Download Ready-to-Print PDF",
            data=pdf_bytes,
            file_name=f"{ws_title.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Engine Error: {e}")
