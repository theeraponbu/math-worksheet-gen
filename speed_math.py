import streamlit as st
import random
from fpdf import FPDF
import io
import os

# --- 1. PDF ENGINE ---
class GlobalMathPDF(FPDF):
    def __init__(self, format='Letter'):
        super().__init__(orientation='P', unit='mm', format=format)
        
    def setup_fonts(self, font_name):
        font_files = {
            "CourierPrime": ("CourierPrime-Regular.ttf", "CourierPrime-Bold.ttf"),
            "Roboto": ("Roboto-Regular.ttf", "Roboto-Bold.ttf"),
            "Lora": ("Lora-Regular.ttf", "Lora-Bold.ttf")
        }
        reg_name, bold_name = font_files[font_name]
        reg_path, bold_path = f"fonts/{reg_name}", f"fonts/{bold_name}"
        if not os.path.exists(reg_path): return False
        self.add_font(font_name, '', reg_path)
        self.add_font(font_name, 'B', bold_path)
        return True

    def draw_page(self, title, school, teacher, problems, font_size, scale, font_name, is_key=False):
        self.add_page()
        self.set_font(font_name, 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font(font_name, 'B', font_size + 4)
        self.cell(0, 15, f"{title}{' (Key)' if is_key else ''}", ln=True, align='C')
        self.set_font(font_name, '', 10)
        self.cell(90, 10, f"Teacher: {teacher}")
        self.cell(0, 10, "Name: _________________ Score: ____", align='R', ln=True)
        self.line(10, 48, self.w - 10, 48)
        
        col_w, row_h = (self.w - 30) / 4, 35 * (scale/100)
        self.set_line_width(0.6)
        for idx, p in enumerate(problems):
            x, y = 15 + (idx % 4) * col_w, 65 + (idx // 4) * row_h
            if y > self.h - 30: break
            self.set_xy(x, y)
            self.set_font(font_name, '', 8); self.cell(5, 5, f"{idx+1})")
            self.set_font(font_name, 'B', font_size)
            self.set_xy(x+5, y); self.cell(20, 10, f"{p['a']:>3}", align='R', ln=True)
            self.set_xy(x+5, y+8); self.cell(20, 10, f"+ {p['b']:>2}", align='R', ln=True)
            self.line(x+8, y+19, x+25, y+19)
            if is_key:
                self.set_text_color(220, 0, 0)
                self.set_xy(x+5, y+21); self.cell(20, 10, f"{p['a']+p['b']:>3}", align='R')
                self.set_text_color(0, 0, 0)

# --- 2. MAIN APP ---
def run_app():
    st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@700&display=swap');</style>", unsafe_allow_html=True)
    st.title("⚡ Speed Math Pro: Ultimate Designer")

    with st.sidebar:
        st.header("📄 Setup")
        paper = st.selectbox("Format", ["Letter", "A4"])
        font_style = st.selectbox("Font", ["CourierPrime", "Roboto", "Lora"])
        scale = st.slider("Scale (%)", 70, 130, 100)
        num_probs = st.slider("Problems", 12, 48, 24)
        f_size = st.slider("Font Size", 16, 32, 24)
        school = st.text_input("School", "GLOBAL ACADEMY")
        teacher = st.text_input("Teacher", "Mr. Smith")
        title = st.text_input("Title", "Vertical Addition")

    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle"):
        st.session_state.current_math = [{"a": random.randint(10, 99), "b": random.randint(10, 99)} for _ in range(num_probs)]

    # --- 3. REFINED PREVIEW (THE FIX) ---
    st.subheader("📄 Live Preview")
    font_css = "'Courier Prime', monospace" if font_style == "CourierPrime" else font_style
    
    # สร้างโจทย์ทีละข้อแบบสะอาดที่สุด
    prob_html_list = []
    for i, p in enumerate(st.session_state.current_math):
        # ใช้เครื่องหมายเครื่องหมายบวกชิดซ้าย และเส้นคั่นที่พอดี
        item = (
            f'<div style="width:80px; font-family:{font_css}; font-weight:bold; font-size:{f_size}px; text-align:right; position:relative; margin-bottom:25px; color:black;">'
            f'<span style="position:absolute; left:-15px; top:0; font-size:12px; font-weight:normal; color:#888;">{i+1})</span>'
            f'{p["a"]}<br><span style="float:left;">+</span>{p["b"]}'
            f'<div style="border-top:3px solid black; width:65px; margin-top:4px; margin-left:auto;"></div>'
            f'</div>'
        )
        prob_html_list.append(item)
    
    all_probs = "".join(prob_html_list)
    aspect = 1.29 if paper == "Letter" else 1.41
    
    # ใช้คอนเทนเนอร์แบบ Static 100% เพื่อกัน Error
    main_container = f"""
    <div style="width:720px; height:{720 * aspect}px; background:white; border:1px solid #ddd; padding:50px; color:black; margin:auto; overflow:hidden;">
        <div style="text-align:center; border-bottom:2px solid black; margin-bottom:25px; font-family:sans-serif;">
            <h2 style="margin:0; font-size:20px;">{school.upper()}</h2>
            <h1 style="margin:10px 0; font-size:32px;">{title}</h1>
            <div style="display:flex; justify-content:space-between; font-size:14px; font-weight:bold;">
                <span>Teacher: {teacher}</span>
                <span>Name: ________________ Score: ____</span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:30px; transform:scale({scale/100}); transform-origin:top center;">
            {all_probs}
        </div>
    </div>
    """
    st.markdown(main_container, unsafe_allow_html=True)

    # --- 4. PDF DOWNLOAD ---
    st.markdown("---")
    pdf = GlobalMathPDF(format=paper)
    if pdf.setup_fonts(font_style):
        pdf.draw_page(title, school, teacher, st.session_state.current_math, f_size, scale, font_style, False)
        pdf.draw_page(title, school, teacher, st.session_state.current_math, f_size, scale, font_style, True)
        st.download_button("📥 Download PDF (Worksheet + Key)", data=bytes(pdf.output()), file_name=f"{title}.pdf")

if __name__ == "__main__":
    run_app()
