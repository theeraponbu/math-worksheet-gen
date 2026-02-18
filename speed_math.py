import streamlit as st
import streamlit.components.v1 as components
import random
from fpdf import FPDF
from pptx import Presentation
from pptx.util import Inches, Pt
import io
import os

# --- 1. PDF ENGINE ---
class GlobalMathPDF(FPDF):
    def __init__(self, format='Letter'):
        super().__init__(orientation='P', unit='mm', format=format)
        
    def setup_fonts(self, font_name):
        font_files = {"CourierPrime": "Courier", "Roboto": "Helvetica", "Lora": "Times"}
        self.f_family = font_files.get(font_name, "Courier")
        return True

    def generate_content(self, title, school, teacher, problems, f_size, f_style, col_gap, row_gap, 
                        is_key=False, probs_per_page=24, restart_num=False, show_teacher=True):
        
        for p_idx in range(0, len(problems), probs_per_page):
            self.add_page()
            page_probs = problems[p_idx : p_idx + probs_per_page]
            
            # --- Header ---
            self.set_font(self.f_family, 'B', 16)
            self.cell(0, 10, school.upper(), ln=True, align='C')
            
            # Styling Text (Bold/Italic)
            style = f_style.replace("Regular", "")
            self.set_font(self.f_family, style, f_size + 4)
            self.cell(0, 15, f"{title}{' (Key)' if is_key else ''}", ln=True, align='C')
            
            # Teacher Visibility Logic
            self.set_font(self.f_family, '', 10)
            if show_teacher:
                self.cell(90, 10, f"Teacher: {teacher}")
                self.cell(0, 10, "Name: ________________ Score: ____", align='R', ln=True)
            else:
                self.cell(0, 10, "Name: ________________________________ Score: ____", align='L', ln=True)
            
            self.line(10, 48, self.w - 10, 48)

            # --- Grid (4 Columns) ---
            col_w = (self.w - 30) / 4 + (col_gap / 15)
            row_h = 15 + (row_gap / 4)
            
            for i, p in enumerate(page_probs):
                col_i = i % 4
                row_i = i // 4
                x = 15 + col_i * col_w
                y = 65 + row_i * row_h
                
                num = (i + 1) if restart_num else (p_idx + i + 1)
                self.set_xy(x, y)
                self.set_font(self.f_family, '', 8); self.cell(5, 5, f"{num})")
                
                self.set_font(self.f_family, style, f_size)
                self.set_xy(x+5, y); self.cell(20, 10, f"{p['a']:>3}", align='R', ln=True)
                self.set_xy(x+5, y+8); self.cell(20, 10, f"+ {p['b']:>2}", align='R', ln=True)
                self.line(x+10, y+19, x+25, y+19)
                
                if is_key:
                    self.set_text_color(220, 0, 0)
                    self.set_xy(x+5, y+21); self.cell(20, 10, f"{p['a']+p['b']:>3}", align='R')
                    self.set_text_color(0, 0, 0)

# --- 2. POWERPOINT ENGINE ---
def build_pptx(problems, title, probs_per_page):
    prs = Presentation()
    for i in range(0, len(problems), probs_per_page):
        slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9), Inches(1))
        title_box.text_frame.text = title
    buffer = io.BytesIO()
    prs.save(buffer)
    return buffer.getvalue()

# --- 3. MATH LOGIC ---
def generate_math_data(num, diff, mode):
    problems, seen = [], set()
    low, high = (1, 9) if diff == "Easy" else (10, 99) if diff == "Medium" else (100, 999)
    while len(problems) < num:
        a, b = random.randint(low, high), random.randint(low, high)
        if (a, b) in seen: continue
        problems.append({"a": a, "b": b}); seen.add((a, b))
    return problems

# --- 4. MAIN APP ---
def run_app():
    st.set_page_config(page_title="MathPrepAI Pro", layout="wide")
    
    with st.sidebar:
        st.header("📐 Layout & Design")
        f_style = st.selectbox("Text Style", ["Regular", "B", "I", "BI"], format_func=lambda x: {"Regular":"Normal", "B":"Bold", "I":"Italic", "BI":"Bold Italic"}[x])
        font_name = st.selectbox("Font Family", ["CourierPrime", "Roboto", "Lora"])
        f_size = st.slider("Font Size", 16, 32, 22)
        col_gap = st.slider("Column Gap", 0, 100, 30)
        row_gap = st.slider("Row Gap", 0, 100, 40)
        
        st.header("📄 Page Control")
        probs_per_page = st.selectbox("Problems per Page", [12, 16, 20, 24, 28, 32], index=3)
        num_pages = st.selectbox("Total Pages to Download", [1, 10, 20, 30])
        restart_num = st.checkbox("Restart Numbering per Page", value=False)
        
        st.header("🏫 Branding")
        show_teacher = st.checkbox("Show Teacher's Name", value=True)
        school = st.text_input("School Name", "Global Academy")
        teacher = st.text_input("Teacher's Name", "Mr. Smith")
        title = st.text_input("Worksheet Title", "Vertical Addition")

    # Business Logic: Calculate total problems
    total_needed = probs_per_page * num_pages
    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle Data"):
        st.session_state.current_math = generate_math_data(total_needed, "Medium", "Mixed (Both)")

    # --- PREVIEW TOGGLE ---
    st.subheader("🖥️ Interactive Preview")
    preview_mode = st.radio("Preview Mode:", ["Worksheet", "Answer Key"], horizontal=True)
    
    # Simple HTML Sync Preview
    font_css = "monospace" if font_name == "CourierPrime" else "sans-serif"
    is_key_preview = (preview_mode == "Answer Key")
    
    items_html = "".join([f"""
        <div style="width: 22%; margin-bottom: {row_gap}px; font-family: {font_css}; font-size: {f_size}px; color: black;">
            <div style="font-size: 10px; color: gray;">{i+1})</div>
            <div style="text-align: right; padding-right: 20px;">
                {p['a']}<br>+ {p['b']}<br>
                <hr style="border: 2px solid black; margin: 2px 0;">
                <span style="color: red;">{p['a']+p['b'] if is_key_preview else '&nbsp;'}</span>
            </div>
        </div>
    """ for i, p in enumerate(st.session_state.current_math[:probs_per_page])])

    st.components.v1.html(f"""
        <div style="background: white; padding: 40px; border: 2px solid #333; color: black;">
            <h2 style="text-align: center;">{school.upper()}</h2>
            <h3 style="text-align: center;">{title}</h3>
            <div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-top: 30px;">{items_html}</div>
        </div>
    """, height=600, scrolling=True)

    st.info(f"📊 Summary: Creating {total_needed} unique problems across {num_pages} page(s).")

    # --- DOWNLOADS ---
    st.markdown("---")
    c1, c2 = st.columns(2)
    
    pdf = GlobalMathPDF()
    pdf.setup_fonts(font_name)
    
    with c1:
        st.subheader("📥 PDF Format")
        # Build PDF with current settings
        pdf.generate_content(title, school, teacher, st.session_state.current_math, f_size, f_style, col_gap, row_gap, False, probs_per_page, restart_num, show_teacher)
        st.download_button("📝 Download PDF Worksheet", data=bytes(pdf.output()), file_name=f"{title}.pdf")
        
        pdf_k = GlobalMathPDF()
        pdf_k.setup_fonts(font_name)
        pdf_k.generate_content(title, school, teacher, st.session_state.current_math, f_size, f_style, col_gap, row_gap, True, probs_per_page, restart_num, show_teacher)
        st.download_button("🔑 Download PDF Key", data=bytes(pdf_k.output()), file_name=f"{title}_Key.pdf")

    with c2:
        st.subheader("📥 PowerPoint Format")
        ppt_data = build_pptx(st.session_state.current_math, title, probs_per_page)
        st.download_button("📊 Download PPTX (Beta)", data=ppt_data, file_name=f"{title}.pptx")

if __name__ == "__main__":
    run_app()
