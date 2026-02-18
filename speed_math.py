import streamlit as st
import streamlit.components.v1 as components
import random
from fpdf import FPDF
import io
import os

# --- 1. PDF ENGINE (PRO MULTI-PAGE & FONT SYNC) ---
class GlobalMathPDF(FPDF):
    def __init__(self, format='Letter'):
        super().__init__(orientation='P', unit='mm', format=format)
        
    def setup_fonts(self, font_name):
        # ระบบจัดการฟอนต์ภายนอกเพื่อให้ PDF สวยงามระดับสากล
        font_files = {
            "CourierPrime": ("CourierPrime-Regular.ttf", "CourierPrime-Bold.ttf"),
            "Roboto": ("Roboto-Regular.ttf", "Roboto-Bold.ttf"),
            "Lora": ("Lora-Regular.ttf", "Lora-Bold.ttf")
        }
        if font_name not in font_files: 
            self.set_font('Courier', '', 12) # Fallback
            return True
            
        reg, bld = font_files[font_name]
        reg_p, bld_p = f"fonts/{reg}", f"fonts/{bld}"
        
        if os.path.exists(reg_p):
            self.add_font(font_name, '', reg_p)
            self.add_font(font_name, 'B', bld_p)
            return True
        return False

    def generate_content(self, title, school, teacher, problems, f_size, f_name, col_gap, row_gap, is_key=False):
        # คำนวณจำนวนข้อต่อหน้าโดยอิงจากระยะห่างที่ User ปรับ (Dynamic Layout)
        row_h_mm = 15 + (row_gap / 4) 
        probs_per_page = int(220 / row_h_mm) * 4
        
        for i in range(0, len(problems), probs_per_page):
            self.add_page()
            page_probs = problems[i : i + probs_per_page]
            
            # Header Section
            try: self.set_font(f_name, 'B', 16)
            except: self.set_font('Courier', 'B', 16)
            
            self.cell(0, 10, school.upper(), ln=True, align='C')
            self.set_font(f_name, 'B', f_size + 4)
            self.cell(0, 15, f"{title}{' (Answer Key)' if is_key else ''}", ln=True, align='C')
            
            self.set_font(f_name, '', 10)
            self.cell(90, 10, f"Teacher: {teacher}")
            self.cell(0, 10, "Name: ________________ Score: ____", align='R', ln=True)
            self.line(10, 48, self.w - 10, 48)

            # Grid Render (4 Columns)
            col_w_mm = (self.w - 30) / 4 + (col_gap / 15)
            for idx, p in enumerate(page_probs):
                col_idx = idx % 4
                row_idx = idx // 4
                x = 15 + col_idx * col_w_mm
                y = 65 + row_idx * row_h_mm
                
                self.set_xy(x, y)
                self.set_font(f_name, '', 8); self.cell(5, 5, f"{i+idx+1})")
                self.set_font(f_name, 'B', f_size)
                
                # ตัวเลขตั้งและตัวบวก
                self.set_xy(x+5, y); self.cell(20, 10, f"{p['a']:>3}", align='R', ln=True)
                self.set_xy(x+5, y+8); self.cell(20, 10, f"+ {p['b']:>2}", align='R', ln=True)
                self.set_line_width(0.6)
                self.line(x+10, y+19, x+25, y+19)
                
                if is_key:
                    self.set_text_color(220, 0, 0)
                    self.set_xy(x+5, y+21); self.cell(20, 10, f"{p['a']+p['b']:>3}", align='R')
                    self.set_text_color(0, 0, 0)

# --- 2. MATH LOGIC (REGROUPING & UNIQUE GUARD) ---
def check_regrouping(a, b):
    temp_a, temp_b = a, b
    while temp_a > 0 or temp_b > 0:
        if (temp_a % 10) + (temp_b % 10) >= 10: return True
        temp_a //= 10; temp_b //= 10
    return False

def generate_math_data(num, diff, mode):
    problems, seen = [], set()
    low, high = (1, 9) if diff == "Easy" else (10, 99) if diff == "Medium" else (100, 999)
    
    while len(problems) < num:
        a, b = random.randint(low, high), random.randint(low, high)
        if (a, b) in seen: continue
        
        has_reg = check_regrouping(a, b)
        if (mode == "Always Regrouping" and has_reg) or \
           (mode == "Never Regrouping" and not has_reg) or \
           (mode == "Mixed (Both)"):
            problems.append({"a": a, "b": b})
            seen.add((a, b))
    return problems

# --- 3. MAIN APP ---
def run_app():
    st.set_page_config(layout="wide")
    st.title("⚡ MathPrepAI: Professional Synchronizer")

    with st.sidebar:
        st.header("📏 Layout & Fonts")
        paper = st.selectbox("Format", ["Letter", "A4"])
        font_style = st.selectbox("Font Style", ["CourierPrime", "Roboto", "Lora"])
        f_size = st.slider("Font Size", 16, 32, 24)
        col_gap = st.slider("Column Spacing", 0, 100, 30)
        row_gap = st.slider("Row Spacing", 0, 100, 40)
        
        st.header("🔢 Math Logic")
        diff = st.radio("Difficulty", ["Easy", "Medium", "Hard"])
        mode = st.selectbox("Regrouping Mode", ["Mixed (Both)", "Never Regrouping", "Always Regrouping"])
        num_probs = st.number_input("Total Problems", 12, 200, 48, step=12)
        
        st.header("🏫 Branding")
        school = st.text_input("School", "GLOBAL ACADEMY")
        teacher = st.text_input("Teacher", "Mr. Smith")
        title = st.text_input("Worksheet Title", "Vertical Addition")

    # Generate Data
    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle & Sync"):
        st.session_state.current_math = generate_math_data(num_probs, diff, mode)

    # --- 4. PROFESSIONAL HTML PREVIEW ---
    font_css = "'Courier Prime', monospace" if font_style == "CourierPrime" else font_style
    aspect = 1.29 if paper == "Letter" else 1.41
    
    # คำนวณพรีวิวให้ตรงกับ PDF
    pages_html = ""
    probs_per_page = 24 # ค่ามาตรฐานสำหรับ Preview พื้นฐาน
    
    for p_idx in range(0, len(st.session_state.current_math), probs_per_page):
        page_probs = st.session_state.current_math[p_idx : p_idx + probs_per_page]
        items_html = "".join([f"""
            <div style="width: 100px; font-family: {font_css}; position: relative; margin-bottom: {row_gap}px;">
                <span style="position: absolute; left: -10px; top: 0; font-size: 10px; color: #888;">{p_idx+i+1})</span>
                <table style="width: 75px; margin-left: auto; border-collapse: collapse; font-weight: bold; font-size: {f_size}px; color: black;">
                    <tr><td style="text-align: right;">{p['a']}</td></tr>
                    <tr style="border-bottom: 3px solid black;">
                        <td style="text-align: right;"><span style="float: left;">+</span>{p['b']}</td>
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
        body {{ background: #eee; display: flex; flex-direction: column; align-items: center; padding: 20px; }}
        .sheet {{ width: 750px; height: {750 * aspect}px; background: white; padding: 50px; margin-bottom: 30px; position: relative; box-shadow: 0 5px 15px rgba(0,0,0,0.2); overflow: hidden; box-sizing: border-box; color: black; }}
        .header {{ text-align: center; border-bottom: 2px solid black; margin-bottom: 30px; }}
        .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); }}
        .footer {{ position: absolute; bottom: 20px; right: 50px; font-size: 12px; }}
    </style>
    {pages_html}
    """
    components.html(full_html, height=800, scrolling=True)

    # --- 5. EXPORT (SEPARATED FILES) ---
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    # ฟังก์ชันช่วยสร้าง PDF
    def build_pdf(problems, is_key):
        pdf = GlobalMathPDF(format=paper)
        pdf.setup_fonts(font_style)
        pdf.generate_content(title, school, teacher, problems, f_size, font_style, col_gap, row_gap, is_key)
        return pdf.output()

    with col1:
        st.download_button("📝 Download Worksheet (PDF)", 
                           data=bytes(build_pdf(st.session_state.current_math, False)), 
                           file_name=f"{title}_Worksheet.pdf")
    with col2:
        st.download_button("🔑 Download Answer Key (PDF)", 
                           data=bytes(build_pdf(st.session_state.current_math, True)), 
                           file_name=f"{title}_AnswerKey.pdf")

if __name__ == "__main__":
    run_app()
