import streamlit as st
import random
from fpdf import FPDF
import io

# --- 1. PDF ENGINE (ULTRA FIDELITY) ---
class GlobalMathPDF(FPDF):
    def __init__(self, format='Letter'):
        super().__init__(orientation='P', unit='mm', format=format)

    def draw_page(self, title, school, teacher, problems, font_size, scale):
        self.add_page()
        # Header - ใช้ Helvetica Bold เพื่อความหรูหราแบบ Minimal
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font('Helvetica', 'B', font_size + 4)
        self.set_text_color(33, 33, 33)
        self.cell(0, 15, title, ln=True, align='C')
        
        # Divider Line
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.3)
        self.line(10, 48, self.w - 10, 48)
        
        # Info Bar
        self.set_text_color(100, 100, 100)
        self.set_font('Helvetica', '', 10)
        w = self.w - 20
        self.set_y(40)
        self.cell(w/2, 10, f"Teacher: {teacher}", ln=False)
        self.cell(w/2, 10, "Name: _________________ Score: ____", ln=True, align='R')
        self.ln(15)

        # Problems Grid
        col_w = (self.w - 30) / 4
        row_h = 35 * (scale/100)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.6) # เส้นคำตอบที่คมชัด
        
        for idx, p in enumerate(problems):
            x = 15 + (idx % 4) * col_w
            y = 65 + (idx // 4) * row_h
            if y > self.h - 30: break
            
            self.set_xy(x, y)
            self.set_font('Helvetica', '', 8)
            self.set_text_color(150, 150, 150)
            self.cell(5, 5, f"{idx+1})")
            
            self.set_text_color(0, 0, 0)
            self.set_font('Helvetica', 'B', font_size)
            self.set_xy(x + 5, y)
            self.cell(20, 10, f"{p['a']:>3}", ln=True, align='R')
            self.set_xy(x + 5, y + 8)
            self.cell(20, 10, f"+ {p['b']:>2}", ln=True, align='R')
            self.line(x + 12, y + 19, x + 30, y + 19)

# --- 2. MAIN APP ---
def run_app():
    st.markdown("""
        <style>
        .main { background-color: #f5f7f9; }
        .stButton>button { border-radius: 8px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("⚡ Speed Math Pro: Premium Designer")
    
    with st.sidebar:
        st.header("📄 Page Setup")
        paper_size = st.selectbox("Standard", ["Letter", "A4"])
        content_scale = st.slider("Scale (%)", 70, 130, 100)
        num_probs = st.slider("Problems", 12, 48, 24)
        font_size = st.slider("Font Size", 16, 32, 24)
        
        st.header("🏫 Branding")
        school = st.text_input("School", "BRIGHT FUTURE ACADEMY")
        teacher = st.text_input("Teacher", "Mr. Anderson")
        ws_title = st.text_input("Title", "Vertical Addition")

    if 'current_math' not in st.session_state or st.button("🔀 Reshuffle All"):
        st.session_state.current_math = [{"a": random.randint(10, 99), "b": random.randint(10, 99)} for _ in range(num_probs)]

    # --- 3. PREMIUM LIVE PREVIEW ---
    st.subheader("📄 Worksheet Preview")
    aspect_ratio = 1.29 if paper_size == "Letter" else 1.41
    preview_width = 720 
    
    problems_html = ""
    for i, p in enumerate(st.session_state.current_math):
        problems_html += f"""
        <div style="text-align:right; font-size:{font_size}px; font-family:'Courier New', monospace; font-weight:bold; width:80px; margin:auto;">
            <span style="float:left; font-size:12px; color:#aaa; font-weight:normal;">{i+1})</span>
            {p['a']}<br>+{p['b']}
            <div style="border-bottom:3px solid black; width:65px; margin-left:auto; margin-top:4px;"></div>
        </div>
        """

    st.markdown(f"""
    <div style="width:{preview_width}px; height:{preview_width * aspect_ratio}px; background:white; margin:auto; border:1px solid #e0e0e0; border-radius:4px; box-shadow:0 15px 35px rgba(0,0,0,0.1); padding:50px; color:black; overflow:hidden;">
        <div style="text-align:center; border-bottom:1px solid #eee; padding-bottom:15px; margin-bottom:25px;">
            <div style="font-weight:bold; font-size:16px; color:#666; letter-spacing:2px;">{school.upper()}</div>
            <div style="font-weight:bold; font-size:32px; margin:15px 0; font-family:'Trebuchet MS';">{ws_title}</div>
            <div style="display:flex; justify-content:space-between; font-size:14px; color:#444;">
                <span><b>Teacher:</b> {teacher}</span>
                <span><b>Name:</b> ____________________ <b>Score:</b> ____</span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:40px; transform:scale({content_scale/100}); transform-origin:top center;">
            {problems_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 4. EXPORT ---
    st.markdown("---")
    pdf = GlobalMathPDF(format=paper_size)
    pdf.draw_page(ws_title, school, teacher, st.session_state.current_math, font_size, content_scale)
    
    try:
        pdf_bytes = bytes(pdf.output())
        st.download_button(
            label="📥 Download Professional PDF",
            data=pdf_bytes,
            file_name=f"{ws_title}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Error: {e}")
