import streamlit as st
import random
from fpdf import FPDF
import io

class MathPDF(FPDF):
    def header_setup(self, title, school, teacher, font_name):
        self.set_font(font_name, 'B', 16)
        self.cell(0, 10, school, ln=True, align='C')
        self.set_font(font_name, 'B', 22)
        self.cell(0, 15, title, ln=True, align='C')
        self.set_font(font_name, '', 10)
        self.cell(100, 10, f"Teacher: {teacher}", ln=False)
        self.cell(0, 10, "Name: __________________________  Score: ______", ln=True, align='R')
        self.line(10, 45, 200, 45)
        self.ln(10)

def generate_problems(count, digits, carry):
    problems = []
    for _ in range(count):
        if digits == 1:
            a, b = random.randint(1, 9), random.randint(1, 9)
        else:
            if not carry:
                a_u, b_u = random.randint(0, 4), random.randint(0, 4)
                a_t, b_t = random.randint(1, 4), random.randint(1, 4)
                a, b = (a_t * 10 + a_u), (b_t * 10 + b_u)
            else:
                a, b = random.randint(10, 99), random.randint(10, 99)
        problems.append({"a": a, "b": b, "ans": a + b})
    return problems

def create_pdf(title, school, teacher, problems, font_size):
    pdf = MathPDF()
    pdf.add_page()
    pdf.header_setup(title, school, teacher, 'Arial') # ใช้ Arial มาตรฐานเพื่อความเร็ว
    
    # Grid Layout Logic (4 columns)
    col_width = 45
    row_height = 30
    for idx, p in enumerate(problems):
        x = 15 + (idx % 4) * col_width
        y = 55 + (idx // 4) * row_height
        
        pdf.set_xy(x, y)
        pdf.set_font('Arial', '', 8)
        pdf.cell(5, 5, f"{idx+1})")
        
        pdf.set_font('Arial', '', font_size)
        pdf.set_xy(x + 10, y)
        pdf.cell(20, 10, f"{p['a']:>3}", ln=True, align='R')
        pdf.set_xy(x + 10, y + 8)
        pdf.cell(20, 10, f"+ {p['b']:>2}", ln=True, align='R')
        pdf.line(x + 15, y + 18, x + 35, y + 18)
        
    return pdf.output()

def run_app():
    st.title("⚡ Speed Math Pro: Instant PDF")
    tier = st.session_state.get('tier', "Free Tier")
    is_pro = tier != "Free Tier (Teaching Only)"

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("📋 Worksheet Info")
        school = st.text_input("School Name", "Global Academy")
        teacher = st.text_input("Teacher Name", "Prof. Math")
        ws_title = st.text_input("Worksheet Title", "Vertical Addition")
        
        st.header("🔢 Math Config")
        num_probs = st.slider("Problems", 12, 48, 24)
        digit_type = st.selectbox("Digits", ["1-Digit", "2-Digits"])
        allow_carry = st.checkbox("Allow Carry Over", value=True)
        
        st.header("🎨 Style")
        f_size = st.slider("Font Size", 14, 28, 20)

    # --- LOGIC ---
    if 'math_problems' not in st.session_state or st.button("🔀 Reshuffle"):
        st.session_state.math_problems = generate_problems(num_probs, 1 if "1" in digit_type else 2, allow_carry)

    # --- PREVIEW ---
    st.subheader("📄 Worksheet Preview")
    st.info("The preview below is a simplified version. The PDF will be perfectly formatted for A4.")
    
    # Simulation of the A4 page
    st.markdown(f"""
        <div style="border:1px solid #ccc; padding:20px; background:white; font-family:monospace; color:black;">
            <center><h3>{school}</h3><h1>{ws_title}</h1></center>
            <hr>
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">
                {" ".join([f"<div>{i+1})<br>&nbsp;&nbsp;{p['a']}<br>+&nbsp;{p['b']}<br><hr></div>" for i, p in enumerate(st.session_state.math_problems)])}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- DOWNLOAD SYSTEM ---
    st.markdown("---")
    if is_pro:
        pdf_data = create_pdf(ws_title, school, teacher, st.session_state.math_problems, f_size)
        st.download_button(
            label="📥 Download Ready-to-Print PDF",
            data=pdf_data,
            file_name=f"{ws_title.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("🔒 Upgrade to Pro to unlock PDF Download.")
