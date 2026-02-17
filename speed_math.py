import streamlit as st
import random
from fpdf import FPDF
import io
import requests
import os

# --- 1. PDF ENGINE (DYNAMIC FONT SUPPORT) ---
class GlobalMathPDF(FPDF):
    def __init__(self, format='Letter'):
        super().__init__(orientation='P', unit='mm', format=format)
        
    def load_selected_font(self, font_name):
        # Dictionary เก็บ URL ของฟอนต์แต่ละแบบ
        font_urls = {
            "CourierPrime": {
                "reg": "https://github.com/google/fonts/raw/main/ofl/courierprime/CourierPrime-Regular.ttf",
                "bold": "https://github.com/google/fonts/raw/main/ofl/courierprime/CourierPrime-Bold.ttf"
            },
            "Roboto": {
                "reg": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf",
                "bold": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf"
            },
            "Lora": {
                "reg": "https://github.com/google/fonts/raw/main/ofl/lora/static/Lora-Regular.ttf",
                "bold": "https://github.com/google/fonts/raw/main/ofl/lora/static/Lora-Bold.ttf"
            }
        }
        
        selected = font_urls[font_name]
        reg_file = f"{font_name}_reg.ttf"
        bold_file = f"{font_name}_bold.ttf"

        # Download if not exists
        for file, url in [(reg_file, selected["reg"]), (bold_file, selected["bold"])]:
            if not os.path.exists(file):
                r = requests.get(url)
                with open(file, "wb") as f:
                    f.write(r.content)

        self.add_font(font_name, '', reg_file)
        self.add_font(font_name, 'B', bold_file)

    def draw_page(self, title, school, teacher, problems, font_size, scale, font_name):
        self.add_page()
        # ใช้ฟอนต์ที่เลือก
        self.set_font(font_name, 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font(font_name, 'B', font_size + 4)
        self.cell(0, 15, title, ln=True, align='C')
        
        self.set_font(font_name, '', 10)
        w = self.w - 20
        self.cell(w/2, 10, f"Teacher: {teacher}", ln=False)
        self.cell(w/2, 10, "Name: _________________ Score: ____", ln=True, align='R')
        self.line(10, 48, self.w - 10, 48)
        self.ln(10)

        col_w = (self.w - 30) / 4
        row_h = 35 * (scale/100)
        
        self.set_line_width(0.6)
        for idx, p in enumerate(problems):
            x = 15 + (idx % 4) * col_w
            y = 60 + (idx // 4) * row_h
            if y > self.h - 30: break
            
            self.set_xy(x, y)
            self.set_font(font_name, '', 9)
            self.cell(5, 5, f"{idx+1})")
            
            self.set_font(font_name, 'B', font_size)
            self.set_xy(x + 5, y)
            self.cell(20, 10, f"{p['a']:>3}", ln=True, align='R')
            self.set_xy(x + 5, y + 8)
            self.cell(20, 10, f"+ {p['b']:>2}", ln=True, align='R')
            self.line(x + 13, y + 19, x + 31, y + 19)

# --- 2. MAIN APP ---
def run_app():
    # โหลด CSS สำหรับ Google Fonts เพื่อให้หน้าจอพรีวิวตรงกับ PDF
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&family=Roboto:wght@400;700&family=Lora:wght@400;700&display=swap');
        </style>
    """, unsafe_allow_html=True)

    st.title("⚡ Speed Math Pro: Custom Font Designer")
    
    with st.sidebar:
        st.header("📄 Page Setup")
        paper_size = st.selectbox("Format", ["Letter", "A4"])
        # เมนูเลือกฟอนต์
        font_choice = st.selectbox("Select Font", ["CourierPrime", "Roboto", "Lora"])
        
        content_scale = st.slider("Scale (%)", 70, 130, 100)
        num_probs = st.slider("Problems", 12, 48, 24)
        font_size = st.slider("Font Size", 16, 32, 24)
        
        st.header("🏫 Branding")
        school = st.text_input("School Name", "GLOBAL ACADEMY")
        teacher = st.text_input("Teacher", "Mr. Smith")
        ws_title = st.text_input("Worksheet Title", "Vertical Addition")

    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle"):
        st.session_state.current_math = [{"a": random.randint(10, 99), "b": random.randint(10, 99)} for _ in range(num_probs)]

    # --- 3. LIVE PREVIEW (MATCHED DYNAMIC FONT) ---
    st.subheader(f"📄 Preview: {font_choice} Font")
    
    # กำหนด CSS Font Family ตามที่เลือก
    css_font_map = {
        "CourierPrime": "'Courier Prime', monospace",
        "Roboto": "'Roboto', sans-serif",
        "Lora": "'Lora', serif"
    }
    css_font = css_font_map[font_choice]
    
    all_problems_html = "".join([
        f'<div style="text-align:right; font-size:{font_size}px; font-family:{css_font}; font-weight:bold; width:85px; margin:auto; margin-bottom:20px;">'
        f'<span style="float:left; font-size:12px; color:gray; font-weight:normal;">{i+1})</span>'
        f'{p["a"]}<br>+{p["b"]}'
        f'<div style="border-bottom:3px solid black; width:65px; margin-left:auto; margin-top:2px;"></div>'
        f'</div>'
        for i, p in enumerate(st.session_state.current_math)
    ])

    aspect_ratio = 1.29 if paper_size == "Letter" else 1.41
    canvas_container = f"""
    <div style="width:720px; height:{720 * aspect_ratio}px; background:white; margin:auto; border:1px solid #ddd; box-shadow:0 4px 15px rgba(0,0,0,0.1); padding:50px; color:black; overflow:hidden; font-family:{css_font};">
        <div style="text-align:center; border-bottom:2px solid black; padding-bottom:10px; margin-bottom:20px;">
            <div style="font-weight:bold; font-size:18px;">{school.upper()}</div>
            <div style="font-weight:bold; font-size:32px; margin:15px 0;">{ws_title}</div>
            <div style="display:flex; justify-content:space-between; font-size:14px;">
                <span>Teacher: {teacher}</span>
                <span>Name: ________________ Score: ____</span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:25px; transform:scale({content_scale/100}); transform-origin:top center;">
            {all_problems_html}
        </div>
    </div>
    """
    st.write(canvas_container, unsafe_allow_html=True)

    # --- 4. DOWNLOAD SYSTEM ---
    st.markdown("---")
    pdf = GlobalMathPDF(format=paper_size)
    try:
        # โหลดฟอนต์ที่เลือกเข้าสู่ PDF Engine
        pdf.load_selected_font(font_choice)
        pdf.draw_page(ws_title, school, teacher, st.session_state.current_math, font_size, content_scale, font_choice)
        
        pdf_bytes = bytes(pdf.output())
        st.download_button(label=f"📥 Download {font_choice} PDF", data=pdf_bytes, file_name=f"{ws_title}.pdf", mime="application/pdf")
        st.success(f"✅ PDF Generated with {font_choice}")
    except Exception as e:
        st.error(f"Error: {e}")
