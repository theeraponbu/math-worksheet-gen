import streamlit as st
import streamlit.components.v1 as components
import random
from fpdf import FPDF
import io

# --- 1. PDF ENGINE (STRICT BOX LOCKING) ---
class MathProPDF(FPDF):
    def __init__(self, paper_format='Letter'):
        super().__init__(orientation='P', unit='mm', format=paper_format)
        self.f_family = 'Courier'

    def setup_fonts(self, font_name):
        font_map = {"CourierPrime": "Courier", "Roboto": "Helvetica", "Lora": "Times"}
        self.f_family = font_map.get(font_name, "Courier")
        return True

    def generate_sheet(self, problems, title, school, teacher, f_size, f_style, col_gap, row_gap, 
                       is_key=False, probs_per_page=24, restart_num=False, show_teacher=True):
        
        style = f_style.replace("Regular", "")
        for p_idx in range(0, len(problems), probs_per_page):
            self.add_page()
            page_probs = problems[p_idx : p_idx + probs_per_page]
            
            # Header
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

            # Strict Box Logic
            col_w = (self.w - 30) / 4 + (col_gap / 20)
            row_h = 28 + (row_gap / 10) 
            
            for i, p in enumerate(page_probs):
                col_i, row_i = i % 4, i // 4
                x, y = 15 + col_i * col_w, 55 + row_i * row_h
                num = (i + 1) if restart_num else (p_idx + i + 1)
                
                self.set_xy(x, y)
                self.set_font(self.f_family, '', 8); self.cell(5, 5, f"{num})")
                self.set_font(self.f_family, style, f_size)
                self.set_xy(x+5, y+2); self.cell(18, 10, f"{p['a']:>3}", align='R')
                self.set_xy(x+5, y+10); self.cell(18, 10, f"+ {p['b']:>2}", align='R')
                self.set_line_width(0.5)
                self.line(x+11, y+18, x+24, y+18)
                
                if is_key:
                    self.set_text_color(220, 0, 0)
                    self.set_xy(x+5, y+22.5); self.cell(18, 10, f"{p['a']+p['b']:>3}", align='R')
                    self.set_text_color(0, 0, 0)

# --- 2. MAIN APP ---
def run_app():
    st.set_page_config(page_title="MathPrepAI Master", layout="wide")

    # --- 2.1 INITIALIZE VARIABLES (ป้องกัน NameError) ---
    with st.sidebar:
        st.header("🏫 Branding")
        school = st.text_input("School Name", "Global Academy")
        title = st.text_input("Worksheet Title", "Vertical Addition")
        teacher = st.text_input("Teacher Name", "Mr. Smith")
        show_teacher = st.checkbox("Include Teacher Name", value=True)

        st.header("📐 Style & Layout")
        font_name = st.selectbox("Font", ["CourierPrime", "Roboto", "Lora"])
        f_style = st.selectbox("Weight", ["Regular", "B", "I", "BI"])
        f_size = st.slider("Size", 16, 32, 22)
        col_gap = st.slider("Col Gap", 0, 100, 30)
        row_gap = st.slider("Row Gap", 0, 100, 40)
        
        st.header("📄 Page Setup")
        paper = st.selectbox("Format", ["Letter", "A4"])
        probs_per_page = st.selectbox("Items Per Page", [12, 16, 20, 24, 28, 32], index=3)
        num_pages = st.selectbox("Download Pages", [1, 10, 20, 30])
        restart_num = st.checkbox("Restart No. per page", value=False)

    # Business Logic
    total_probs = probs_per_page * num_pages
    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle Data"):
        st.session_state.current_math = [{"a": random.randint(10, 99), "b": random.randint(10, 99)} for _ in range(total_probs)]

    # --- 2.2 PERFECT PREVIEW ---
    st.subheader("🖥️ Synchronized Paper View")
    preview_mode = st.radio("Mode:", ["Worksheet", "Answer Key"], horizontal=True)
    is_key = (preview_mode == "Answer Key")
    font_css = "monospace" if font_name == "CourierPrime" else "sans-serif"
    aspect = 1.29 if paper == "Letter" else 1.41
    
    # HTML Items (ล็อกกล่องโจทย์เหมือน PDF)
    items_html = "".join([f"""
        <div style="width: 22%; height: {100 + row_gap}px; margin-bottom: 10px; font-family: {font_css}; color: black; font-size: {f_size}px; position: relative;">
            <div style="font-size: 10px; color: #999; text-align: left;">{i+1})</div>
            <div style="text-align: right; padding-right: 15px; font-weight: {'bold' if 'B' in f_style else 'normal'}; font-style: {'italic' if 'I' in f_style else 'normal'};">
                {p['a']}<br>+ {p['b']}<br>
                <div style="border-top: 2.5px solid black; width: 42px; margin-left: auto; margin-top: 1px;"></div>
                <div style="color: #d00; height: 30px; margin-top: 2px;">{p['a']+p['b'] if is_key else '&nbsp;'}</div>
            </div>
        </div>
    """ for i, p in enumerate(st.session_state.current_math[:probs_per_page])])

    # ปรับความสูงพรีวิวและเพิ่มพื้นที่สโครลให้เห็นขอบล่างชัดเจน
    components.html(f"""
        <div style="background: #444; display: flex; flex-direction: column; align-items: center; padding: 100px 0; min-height: 1200px; overflow-y: auto;">
            <div style="width: 700px; height: {700 * aspect}px; background: white; padding: 50px; box-shadow: 0 20px 60px rgba(0,0,0,0.5); box-sizing: border-box; flex-shrink: 0; position: relative;">
                <div style="text-align: center; border-bottom: 2px solid #000; margin-bottom: 20px; color: black; font-family: sans-serif;">
                    <h2 style="margin: 0; font-size: 20px;">{school.upper()}</h2>
                    <h1 style="margin: 5px 0; font-size: 28px;">{title}</h1>
                    <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: bold; padding: 10px 0;">
                        <span>{"Teacher: " + teacher if show_teacher and teacher else "Name: ________________________________________________"}</span>
                        <span>{ "Name: ________________" if show_teacher else "Score: ____"}</span>
                    </div>
                </div>
                <div style="display: flex; flex-wrap: wrap; justify-content: space-around; align-content: flex-start;">{items_html}</div>
                <div style="position: absolute; bottom: 30px; right: 50px; color: #888; font-family: sans-serif; font-size: 12px;">Page 1</div>
            </div>
            <div style="height: 150px; width: 100%;"></div>
        </div>
    """, height=1000)

    # --- 2.3 DOWNLOAD BUTTONS ---
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        pdf_ws = MathProPDF(paper_format=paper)
        pdf_ws.setup_fonts(font_name)
        pdf_ws.generate_sheet(st.session_state.current_math, title, school, teacher, f_size, f_style, col_gap, row_gap, False, probs_per_page, restart_num, show_teacher)
        st.download_button("📝 Download Worksheet (PDF)", data=bytes(pdf_ws.output()), file_name=f"{title}.pdf", use_container_width=True)
    with col2:
        pdf_k = MathProPDF(paper_format=paper)
        pdf_k.setup_fonts(font_name)
        pdf_k.generate_sheet(st.session_state.current_math, title, school, teacher, f_size, f_style, col_gap, row_gap, True, probs_per_page, restart_num, show_teacher)
        st.download_button("🔑 Download Answer Key (PDF)", data=bytes(pdf_k.output()), file_name=f"{title}_Key.pdf", use_container_width=True)

if __name__ == "__main__":
    run_app()
