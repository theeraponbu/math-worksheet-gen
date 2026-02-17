import streamlit as st
import random
from fpdf import FPDF
import io
import os

# --- 1. PDF ENGINE (STABLE LOCAL FONT & PRECISE ALIGNMENT) ---
class GlobalMathPDF(FPDF):
    def __init__(self, format='Letter'):
        super().__init__(orientation='P', unit='mm', format=format)
        
    def setup_fonts(self, font_name):
        """ดึงฟอนต์จากโฟลเดอร์ fonts ใน GitHub/Host ของอาจารย์โดยตรง"""
        font_files = {
            "CourierPrime": ("CourierPrime-Regular.ttf", "CourierPrime-Bold.ttf"),
            "Roboto": ("Roboto-Regular.ttf", "Roboto-Bold.ttf"),
            "Lora": ("Lora-Regular.ttf", "Lora-Bold.ttf")
        }
        
        reg_name, bold_name = font_files[font_name]
        reg_path = f"fonts/{reg_name}"
        bold_path = f"fonts/{bold_name}"

        if not os.path.exists(reg_path) or not os.path.exists(bold_path):
            st.error(f"⚠️ ไม่พบไฟล์ {reg_name} ในโฟลเดอร์ /fonts กรุณาตรวจสอบบน GitHub")
            return False

        self.add_font(font_name, '', reg_path)
        self.add_font(font_name, 'B', bold_path)
        return True

    def draw_page(self, title, school, teacher, problems, font_size, scale, font_name, is_answer_key=False):
        self.add_page()
        display_title = f"{title} (Answer Key)" if is_answer_key else title
        
        # Header Section
        self.set_font(font_name, 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font(font_name, 'B', font_size + 4)
        self.cell(0, 15, display_title, ln=True, align='C')
        
        # Info row
        self.set_font(font_name, '', 10)
        w = self.w - 20
        self.cell(w/2, 10, f"Teacher: {teacher}", ln=False)
        self.cell(w/2, 10, "Name: _________________ Score: ____", ln=True, align='R')
        self.set_line_width(0.5)
        self.line(10, 48, self.w - 10, 48)
        self.ln(10)

        # Grid logic
        col_w = (self.w - 30) / 4
        row_h = 35 * (scale/100)
        self.set_line_width(0.6)
        
        for idx, p in enumerate(problems):
            x = 15 + (idx % 4) * col_w
            y = 65 + (idx // 4) * row_h
            if y > self.h - 30: break
            
            # 1. เลขข้อ
            self.set_xy(x, y)
            self.set_font(font_name, '', 8)
            self.cell(5, 5, f"{idx+1})")
            
            # 2. ตัวเลขโจทย์
            self.set_font(font_name, 'B', font_size)
            self.set_xy(x + 5, y)
            self.cell(20, 10, f"{p['a']:>3}", ln=True, align='R')
            self.set_xy(x + 5, y + 8)
            self.cell(20, 10, f"+ {p['b']:>2}", ln=True, align='R')
            
            # 3. เส้นคั่นโจทย์ (ปลายขวาตรงกับหลักหน่วยเป๊ะ)
            # เริ่มวาดจาก x+7 เพื่อให้คลุมเครื่องหมายบวก และจบที่ x+25 เพื่อให้ตรงขอบขวาตัวเลข
            self.line(x + 7, y + 19, x + 25, y + 19)

            # 4. เขียนคำตอบ (เฉพาะหน้าเฉลย) - ขยับลงมาให้โปร่ง สวยงาม
            if is_answer_key:
                self.set_text_color(220, 0, 0) # สีแดงคมชัด
                self.set_xy(x + 5, y + 21) # ขยับลงมาไม่ให้เบียดเส้น
                self.cell(20, 10, f"{p['a'] + p['b']:>3}", ln=True, align='R')
                self.set_text_color(0, 0, 0)

# --- 2. MAIN APP ---
def run_app():
    # โหลด CSS สำหรับ Preview
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@700&family=Roboto:wght@700&family=Lora:wght@700&display=swap');
        .main { background-color: #f8f9fa; }
        </style>
    """, unsafe_allow_html=True)

    st.title("⚡ Speed Math Pro: Enterprise Designer")
    
    with st.sidebar:
        st.header("📄 Page Setup")
        paper_size = st.selectbox("Paper Size", ["Letter", "A4"])
        font_choice = st.selectbox("Select Font Style", ["CourierPrime", "Roboto", "Lora"])
        content_scale = st.slider("Content Scale (%)", 70, 130, 100)
        num_probs = st.slider("Problems per Page", 12, 48, 24)
        font_size = st.slider("Math Font Size", 16, 32, 24)
        
        st.header("🏫 Branding")
        school = st.text_input("School Name", "GLOBAL ACADEMY")
        teacher = st.text_input("Teacher", "Mr. Smith")
        ws_title = st.text_input("Worksheet Title", "Vertical Addition")

    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle Problems"):
        st.session_state.current_math = [{"a": random.randint(10, 99), "b": random.randint(10, 99)} for _ in range(num_probs)]

    # --- 3. LIVE DESIGNER PREVIEW (ปรับจูน CSS ให้เป๊ะเหมือน PDF) ---
    css_fonts = {"CourierPrime": "'Courier Prime'", "Roboto": "'Roboto'", "Lora": "'Lora'"}
    current_css = css_fonts[font_choice]
    
    problems_html = ""
    for i, p in enumerate(st.session_state.current_math):
        problems_html += f"""
        <div style="text-align:right; font-size:{font_size}px; font-family:{current_css}; font-weight:bold; width:100px; margin:auto; margin-bottom:25px; position:relative;">
            <span style="position:absolute; left:-10px; top:0; font-size:12px; color:#888; font-weight:normal;">{i+1})</span>
            <div style="padding-right:10px;">
                {p['a']}<br>
                <span style="float:left; padding-left:5px;">+</span>{p['b']}
                <div style="border-bottom:3px solid black; width:70px; margin-left:auto; margin-top:4px;"></div>
            </div>
        </div>
        """

    aspect = 1.29 if paper_size == "Letter" else 1.41
    preview_container = f"""
    <div style="width:720px; height:{720 * aspect}px; background:white; margin:auto; border:1px solid #ddd; border-radius:4px; box-shadow:0 10px 25px rgba(0,0,0,0.05); padding:50px; color:black; overflow:hidden; font-family:{current_css};">
        <div style="text-align:center; border-bottom:2px solid black; padding-bottom:10px; margin-bottom:20px;">
            <div style="font-weight:bold; font-size:18px;">{school.upper()}</div>
            <div style="font-weight:bold; font-size:32px; margin:15px 0;">{ws_title}</div>
            <div style="display:flex; justify-content:space-between; font-size:14px;">
                <span>Teacher: {teacher}</span>
                <span>Name: ________________ Score: ____</span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:25px; transform:scale({content_scale/100}); transform-origin:top center;">
            {all_problems_html if 'all_problems_html' in locals() else problems_html}
        </div>
    </div>
    """
    st.write(preview_container, unsafe_allow_html=True)

    # --- 4. DOWNLOAD SYSTEM (WITH ANSWER KEY) ---
    st.markdown("---")
    pdf = GlobalMathPDF(format=paper_size)
    try:
        if pdf.setup_fonts(font_choice):
            # หน้าที่ 1: โจทย์
            pdf.draw_page(ws_title, school, teacher, st.session_state.current_math, font_size, content_scale, font_choice, False)
            # หน้าที่ 2: เฉลย
            pdf.draw_page(ws_title, school, teacher, st.session_state.current_math, font_size, content_scale, font_choice, True)
            
            pdf_bytes = bytes(pdf.output())
            st.download_button(label="📥 Download Worksheet + Answer Key (PDF)", 
                               data=pdf_bytes, 
                               file_name=f"{ws_title}.pdf", 
                               mime="application/pdf")
            st.success("✅ ระบบสร้างไฟล์ PDF พร้อมใช้งาน (1 หน้าโจทย์ + 1 หน้าเฉลย)")
    except Exception as e:
        st.error(f"Engine Error: {e}")

if __name__ == "__main__":
    run_app()
