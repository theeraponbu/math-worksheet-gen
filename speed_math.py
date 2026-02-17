import streamlit as st
import random
from fpdf import FPDF
import io

# --- คลาสสำหรับสร้าง PDF ภาษาอังกฤษมาตรฐาน ---
class SpeedMathPDF(FPDF):
    def header_setup(self, title, school, teacher):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font('Helvetica', 'B', 22)
        self.cell(0, 15, title, ln=True, align='C')
        self.set_font('Helvetica', '', 10)
        self.cell(100, 10, f"Teacher: {teacher}", ln=False)
        self.cell(0, 10, "Name: __________________________  Score: ______", ln=True, align='R')
        self.line(10, 45, 200, 45) # เส้นคั่นหัวกระดาษ
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

def run_app():
    st.title("⚡ Speed Math Pro: Ultimate Engine")
    tier = st.session_state.get('tier', "Free Tier")
    is_pro = tier != "Free Tier (Teaching Only)"

    # --- SIDEBAR SETTINGS ---
    with st.sidebar:
        st.header("📋 Worksheet Customization")
        school = st.text_input("School Name", "International Math Academy")
        teacher = st.text_input("Teacher Name", "Prof. Anderson")
        ws_title = st.text_input("Worksheet Title", "Vertical Addition Mastery")
        
        st.subheader("🔢 Math Settings")
        num_probs = st.slider("Number of Problems", 12, 48, 24)
        digit_type = st.selectbox("Complexity", ["1-Digit", "2-Digits"])
        allow_carry = st.checkbox("Allow Carry Over (ตัวทด)", value=True)
        
        st.subheader("🎨 Typography & Size")
        font_size = st.slider("Math Font Size (in PDF)", 14, 32, 22)
        main_color = st.color_picker("Theme Color", "#1b5e20")

    # --- LOGIC ---
    if 'math_problems' not in st.session_state or st.button("🔀 Reshuffle All Problems"):
        st.session_state.math_problems = generate_problems(num_probs, 1 if "1" in digit_type else 2, allow_carry)

    # --- PROFESSIONAL PREVIEW (A4 Simulation) ---
    st.subheader("📄 Worksheet Preview (Full Page)")
    
    st.markdown(f"""
        <div style="border: 2px solid {main_color}; padding: 30px; background-color: white; color: black; font-family: 'Courier New', Courier, monospace;">
            <div style="text-align: center;">
                <h3 style="margin:0;">{school.upper()}</h3>
                <h1 style="color: {main_color}; margin: 10px 0;">{ws_title}</h1>
            </div>
            <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 20px;">
                <span>Teacher: {teacher}</span>
                <span>Name: ____________________ Score: ____</span>
            </div>
            <hr style="border: 1px solid {main_color};">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 30px; margin-top: 20px;">
                {" ".join([f"<div style='text-align: right; border-bottom: 1px solid #ddd; padding: 10px;'>{i+1})<br>{p['a']}<br>+{p['b']}<br><hr style='border:1px solid black;'></div>" for i, p in enumerate(st.session_state.math_problems)])}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- INSTANT DOWNLOAD SYSTEM ---
    st.markdown("---")
    if is_pro:
        # ส่วนการเจน PDF จริง (โจทย์ + เฉลย)
        pdf = SpeedMathPDF()
        
        # หน้าที่ 1: โจทย์
        pdf.add_page()
        pdf.header_setup(ws_title, school, teacher)
        col_w, row_h = 45, 35
        for idx, p in enumerate(st.session_state.math_problems):
            x = 15 + (idx % 4) * col_w
            y = 55 + (idx // 4) * row_h
            pdf.set_xy(x, y)
            pdf.set_font('Helvetica', '', 8)
            pdf.cell(5, 5, f"{idx+1})")
            pdf.set_font('Helvetica', 'B', font_size)
            pdf.set_xy(x + 10, y)
            pdf.cell(20, 10, f"{p['a']:>3}", ln=True, align='R')
            pdf.set_xy(x + 10, y + 8)
            pdf.cell(20, 10, f"+ {p['b']:>2}", ln=True, align='R')
            pdf.line(x + 15, y + 18, x + 35, y + 18)

        # หน้าที่ 2: เฉลย (Answer Key)
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(0, 10, f"ANSWER KEY: {ws_title}", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font('Helvetica', '', 12)
        for idx, p in enumerate(st.session_state.math_problems):
            pdf.cell(40, 10, f"Q{idx+1}: {p['ans']}", border=1, align='C')
            if (idx + 1) % 5 == 0: pdf.ln()

        pdf_bytes = pdf.output()
        
        st.download_button(
            label="📥 Download Professional PDF (Worksheet + Key)",
            data=pdf_bytes,
            file_name=f"{ws_title.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("🔒 PDF Download is a Pro feature. Use Credits or Upgrade.")
