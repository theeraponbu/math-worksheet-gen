import streamlit as st
import random
from fpdf import FPDF
import io

# --- 1. PDF ENGINE (LETTER / A4 SUPPORT) ---
class GlobalMathPDF(FPDF):
    def __init__(self, format='Letter'):
        # Letter: 215.9 x 279.4 mm | A4: 210 x 297 mm
        super().__init__(orientation='P', unit='mm', format=format)

    def draw_page(self, title, school, teacher, problems, font_size, scale):
        self.add_page()
        # Header Styling
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font('Helvetica', 'B', font_size + 4)
        self.cell(0, 15, title, ln=True, align='C')
        
        # Info Bar
        self.set_font('Helvetica', '', 10)
        w = self.w - 20
        self.cell(w/2, 10, f"Teacher: {teacher}", ln=False)
        self.cell(w/2, 10, "Name: _________________ Score: ____", ln=True, align='R')
        self.line(10, 48, self.w - 10, 48)
        self.ln(10)

        # Grid Calculation
        col_w = (self.w - 30) / 4
        row_h = 35 * (scale/100)
        
        for idx, p in enumerate(problems):
            x = 15 + (idx % 4) * col_w
            y = 60 + (idx // 4) * row_h
            
            # ป้องกันการเขียนทับขอบล่างกระดาษ
            if y > self.h - 30: 
                break
            
            self.set_xy(x, y)
            self.set_font('Helvetica', '', 8)
            self.cell(5, 5, f"{idx+1})")
            
            self.set_font('Helvetica', 'B', font_size)
            self.set_xy(x + 5, y)
            self.cell(20, 10, f"{p['a']:>3}", ln=True, align='R')
            self.set_xy(x + 5, y + 8)
            self.cell(20, 10, f"+ {p['b']:>2}", ln=True, align='R')
            self.line(x + 10, y + 18, x + 28, y + 18)

# --- 2. MAIN APP ---
def run_app():
    st.title("⚡ Speed Math Pro: Global Designer")
    
    # ดึงค่าสิทธิ์จาก Session State
    tier = st.session_state.get('tier', "Commercial Enterprise (Full Access)")

    # --- SIDEBAR CONFIGURATION ---
    with st.sidebar:
        st.header("📄 Page Setup")
        paper_size = st.selectbox("Paper Format", ["Letter", "A4"])
        content_scale = st.slider("Content Scale (%)", 70, 130, 100)
        num_probs = st.slider("Number of Problems", 12, 48, 24)
        font_size = st.slider("Math Font Size", 16, 32, 22)
        
        st.header("🏫 Branding")
        school = st.text_input("School Name", "GLOBAL ACADEMY")
        teacher = st.text_input("Teacher", "Mr. Smith")
        ws_title = st.text_input("Worksheet Title", "Vertical Addition")

    # --- LOGIC: PROBLEM GENERATION ---
    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle Problems"):
        st.session_state.current_math = [
            {"a": random.randint(10, 99), "b": random.randint(10, 99)} 
            for _ in range(num_probs)
        ]

    # --- 3. LIVE DESIGNER PREVIEW (FINAL CLEANUP) ---
    st.subheader("📄 Live Designer Preview")
    
    aspect_ratio = 1.29 if paper_size == "Letter" else 1.41
    preview_width = 700 
    
    # รวบรวมโจทย์ทั้งหมดเข้าด้วยกันก่อน เพื่อป้องกัน Tag หลุด
    all_problems_content = ""
    for i, p in enumerate(st.session_state.current_math):
        single_problem = f"""
        <div style="text-align: right; font-size: {font_size}px; font-family: 'Courier New', monospace; margin-bottom: 20px;">
            <span style="float: left; font-size: 12px; color: gray;">{i+1})</span>
            {p['a']}<br>
            +{p['b']}<br>
            <hr style="border: 1px solid black; margin: 3px 0;">
        </div>
        """
        all_problems_content += single_problem

    # แสดงผลใบงานจำลอง
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
            overflow: hidden;
        ">
            <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 20px;">
                <div style="font-weight: bold; font-size: 18px; font-family: Arial;">{school.upper()}</div>
                <div style="font-weight: bold; font-size: 26px; margin: 10px 0; font-family: Arial;">{ws_title}</div>
                <div style="display: flex; justify-content: space-between; font-size: 14px; font-family: Arial;">
                    <span>Teacher: {teacher}</span>
                    <span>Name: ________________ Score: ____</span>
                </div>
            </div>
            <div style="
                display: grid; 
                grid-template-columns: repeat(4, 1fr); 
                gap: 25px;
                transform: scale({content_scale/100});
                transform-origin: top center;
            ">
                {all_problems_content}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- 4. DOWNLOAD SYSTEM ---
    st.markdown("---")
    
    # สร้าง PDF Object
    pdf = GlobalMathPDF(format=paper_size)
    pdf.draw_page(ws_title, school, teacher, st.session_state.current_math, font_size, content_scale)
    
    try:
        # แปลงเป็นไบนารีและส่งให้ปุ่มดาวน์โหลด
        pdf_bytes = bytes(pdf.output())
        
        st.download_button(
            label="📥 Download Professional PDF",
            data=pdf_bytes,
            file_name=f"{ws_title.replace(' ', '_')}.pdf",
            mime="application/pdf",
            key="speed_math_final_dl"
        )
        st.success("✅ Professional PDF is ready for download!")
        
    except Exception as e:
        st.error(f"Engine Error: {e}")

if __name__ == "__main__":
    run_app()
