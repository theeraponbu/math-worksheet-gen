import streamlit as st
import random
from fpdf import FPDF
import io

# --- 1. PDF CLASS CONFIG ---
class GlobalMathPDF(FPDF):
    def __init__(self, format='Letter'):
        super().__init__(orientation='P', unit='mm', format=format)

    def draw_page(self, title, school, teacher, problems, font_size, scale):
        self.add_page()
        # Header Section
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font('Helvetica', 'B', font_size + 4)
        self.cell(0, 15, title, ln=True, align='C')
        
        # Info Row
        self.set_font('Helvetica', '', 10)
        self.cell(95, 10, f"Teacher: {teacher}", ln=False)
        self.cell(0, 10, "Name: _________________ Score: ____", ln=True, align='R')
        self.line(10, 48, self.w - 10, 48) # เส้นคั่น
        self.ln(10)

        # Grid Setup (4 Columns)
        col_w = (self.w - 30) / 4
        row_h = 30 * (scale/100)
        self.set_font('Helvetica', 'B', font_size)
        
        for idx, p in enumerate(problems):
            x = 15 + (idx % 4) * col_w
            y = 60 + (idx // 4) * row_h
            
            self.set_xy(x, y)
            self.set_font('Helvetica', '', 8)
            self.cell(5, 5, f"{idx+1})") # เลขข้อ
            
            self.set_font('Helvetica', 'B', font_size)
            self.set_xy(x + 5, y)
            self.cell(20, 10, f"{p['a']:>3}", ln=True, align='R')
            self.set_xy(x + 5, y + 8)
            self.cell(20, 10, f"+ {p['b']:>2}", ln=True, align='R')
            self.line(x + 10, y + 18, x + 28, y + 18) # เส้นบวก

def generate_problems(count):
    return [{"a": random.randint(10, 99), "b": random.randint(10, 99), "ans": 0} for _ in range(count)]

# --- 2. MAIN APP ---
def run_app():
    st.title("⚡ Speed Math Pro: Global Designer")
    
    # ดึงค่าสิทธิ์ (เราจะให้ผ่านเพื่อทดสอบดาวน์โหลด)
    tier = st.session_state.get('tier', "Commercial Enterprise (Full Access)")

    with st.sidebar:
        st.header("📄 Page Setup")
        paper_size = st.selectbox("Standard", ["Letter", "A4"])
        content_scale = st.slider("Scale (%)", 70, 130, 100)
        num_probs = st.slider("Problems", 12, 40, 24)
        font_size = st.slider("Font Size", 16, 28, 22)
        
        st.header("🏫 Branding")
        school = st.text_input("School", "Global Academy")
        teacher = st.text_input("Teacher", "Mr. Smith")
        ws_title = st.text_input("Title", "Vertical Addition")

    # Generate Logic
    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle"):
        st.session_state.current_math = generate_problems(num_probs)

    # --- ACTION: DOWNLOAD SYSTEM (The "Pass" Test) ---
    st.markdown("---")
    
    # 1. สร้าง PDF Object
    pdf = GlobalMathPDF(format=paper_size)
    pdf.draw_page(ws_title, school, teacher, st.session_state.current_math, font_size, content_scale)
    
    # 2. แปลงเป็น Bytes ด้วยวิธีที่ชัวร์ที่สุด
    try:
        # ใช้คำสั่ง output(dest='S') เพื่อดึงข้อมูลออกมาเป็น Raw String/Bytes ทันที
        pdf_output = pdf.output() 
        pdf_bytes = bytes(pdf_output) if isinstance(pdf_output, (bytearray, bytes)) else pdf_output
        
        st.download_button(
            label="📥 Download Professional PDF (Ready to Print)",
            data=pdf_bytes,
            file_name=f"{ws_title.replace(' ', '_')}.pdf",
            mime="application/pdf",
            key="download_btn_final"
        )
        st.success("✅ PDF Engine Ready: Click to download instantly.")
    except Exception as e:
        st.error(f"Engine Error: {e}")

    # Simplified Preview for Screen
    st.info("A4/Letter Preview is shown below. PDF will be pixel-perfect.")
    st.write(f"Displaying {num_probs} problems in {paper_size} format.")
