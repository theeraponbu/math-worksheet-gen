import streamlit as st
import streamlit.components.v1 as components
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
        reg, bld = font_files[font_name]
        reg_p, bld_p = f"fonts/{reg}", f"fonts/{bld}"
        if not os.path.exists(reg_p): return False
        self.add_font(font_name, '', reg_p)
        self.add_font(font_name, 'B', bld_p)
        return True

    def draw_page(self, title, school, teacher, problems, f_size, scale, f_name, col_gap, row_gap, is_key=False):
        self.add_page()
        self.set_font(f_name, 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font(f_name, 'B', f_size + 4)
        self.cell(0, 15, f"{title}{' (Key)' if is_key else ''}", ln=True, align='C')
        self.set_font(f_name, '', 10)
        self.cell(90, 10, f"Teacher: {teacher}")
        self.cell(0, 10, "Name: _________________ Score: ____", align='R', ln=True)
        self.line(10, 48, self.w - 10, 48)
        
        # ปรับระยะตาม User Input (แปลงจาก px เป็น mm โดยประมาณ)
        col_w = (self.w - 30) / 4 + (col_gap / 10)
        row_h = (35 * (scale/100)) + (row_gap / 5)
        
        self.set_line_width(0.6)
        for idx, p in enumerate(problems):
            x, y = 15 + (idx % 4) * col_w, 65 + (idx // 4) * row_h
            if y > self.h - 30: break
            self.set_xy(x, y)
            self.set_font(f_name, '', 8); self.cell(5, 5, f"{idx+1})")
            self.set_font(f_name, 'B', f_size)
            self.set_xy(x+5, y); self.cell(20, 10, f"{p['a']:>3}", align='R', ln=True)
            self.set_xy(x+5, y+8); self.cell(20, 10, f"+ {p['b']:>2}", align='R', ln=True)
            self.line(x+10, y+19, x+25, y+19)
            if is_key:
                self.set_text_color(220, 0, 0)
                self.set_xy(x+5, y+21); self.cell(20, 10, f"{p['a']+p['b']:>3}", align='R')
                self.set_text_color(0, 0, 0)

# --- 2. MAIN APP ---
def run_app():
    st.title("⚡ Speed Math Pro: Custom Spacing Designer")

    with st.sidebar:
        st.header("📄 Page Setup")
        paper = st.selectbox("Format", ["Letter", "A4"])
        font_style = st.selectbox("Font", ["CourierPrime", "Roboto", "Lora"])
        scale = st.slider("Content Scale (%)", 70, 130, 100)
        
        st.header("📏 Spacing (Custom)")
        col_gap = st.slider("Column Gap (px)", 10, 100, 30)
        row_gap = st.slider("Row Gap (px)", 10, 100, 40)
        
        st.header("🔢 Math Settings")
        num_probs = st.slider("Problems", 12, 48, 24)
        f_size = st.slider("Font Size", 16, 32, 24)
        
        st.header("🏫 Branding")
        school = st.text_input("School", "GLOBAL ACADEMY")
        teacher = st.text_input("Teacher", "Mr. Smith")
        title = st.text_input("Title", "Vertical Addition")

    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle"):
        st.session_state.current_math = [{"a": random.randint(10, 99), "b": random.randint(10, 99)} for _ in range(num_probs)]

    # --- 3. COMPONENT-BASED PREVIEW (FIXED BUG) ---
    st.subheader("📄 Live Designer Preview")
    font_css = "'Courier Prime', monospace" if font_style == "CourierPrime" else font_style
    aspect = 1.29 if paper == "Letter" else 1.41
    
    # สร้างโจทย์ด้วยตารางที่เป๊ะที่สุด
    prob_html = "".join([f"""
        <div style="width: 100px; font-family: {font_css}; color: black; position: relative;">
            <span style="position: absolute; left: -10px; top: 0; font-size: 10px; color: #888;">{i+1})</span>
            <table style="width: 75px; margin-left: auto; border-collapse: collapse; font-weight: bold; font-size: {f_size}px;">
                <tr><td colspan="2" style="text-align: right; padding-right: 5px;">{p['a']}</td></tr>
                <tr style="border-bottom: 3px solid black;">
                    <td style="text-align: left; width: 25px; vertical-align: bottom; padding-bottom: 2px;">+</td>
                    <td style="text-align: right; padding-right: 5px; padding-bottom: 2px;">{p['b']}</td>
                </tr>
            </table>
        </div>
    """ for i, p in enumerate(st.session_state.current_math)])

    # HTML ชุดเต็มสำหรับใส่ใน IFrame (Sandbox)
    full_html = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@700&family=Roboto:wght@700&family=Lora:wght@700&display=swap');
        body {{ background: #eee; display: flex; justify-content: center; padding: 20px; margin: 0; }}
        .sheet {{ width: 750px; height: {750 * aspect}px; background: white; padding: 50px; box-sizing: border-box; box-shadow: 0 10px 20px rgba(0,0,0,0.2); overflow: hidden; }}
        .header {{ text-align: center; border-bottom: 2px solid black; margin-bottom: 30px; font-family: sans-serif; }}
        .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); column-gap: {col_gap}px; row-gap: {row_gap}px; transform: scale({scale/100}); transform-origin: top center; }}
    </style>
    <div class="sheet">
        <div class="header">
            <h2 style="margin: 0;">{school.upper()}</h2>
            <h1 style="margin: 10px 0;">{title}</h1>
            <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: bold;">
                <span>Teacher: {teacher}</span>
                <span>Name: ________________ Score: ____</span>
            </div>
        </div>
        <div class="grid">{prob_html}</div>
    </div>
    """
    
    # ใช้ iframe component เพื่อแยก HTML ออกจาก streamlit ป้องกันติ่ง </div>
    components.html(full_html, height=1000, scrolling=True)

    # --- 4. EXPORT ---
    st.markdown("---")
    pdf = GlobalMathPDF(format=paper)
    if pdf.setup_fonts(font_choice := font_style):
        pdf.draw_page(title, school, teacher, st.session_state.current_math, f_size, scale, font_choice, col_gap, row_gap, False)
        pdf.draw_page(title, school, teacher, st.session_state.current_math, f_size, scale, font_choice, col_gap, row_gap, True)
        st.download_button("📥 Download PDF", data=bytes(pdf.output()), file_name=f"{title}.pdf")

if __name__ == "__main__":
    run_app()
