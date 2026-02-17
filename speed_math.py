import streamlit as st
import random
from fpdf import FPDF

# --- 1. PDF CLASS DEFINITION ---
class SpeedMathPDF(FPDF):
    def header_setup(self, title, school, teacher):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        self.set_font('Helvetica', 'B', 22)
        self.cell(0, 15, title, ln=True, align='C')
        self.set_font('Helvetica', '', 10)
        self.cell(100, 10, f"Teacher: {teacher}", ln=False)
        self.cell(0, 10, "Name: __________________________  Score: ______", ln=True, align='R')
        self.set_draw_color(46, 125, 50)
        self.line(10, 48, 200, 48)
        self.ln(12)

# --- 2. MATH CORE LOGIC ---
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

# --- 3. THE MAIN FUNCTION (Must match main.py calling) ---
def run_app():
    # ป้องกัน AttributeError ด้วยการเช็ค session_state
    tier = st.session_state.get('tier', "Free Tier (Teaching Only)")
    is_pro = tier != "Free Tier (Teaching Only)"

    st.title("⚡ Speed Math Pro: Vertical Addition")

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("📋 Worksheet Settings")
        school = st.text_input("School Name", "Global Academy")
        teacher = st.text_input("Teacher Name", "Prof. Anderson")
        ws_title = st.text_input("Worksheet Title", "Speed Addition Drill")
        num_probs = st.slider("Problems", 12, 48, 24)
        digit_choice = st.selectbox("Complexity", ["1-Digit", "2-Digits"])
        allow_carry = st.checkbox("Allow Carry Over", value=True)
        font_size = st.slider("Font Size", 16, 32, 22)

    # --- PROBLEM RE-GENERATION ---
    if 'math_problems' not in st.session_state or st.button("🔀 New Problems"):
        st.session_state.math_problems = generate_problems(num_probs, 1 if "1" in digit_choice else 2, allow_carry)

    # --- UI PREVIEW (A4 Simulation) ---
    st.markdown(f"""
        <div style="border: 2px solid #2e7d32; padding: 30px; background-color: white; color: black; font-family: 'Courier New', monospace;">
            <center><h3>{school.upper()}</h3><h1>{ws_title}</h1></center>
            <div style="display: flex; justify-content: space-between;">
                <span>Teacher: {teacher}</span>
                <span>Name: ____________________ Score: ____</span>
            </div>
            <hr style="border: 1px solid #2e7d32;">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 30px; margin-top: 20px;">
                {" ".join([f"<div style='text-align: right; border-bottom: 1px solid #ddd; padding: 5px;'>{i+1})<br>{p['a']}<br>+{p['b']}<br><hr style='border:1px solid black;'></div>" for i, p in enumerate(st.session_state.math_problems)])}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- PDF EXPORT ---
    st.markdown("---")
    if is_pro:
        pdf = SpeedMathPDF()
        pdf.add_page()
        pdf.header_setup(ws_title, school, teacher)
        
        col_w, row_h = 45, 35
        pdf.set_font('Helvetica', 'B', font_size)
        
        for idx, p in enumerate(st.session_state.math_problems):
            x = 15 + (idx % 4) * col_w
            y = 60 + (idx // 4) * row_h
            pdf.set_xy(x, y)
            pdf.set_font('Helvetica', '', 8)
            pdf.cell(5, 5, f"{idx+1})")
            pdf.set_font('Helvetica', 'B', font_size)
            pdf.set_xy(x + 10, y)
            pdf.cell(20, 10, f"{p['a']:>3}", ln=True, align='R')
            pdf.set_xy(x + 10, y + 8)
            pdf.cell(20, 10, f"+ {p['b']:>2}", ln=True, align='R')
            pdf.line(x + 15, y + 19, x + 35, y + 19)

        # หน้าเฉลย
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 18)
        pdf.cell(0, 15, "ANSWER KEY", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font('Helvetica', '', 12)
        for idx, p in enumerate(st.session_state.math_problems):
            pdf.cell(38, 12, f"Q{idx+1}: {p['ans']}", border=1, align='C')
            if (idx + 1) % 5 == 0: pdf.ln()

        pdf_bytes = bytes(pdf.output())
        st.download_button(
            label="📥 Download Professional PDF",
            data=pdf_bytes,
            file_name=f"{ws_title.replace(' ', '_')}.pdf",
            mime="application/pdf",
            key="speed_math_download"
        )
    else:
        st.warning("🔒 Upgrade to Pro to unlock PDF downloads.")
