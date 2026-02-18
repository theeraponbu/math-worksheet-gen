import streamlit as st
import streamlit.components.v1 as components
import random
from fpdf import FPDF
import io
import os

# --- 1. PDF ENGINE (STRICT BOX MAPPING) ---
class MathProPDF(FPDF):
    def __init__(self, paper_format='Letter'):
        super().__init__(orientation='P', unit='mm', format=paper_format)
        self.f_family = 'Courier'

    def setup_fonts(self, font_name):
        # แผนที่ฟอนต์เพื่อป้องกัน Error
        font_map = {"CourierPrime": "Courier", "Roboto": "Helvetica", "Lora": "Times"}
        self.f_family = font_map.get(font_name, "Courier")
        return True

    def generate_sheet(self, problems, title, school, teacher, f_size, f_style, col_gap, row_gap, 
                       is_key=False, probs_per_page=24, restart_num=False, show_teacher=True):
        
        style = f_style.replace("Regular", "")
        
        for p_idx in range(0, len(problems), probs_per_page):
            self.add_page()
            page_probs = problems[p_idx : p_idx + probs_per_page]
            
            # --- Header: Fixed 45mm ---
            self.set_font(self.f_family, 'B', 16)
            self.cell(0, 10, school.upper(), ln=True, align='C')
            self.set_font(self.f_family, style, f_size + 4)
            self.cell(0, 12, f"{title}{' (Key)' if is_key else ''}", ln=True, align='C')
            
            self.set_font(self.f_family, '', 10)
            if show_teacher and teacher:
                self.cell(90, 8, f"Teacher: {teacher}")
                self.cell(0, 8, "Name: ________________ Score: ____", align='R', ln=True)
            else:
                self.cell(0, 8, "Name: ________________________________________________ Score: ____", align='L', ln=True)
            self.line(10, 45, self.w - 10, 45)

            # --- BOX LOGIC: ล็อกเนื้อหาในพื้นที่เฉพาะ ---
            # คำนวณความกว้างคอลัมน์และบรรทัดแบบสมมาตร
            col_w = (self.w - 30) / 4 + (col_gap / 20)
            box_h = 25 + (row_gap / 5) # ล็อกความสูงกล่องแต่ละข้อ
            
            for i, p in enumerate(page_probs):
                col_i, row_i = i % 4, i // 4
                x, y = 15 + col_i * col_w, 55 + row_i * box_h
                
                # ลำดับข้อ
                num = (i + 1) if restart_num else (p_idx + i + 1)
                self.set_xy(x, y)
                self.set_font(self.f_family, '', 8); self.cell(5, 5, f"{num})")
                
                # ตัวเลขในกล่อง (ล็อกตำแหน่งสัมพันธ์กับมุมกล่อง x, y)
                self.set_font(self.f_family, style, f_size)
                self.set_xy(x+5, y); self.cell(18, 10, f"{p['a']:>3}", align='R', ln=True)
                self.set_xy(x+5, y+8); self.cell(18, 10, f"+ {p['b']:>2}", align='R', ln=True)
                
                # เส้นคั่นแบบสั้น (Clean Short Line)
                self.set_line_width(0.5)
                self.line(x+11, y+18, x+23, y+18)
                
                if is_key:
                    self.set_text_color(220, 0, 0) # เฉลยสีแดง
                    self.set_xy(x+5, y+19); self.cell(18, 10, f"{p['a']+p['b']:>3}", align='R')
                    self.set_text_color(0, 0, 0)

# --- 2. MATH LOGIC ---
def generate_math_data(num, diff):
    problems, seen = [], set()
    low, high = (1, 9) if diff == "Easy" else (10, 99) if diff == "Medium" else (100, 999)
    while len(problems) < num:
        a, b = random.randint(low, high), random.randint(low, high)
        if (a, b) not in seen:
            problems.append({"a": a, "b": b}); seen.add((a, b))
    return problems

# --- 3. MAIN APP ---
def run_app():
    st.title("⚡ Math Drills: Strict Box Sync")

    with st.sidebar:
        st.header("📐 Design")
        font_name = st.selectbox("Font Family", ["CourierPrime", "Roboto", "Lora"])
        f_style = st.selectbox("Text Weight", ["Regular", "B", "I", "BI"])
        f_size = st.slider("Font Size", 16, 32, 22)
        col_gap = st.slider("Column Space", 0, 100, 30)
        row_gap = st.slider("Row Space", 0, 100, 40)
        
        st.header("📄 Page Control")
        paper = st.selectbox("Format", ["Letter", "A4"])
        probs_per_page = st.selectbox("Items Per Page", [12, 16, 20, 24, 28, 32], index=3)
        num_pages = st.selectbox("Total Pages", [1, 10, 20, 30])
        restart_num = st.checkbox("Restart No. per page", value=False)
        
        st.header("🏫 Branding")
        show_teacher = st.checkbox("Show Teacher Name", value=True)
        school = st.text_input("School", "Global Academy")
        teacher = st.text_input("Teacher", "Mr. Smith")
        title = st.text_input("Title", "Vertical Addition")

    # Business Logic
    total_probs = probs_per_page * num_pages
    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle Data"):
        st.session_state.current_math = generate_math_data(total_probs, "Medium")

    # --- PERFECT SYNC PREVIEW ---
    st.subheader("🖥️ Synchronized Paper View")
    preview_mode = st.radio("Mode:", ["Worksheet", "Answer Key"], horizontal=True)
    
    is_key = (preview_mode == "Answer Key")
    font_css = "monospace" if font_name == "CourierPrime" else "sans-serif"
    aspect = 1.29 if paper == "Letter" else 1.41
    
    items_html = "".join([f"""
        <div style="width: 22%; height: {30 + row_gap/5}px; margin-bottom: 10px; font-family: {font_css}; color: black; font-size: {f_size}px; position: relative;">
            <div style="font-size: 10px; color: #999; text-align: left;">{i+1})</div>
            <div style="text-align: right; padding-right: 15px; font-weight: {'bold' if 'B' in f_style else 'normal'}; font-style: {'italic' if 'I' in f_style else 'normal'};">
                {p['a']}<br>+ {p['b']}<br>
                <div style="border-top: 2.5px solid black; width: 42px; margin-left: auto; margin-top: 1px;"></div>
                <div style="color: #d00; height: 25px;">{p['a']+p['b'] if is_key else '&nbsp;'}</div>
            </div>
        </div>
    """ for i, p in enumerate(st.session_state.current_math[:probs_per_page])])

    # พรีวิวแบบเห็นขอบบน-ล่าง (Realistic Paper View)
    components.html(f"""
        <div style="background: #ccc; display: flex; flex-direction: column; align-items: center; padding: 100px 0; min-height: 1000px; overflow-y: auto;">
            <div style="width: 680px; height: {680 * aspect}px; background: white; padding: 45px; box-shadow: 0 10px 40px rgba(0,0,0,0.4); box-sizing: border-box; flex-shrink: 0;">
                <div style="text-align: center; border-bottom: 2px solid #000; margin-bottom: 15px; color: black; font-family: sans-serif;">
                    <h3 style="margin: 0;">{school.upper()}</h3>
                    <h2 style="margin: 5px 0;">{title}</h2>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: bold; padding: 8px 0;">
                        <span>{"Teacher: " + teacher if show_teacher and teacher else "Name: ________________________________________________"}</span>
                        <span>{ "Name: ________________" if show_teacher else "Score: ____"}</span>
                    </div>
                </div>
                <div style="display: flex; flex-wrap: wrap; justify-content: space-around; align-content: flex-start;">{items_html}</div>
            </div>
            <div style="height: 100px;"></div>
        </div>
    """, height=900)

    # --- EXPORT ---
    st.markdown("---")
    col_ws, col_key = st.columns(2)
    
    with col_ws:
        pdf_ws = MathProPDF(paper_format=paper)
        pdf_ws.setup_fonts(font_name)
        pdf_ws.generate_sheet(st.session_state.current_math, title, school, teacher, f_size, f_style, col_gap, row_gap, False, probs_per_page, restart_num, show_teacher)
        st.download_button("📝 Download Worksheet (PDF)", data=bytes(pdf_ws.output()), file_name=f"{title}.pdf", use_container_width=True)

    with col_key:
        pdf_k = MathProPDF(paper_format=paper)
        pdf_k.setup_fonts(font_name)
        pdf_k.generate_sheet(st.session_state.current_math, title, school, teacher, f_size, f_style, col_gap, row_gap, True, probs_per_page, restart_num, show_teacher)
        st.download_button("🔑 Download Answer Key (PDF)", data=bytes(pdf_k.output()), file_name=f"{title}_Key.pdf", use_container_width=True)

if __name__ == "__main__":
    run_app()
