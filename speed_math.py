import streamlit as st
import streamlit.components.v1 as components
import random
from fpdf import FPDF
import io
import os

# --- 1. PDF ENGINE (MULTI-PAGE SUPPORT) ---
class GlobalMathPDF(FPDF):
    def __init__(self, format='Letter'):
        super().__init__(orientation='P', unit='mm', format=format)
        
    def setup_fonts(self, font_name):
        font_files = {
            "CourierPrime": ("CourierPrime-Regular.ttf", "CourierPrime-Bold.ttf"),
            "Roboto": ("Roboto-Regular.ttf", "Roboto-Bold.ttf"),
            "Lora": ("Lora-Regular.ttf", "Lora-Bold.ttf")
        }
        if font_name not in font_files: return False
        reg, bld = font_files[font_name]
        reg_p, bld_p = f"fonts/{reg}", f"fonts/{bld}"
        if not os.path.exists(reg_p): return False
        self.add_font(font_name, '', reg_p)
        self.add_font(font_name, 'B', bld_p)
        return True

    def generate_content(self, title, school, teacher, problems, f_size, f_name, col_gap, row_gap, is_key=False):
        # คำนวณจำนวนข้อต่อหน้า (อ้างอิงจากระยะที่ User ปรับ)
        # พื้นที่ใช้งานแนวตั้งประมาณ 220mm (หัก Header/Footer)
        row_h_mm = 15 + (row_gap / 4) 
        probs_per_page = int(220 / row_h_mm) * 4
        
        for i in range(0, len(problems), probs_per_page):
            self.add_page()
            page_probs = problems[i : i + probs_per_page]
            
            # Header
            self.set_font(f_name, 'B', 16)
            self.cell(0, 10, school.upper(), ln=True, align='C')
            self.set_font(f_name, 'B', f_size + 4)
            self.cell(0, 15, f"{title}{' (Key)' if is_key else ''}", ln=True, align='C')
            self.set_font(f_name, '', 10)
            self.cell(90, 10, f"Teacher: {teacher}")
            self.cell(0, 10, "Name: ________________ Score: ____", align='R', ln=True)
            self.line(10, 48, self.w - 10, 48)

            # Grid Render
            col_w_mm = (self.w - 30) / 4 + (col_gap / 15)
            for idx, p in enumerate(page_probs):
                x = 15 + (idx % 4) * col_w_mm
                y = 65 + (idx // 4) * row_h_mm
                
                self.set_xy(x, y)
                self.set_font(f_name, '', 8); self.cell(5, 5, f"{i+idx+1})")
                self.set_font(f_name, 'B', f_size)
                self.set_xy(x+5, y); self.cell(20, 10, f"{p['a']:>3}", align='R', ln=True)
                self.set_xy(x+5, y+8); self.cell(20, 10, f"+ {p['b']:>2}", align='R', ln=True)
                self.set_line_width(0.6)
                self.line(x+10, y+19, x+25, y+19)
                
                if is_key:
                    self.set_text_color(220, 0, 0)
                    self.set_xy(x+5, y+21); self.cell(20, 10, f"{p['a']+p['b']:>3}", align='R')
                    self.set_text_color(0, 0, 0)

# --- 2. MAIN APP ---
def run_app():
    st.title("⚡ MathPrepAI: Professional Synchronizer")

    with st.sidebar:
        st.header("📏 Layout Control")
        paper = st.selectbox("Format", ["Letter", "A4"])
        font_style = st.selectbox("Font", ["CourierPrime", "Roboto", "Lora"])
        f_size = st.slider("Font Size", 16, 32, 24)
        col_gap = st.slider("Column Spacing", 0, 100, 30)
        row_gap = st.slider("Row Spacing", 0, 100, 40)
        
        st.header("🔢 Content")
        num_probs = st.number_input("Total Problems", 1, 200, 48)
        
        st.header("🏫 Branding")
        school = st.text_input("School", "GLOBAL ACADEMY")
        teacher = st.text_input("Teacher", "Mr. Smith")
        title = st.text_input("Title", "Vertical Addition")

    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle Numbers"):
        st.session_state.current_math = [{"a": random.randint(10, 99), "b": random.randint(10, 99)} for _ in range(num_probs)]

    # --- 3. SYNC PREVIEW LOGIC ---
    font_css = "'Courier Prime', monospace" if font_style == "CourierPrime" else font_style
    aspect = 1.29 if paper == "Letter" else 1.41
    
    # คำนวณจำนวนข้อต่อหน้าให้ตรงกับ PDF
    row_h_px = 140 + row_gap 
    probs_per_page = 24 # ค่าเริ่มต้นสำหรับการคำนวณ Preview
    
    pages_html = ""
    for p_idx in range(0, len(st.session_state.current_math), probs_per_page):
        page_probs = st.session_state.current_math[p_idx : p_idx + probs_per_page]
        
        items_html = "".join([f"""
            <div style="width: 100px; font-family: {font_css}; color: black; position: relative; margin-bottom: {row_gap}px;">
                <span style="position: absolute; left: -10px; top: 0; font-size: 10px; color: #888;">{p_idx+i+1})</span>
                <table style="width: 75px; margin-left: auto; border-collapse: collapse; font-weight: bold; font-size: {f_size}px;">
                    <tr><td colspan="2" style="text-align: right; padding-right: 5px;">{p['a']}</td></tr>
                    <tr style="border-bottom: 3px solid black;">
                        <td style="text-align: left; width: 25px; vertical-align: bottom; padding-bottom: 2px;">+</td>
                        <td style="text-align: right; padding-right: 5px; padding-bottom: 2px;">{p['b']}</td>
                    </tr>
                </table>
            </div>
        """ for i, p in enumerate(page_probs)])

        pages_html += f"""
        <div class="sheet">
            <div class="header">
                <h2 style="margin: 0;">{school.upper()}</h2>
                <h1 style="margin: 10px 0;">{title}</h1>
                <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: bold;">
                    <span>Teacher: {teacher}</span>
                    <span>Name: ________________ Score: ____</span>
                </div>
            </div>
            <div class="grid" style="column-gap: {col_gap}px;">{items_html}</div>
            <div class="footer">Page {p_idx//probs_per_page + 1}</div>
        </div>
        """

    full_html = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@700&family=Roboto:wght@700&family=Lora:wght@700&display=swap');
        body {{ background: #555; display: flex; flex-direction: column; align-items: center; padding: 20px; margin: 0; }}
        .sheet {{ width: 750px; height: {750 * aspect}px; background: white; padding: 50px; margin-bottom: 30px; position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow: hidden; box-sizing: border-box; }}
        .header {{ text-align: center; border-bottom: 2px solid black; margin-bottom: 30px; font-family: sans-serif; }}
        .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); }}
        .footer {{ position: absolute; bottom: 20px; right: 50px; font-size: 12px; font-family: sans-serif; }}
    </style>
    {pages_html}
    """
    
    components.html(full_html, height=800, scrolling=True)

    # --- 4. EXPORT ---
    st.markdown("---")
    pdf = GlobalMathPDF(format=paper)
    if pdf.setup_fonts(font_style):
        # สร้างไฟล์ PDF ตาม Logic หน้าเดียวกับพรีวิว
        pdf.generate_content(title, school, teacher, st.session_state.current_math, f_size, font_style, col_gap, row_gap, False)
        # เพิ่มหน้าเฉลย
        pdf.generate_content(title, school, teacher, st.session_state.current_math, f_size, font_style, col_gap, row_gap, True)
        
        st.download_button("📥 Download Multi-Page PDF", data=bytes(pdf.output()), file_name=f"{title}.pdf")

if __name__ == "__main__":
    run_app()
