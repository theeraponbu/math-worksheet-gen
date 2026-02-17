import streamlit as st
import random
from fpdf import FPDF
import io
import os

# --- 1. PDF ENGINE (HIGH FIDELITY) ---
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

    def draw_page(self, title, school, teacher, problems, f_size, scale, f_name, is_key=False):
        self.add_page()
        self.set_font(f_name, 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font(f_name, 'B', f_size + 4)
        self.cell(0, 15, f"{title}{' (Key)' if is_key else ''}", ln=True, align='C')
        self.set_font(f_name, '', 10)
        self.cell(90, 10, f"Teacher: {teacher}")
        self.cell(0, 10, "Name: _________________ Score: ____", align='R', ln=True)
        self.line(10, 48, self.w - 10, 48)
        
        col_w, row_h = (self.w - 30) / 4, 35 * (scale/100)
        self.set_line_width(0.6)
        for idx, p in enumerate(problems):
            x, y = 15 + (idx % 4) * col_w, 65 + (idx // 4) * row_h
            if y > self.h - 30: break
            self.set_xy(x, y)
            self.set_font(f_name, '', 8); self.cell(5, 5, f"{idx+1})")
            self.set_font(f_name, 'B', f_size)
            self.set_xy(x+5, y); self.cell(20, 10, f"{p['a']:>3}", align='R', ln=True)
            self.set_xy(x+5, y+8); self.cell(20, 10, f"+ {p['b']:>2}", align='R', ln=True)
            # ปรับเส้นให้ปลายขวาตรงหลักหน่วยเหมือนหน้าจอ
            self.line(x+10, y+19, x+25, y+19)
            if is_key:
                self.set_text_color(220, 0, 0)
                self.set_xy(x+5, y+21); self.cell(20, 10, f"{p['a']+p['b']:>3}", align='R')
                self.set_text_color(0, 0, 0)

# --- 2. MAIN APP ---
def run_app():
    st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@700&display=swap');</style>", unsafe_allow_html=True)
    st.title("⚡ Speed Math Pro: Enterprise Designer")

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

    # --- 3. THE REFINED PREVIEW (BUG FIX) ---
    st.subheader("📄 Live Designer Preview")
    font_css = "'Courier Prime', monospace" if font_style == "CourierPrime" else font_style
    
    # รวบรวม HTML โจทย์ทีละข้อ
    prob_html_list = []
    for i, p in enumerate(st.session_state.current_math):
        item = f"""
        <div style="width: 100px; margin-bottom: 25px; font-family: {font_css}; color: black; position: relative;">
            <span style="position: absolute; left: -10px; top: 0; font-size: 10px; color: #888; font-weight: normal;">{i+1})</span>
            <table style="width: 75px; margin-left: auto; border-collapse: collapse; font-weight: bold; font-size: {f_size}px; line-height: 1.1;">
                <tr><td colspan="2" style="text-align: right; padding-right: 5px;">{p['a']}</td></tr>
                <tr style="border-bottom: 3px solid black;">
                    <td style="text-align: left; width: 25px; vertical-align: bottom; padding-bottom: 2px;">+</td>
                    <td style="text-align: right; padding-right: 5px; padding-bottom: 2px;">{p['b']}</td>
                </tr>
            </table>
        </div>
        """
        prob_html_list.append(item)
    
    # รวมโจทย์ทั้งหมดและปิด Tag </div> สุดท้ายให้เรียบร้อย
    all_probs_joined = "".join(prob_html_list)
    aspect = 1.29 if paper == "Letter" else 1.41
    
    # หุ้มด้วย div ใบงานเพียงใบเดียวเพื่อความเสถียร
    full_preview_html = f"""
    <div style="width: 750px; height: {750 * aspect}px; background: white; border: 1px solid #ddd; padding: 50px; color: black; margin: auto; overflow: hidden;">
        <div style="text-align: center; border-bottom: 2px solid black; margin-bottom: 30px; font-family: Arial, sans-serif;">
            <h2 style="margin: 0; font-size: 22px;">{school.upper()}</h2>
            <h1 style="margin: 10px 0; font-size: 36px;">{title}</h1>
            <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: bold; color: #444;">
                <span>Teacher: {teacher}</span>
                <span>Name: ________________ Score: ____</span>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; transform: scale({scale/100}); transform-origin: top center;">
            {all_probs_joined}
        </div>
    </div>
    """
    st.write(full_preview_html, unsafe_allow_html=True)

    # --- 4. EXPORT ---
    st.markdown("---")
    pdf = GlobalMathPDF(format=paper)
    if pdf.setup_fonts(font_style):
        pdf.draw_page(title, school, teacher, st.session_state.current_math, f_size, scale, font_style, False)
        pdf.draw_page(title, school, teacher, st.session_state.current_math, f_size, scale, font_style, True)
        st.download_button("📥 Download PDF", data=bytes(pdf.output()), file_name=f"{title}.pdf")

if __name__ == "__main__":
    run_app()
