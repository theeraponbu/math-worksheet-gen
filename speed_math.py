import streamlit as st
import streamlit.components.v1 as components
import random
from fpdf import FPDF
from pptx import Presentation
from pptx.util import Inches, Pt
import io
import os

# --- 1. PDF ENGINE (MULTI-PAGE & DYNAMIC HEADER) ---
class MathProPDF(FPDF):
    def __init__(self, paper_format='Letter'):
        super().__init__(orientation='P', unit='mm', format=paper_format)
        self.f_family = 'Courier' # Default

    def setup_fonts(self, font_name):
        # ระบบจัดการฟอนต์มาตรฐาน
        font_map = {"CourierPrime": "Courier", "Roboto": "Helvetica", "Lora": "Times"}
        self.f_family = font_map.get(font_name, "Courier")
        return True

    def generate_sheet(self, problems, title, school, teacher, f_size, f_style, col_gap, row_gap, 
                       is_key=False, probs_per_page=24, restart_num=False, show_teacher=True):
        
        for p_idx in range(0, len(problems), probs_per_page):
            self.add_page()
            page_probs = problems[p_idx : p_idx + probs_per_page]
            
            # --- Header Logic ---
            style = f_style.replace("Regular", "")
            self.set_font(self.f_family, 'B', 16)
            self.cell(0, 10, school.upper(), ln=True, align='C')
            self.set_font(self.f_family, style, f_size + 4)
            self.cell(0, 15, f"{title}{' (Answer Key)' if is_key else ''}", ln=True, align='C')
            
            self.set_font(self.f_family, '', 10)
            if show_teacher:
                self.cell(90, 10, f"Teacher: {teacher}")
                self.cell(0, 10, "Name: ________________ Score: ____", align='R', ln=True)
            else:
                # ถ้าไม่ใส่ชื่อครู ขยับช่องชื่อชิดซ้ายและทำเส้นให้ยาวขึ้น
                self.cell(0, 10, "Name: ________________________________________________ Score: ____", align='L', ln=True)
            
            self.line(10, 48, self.w - 10, 48)

            # --- Grid Layout (4 Columns) ---
            col_w = (self.w - 30) / 4 + (col_gap / 15)
            row_h = 15 + (row_gap / 4)
            
            for i, p in enumerate(page_probs):
                col_i = i % 4
                row_i = i // 4
                x = 15 + col_i * col_w
                y = 65 + row_i * row_h
                
                # Numbering Logic
                num = (i + 1) if restart_num else (p_idx + i + 1)
                
                self.set_xy(x, y)
                self.set_font(self.f_family, '', 8); self.cell(5, 5, f"{num})")
                self.set_font(self.f_family, style, f_size)
                self.set_xy(x+5, y); self.cell(20, 10, f"{p['a']:>3}", align='R', ln=True)
                self.set_xy(x+5, y+8); self.cell(20, 10, f"+ {p['b']:>2}", align='R', ln=True)
                self.line(x+10, y+19, x+25, y+19)
                
                if is_key:
                    self.set_text_color(220, 0, 0) # สีแดงสำหรับเฉลย
                    self.set_xy(x+5, y+21); self.cell(20, 10, f"{p['a']+p['b']:>3}", align='R')
                    self.set_text_color(0, 0, 0)

# --- 2. POWERPOINT ENGINE ---
def build_pptx(problems, title, probs_per_page):
    prs = Presentation()
    for i in range(0, len(problems), probs_per_page):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
        txBox.text_frame.text = f"{title} - Page {int(i/probs_per_page)+1}"
    buffer = io.BytesIO()
    prs.save(buffer)
    return buffer.getvalue()

# --- 3. MATH LOGIC (UNIQUE GUARD) ---
def generate_math_data(num, diff):
    problems, seen = [], set()
    low, high = (1, 9) if diff == "Easy" else (10, 99) if diff == "Medium" else (100, 999)
    while len(problems) < num:
        a, b = random.randint(low, high), random.randint(low, high)
        if (a, b) not in seen:
            problems.append({"a": a, "b": b})
            seen.add((a, b))
    return problems

# --- 4. MAIN APP ---
def run_app():
    st.set_page_config(page_title="MathPrepAI Global", layout="wide")
    st.title("⚡ MathPrepAI: Professional Synchronizer")

    with st.sidebar:
        st.header("📐 Typography & Style")
        font_name = st.selectbox("Font Family", ["CourierPrime", "Roboto", "Lora"])
        f_style = st.selectbox("Text Weight", ["Regular", "B", "I", "BI"], 
                              format_func=lambda x: {"Regular":"Normal", "B":"Bold", "I":"Italic", "BI":"Bold Italic"}[x])
        f_size = st.slider("Font Size", 16, 32, 22)
        col_gap = st.slider("Column Spacing", 0, 100, 30)
        row_gap = st.slider("Row Spacing", 0, 100, 40)
        
        st.header("📄 Page Control")
        paper = st.selectbox("Paper Format", ["Letter", "A4"])
        probs_per_page = st.selectbox("Problems per Page", [12, 16, 20, 24, 28, 32], index=3)
        num_pages = st.selectbox("Total Pages to Generate", [1, 10, 20, 30])
        restart_num = st.checkbox("Restart numbering each page", value=False)
        
        st.header("🏫 Branding")
        show_teacher = st.checkbox("Include Teacher's Name", value=True)
        school = st.text_input("School Name", "Global Math Academy")
        teacher = st.text_input("Teacher's Name", "Mr. Smith")
        title = st.text_input("Worksheet Title", "Vertical Addition")

    # Generate Data
    total_probs = probs_per_page * num_pages
    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle Numbers"):
        st.session_state.current_math = generate_math_data(total_probs, "Medium")

    # --- PREVIEW SECTION ---
    st.subheader("🖥️ Interactive Preview")
    preview_mode = st.radio("Display Mode:", ["Worksheet", "Answer Key"], horizontal=True)
    
    st.info(f"📊 Layout Status: {probs_per_page} problems per page. Total {total_probs} problems across {num_pages} page(s).")
    
    # HTML Preview Logic
    is_key = (preview_mode == "Answer Key")
    font_css = "monospace" if font_name == "CourierPrime" else "sans-serif"
    
    items_html = "".join([f"""
        <div style="width: 22%; margin-bottom: {row_gap}px; font-family: {font_css}; font-size: {f_size}px; color: black;">
            <div style="font-size: 10px; color: gray;">{i+1})</div>
            <div style="text-align: right; padding-right: 20px;">
                {p['a']}<br>+ {p['b']}<br>
                <hr style="border: 2px solid black; margin: 2px 0;">
                <span style="color: red;">{p['a']+p['b'] if is_key else '&nbsp;'}</span>
            </div>
        </div>
    """ for i, p in enumerate(st.session_state.current_math[:probs_per_page])])

    components.html(f"""
        <div style="background: white; padding: 40px; border: 1px solid #333; color: black;">
            <h2 style="text-align: center;">{school.upper()}</h2>
            <h3 style="text-align: center;">{title}</h3>
            <div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-top: 30px;">{items_html}</div>
        </div>
    """, height=600, scrolling=True)

    # --- DOWNLOADS ---
    st.markdown("---")
    st.subheader("📥 Export Final Files")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### 📝 PDF Format")
        pdf = MathProPDF(paper_format=paper)
        pdf.setup_fonts(font_name)
        # เจน PDF โจทย์
        pdf.generate_sheet(st.session_state.current_math, title, school, teacher, f_size, f_style, col_gap, row_gap, False, probs_per_page, restart_num, show_teacher)
        st.download_button("📝 Download Worksheet (PDF)", data=bytes(pdf.output()), file_name=f"{title}.pdf", use_container_width=True)
        
        # เจน PDF เฉพาะเฉลย
        pdf_k = MathProPDF(paper_format=paper)
        pdf_k.setup_fonts(font_name)
        pdf_k.generate_sheet(st.session_state.current_math, title, school, teacher, f_size, f_style, col_gap, row_gap, True, probs_per_page, restart_num, show_teacher)
        st.download_button("🔑 Download Answer Key (PDF)", data=bytes(pdf_k.output()), file_name=f"{title}_Key.pdf", use_container_width=True)

    with c2:
        st.markdown("### 📊 PowerPoint Format")
        ppt_data = build_pptx(st.session_state.current_math, title, probs_per_page)
        st.download_button("📊 Download PPTX (Full Package)", data=ppt_data, file_name=f"{title}.pptx", use_container_width=True)

if __name__ == "__main__":
    run_app()
