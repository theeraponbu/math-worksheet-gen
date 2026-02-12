import streamlit as st
import random

# --- 1. ตั้งค่าหน้าเว็บ (Page Config) ---
st.set_page_config(
    page_title="MathPrepAI",
    page_icon="🧮",
    layout="wide"
)

# --- CSS เพื่อซ่อนปุ่มตอนสั่ง Print (ให้กระดาษสวย) ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display:none;}
            @media print {
                .stButton {display: none;}
                .css-15zrgzn {display: none;}
                .css-1y4p8pa {padding-top: 0rem;}
                [data-testid="stSidebar"] {display: none;}
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 2. ฟังก์ชัน Logic คำนวณเลข ---

def generate_quadratic_question(level):
    """สร้างโจทย์สมการกำลังสอง"""
    if level == "Level 1: Basic (a=1)":
        a = 1
        root1 = random.randint(-9, 9)
        root2 = random.randint(-9, 9)
        if root1 == 0: root1 = 1
        if root2 == 0: root2 = -2
    else:
        a = random.randint(2, 5)
        root1 = random.randint(-5, 5)
        root2 = random.randint(-5, 5)
        if root1 == 0: root1 = 1
        if root2 == 0: root2 = -2

    m = random.randint(-9, 9)
    n = random.randint(-9, 9)
    if m == 0: m = 3
    if n == 0: n = -2
    
    if level == "Level 1: Basic (a=1)":
        a = 1
        b = m + n
        c = m * n
        ans_str = f"x = {-m}, {-n}"
    else:
        a = random.randint(2, 5)
        b = (a * n) + m
        c = m * n
        ans_str = f"x = {-n}, \\frac{{{-m}}}{{{a}}}"

    term_a = f"{a}x^2" if a > 1 else "x^2"
    term_b = f"+ {b}x" if b > 0 else f"- {abs(b)}x"
    term_c = f"+ {c}" if c > 0 else f"- {abs(c)}"
    if b == 0: term_b = ""
    if c == 0: term_c = ""

    question_latex = f"{term_a} {term_b} {term_c} = 0"
    return question_latex, ans_str

def generate_system_equations(level):
    """สร้างโจทย์ระบบสมการเชิงเส้น"""
    x_ans = random.randint(-9, 9)
    y_ans = random.randint(-9, 9)
    if x_ans == 0: x_ans = 3
    if y_ans == 0: y_ans = -2
    
    if level == "Level 1: Simple (Positive)":
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        d = random.randint(1, 3)
        e = random.randint(1, 3)
        if random.random() > 0.5: d = 1
    else: 
        a = random.randint(-5, 9)
        b = random.randint(-5, 9)
        d = random.randint(-5, 9)
        e = random.randint(-5, 9)
        if a == 0: a = 2
        if b == 0: b = -3
        if d == 0: d = 4
        if e == 0: e = -1

    c = (a * x_ans) + (b * y_ans)
    f = (d * x_ans) + (e * y_ans)

    def format_eq(coef_x, coef_y, const):
        tx = f"{coef_x}x" if coef_x != 1 else "x"
        if coef_x == -1: tx = "-x"
        
        if coef_y > 0:
            ty = f"+ {coef_y}y" if coef_y != 1 else "+ y"
        elif coef_y < 0:
            ty = f"- {abs(coef_y)}y" if coef_y != -1 else "- y"
        else:
            ty = ""
        return f"{tx} {ty} = {const}"

    eq1_latex = format_eq(a, b, c)
    eq2_latex = format_eq(d, e, f)
    system_latex = r"\begin{cases} " + eq1_latex + r" \\ " + eq2_latex + r" \end{cases}"
    ans_latex = f"(x, y) = ({x_ans}, {y_ans})"
    return system_latex, ans_latex

# --- 3. ส่วนแสดงผล (Frontend) ---

# State Management (จำค่าหน้าปัจจุบัน)
if 'current_tool' not in st.session_state:
    st.session_state['current_tool'] = 'Dashboard'

# Sidebar Navigation
with st.sidebar:
    st.title("🧮 MathPrepAI")
    if st.button("🏠 Dashboard"):
        st.session_state['current_tool'] = 'Dashboard'
        st.rerun()
    st.markdown("---")
    st.caption("Tools List")
    if st.button("📐 System of Equations"):
        st.session_state['current_tool'] = "System of Equations"
        st.rerun()
    if st.button("🎲 Factoring Quadratics"):
        st.session_state['current_tool'] = "Factoring Quadratics"
        st.rerun()

# --- Main Content Area ---

if st.session_state['current_tool'] == 'Dashboard':
    st.title("🚀 Welcome, Teacher!")
    st.markdown("Select a tool below to generate professional worksheets.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📐 **System of Equations**\n\nCreate systems with integer solutions.")
        if st.button("Launch System of Equations", key="d_btn1"):
            st.session_state['current_tool'] = "System of Equations"
            st.rerun()
            
    with col2:
        st.success("🎲 **Factoring Quadratics**\n\nCreate quadratic equations easily.")
        if st.button("Launch Quadratics", key="d_btn2"):
            st.session_state['current_tool'] = "Factoring Quadratics"
            st.rerun()

elif st.session_state['current_tool'] == "System of Equations":
    st.header("📐 System of Equations Generator")
    
    c1, c2 = st.columns(2)
    with c1:
        qty = st.slider("Quantity", 5, 20, 10, key="sys_qty")
    with c2:
        lvl = st.selectbox("Difficulty", ["Level 1: Simple (Positive)", "Level 2: Advanced"], key="sys_lvl")
        
    if st.button("Generate Worksheet", key="sys_gen"):
        st.write("---")
        q_list = [generate_system_equations(lvl) for _ in range(qty)]
        
        qc1, qc2 = st.columns(2)
        for i, (q, a) in enumerate(q_list):
            with qc1 if i % 2 == 0 else qc2:
                st.latex(f"{i+1}.) \\quad {q}")
                st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("---")
        with st.expander("🔐 Show Answer Key"):
            ac1, ac2, ac3 = st.columns(3)
            for i, (q, a) in enumerate(q_list):
                with ac1 if i%3==0 else ac2 if i%3==1 else ac3:
                    st.markdown(f"**{i+1}.** ${a}$")

elif st.session_state['current_tool'] == "Factoring Quadratics":
    st.header("🎲 Factoring Quadratics Generator")
    
    c1, c2 = st.columns(2)
    with c1:
        qty = st.slider("Quantity", 5, 20, 10, key="quad_qty")
    with c2:
        lvl = st.selectbox("Difficulty", ["Level 1: Basic (a=1)", "Level 2: Advanced (a>1)"], key="quad_lvl")
        
    if st.button("Generate Worksheet", key="quad_gen"):
        st.write("---")
        q_list = [generate_quadratic_question(lvl) for _ in range(qty)]
        
        qc1, qc2 = st.columns(2)
        for i, (q, a) in enumerate(q_list):
            with qc1 if i % 2 == 0 else qc2:
                st.markdown(f"**{i+1}.** Solve for $x$:")
                st.latex(q)
                st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("---")
        with st.expander("🔐 Show Answer Key"):
            ac1, ac2, ac3 = st.columns(3)
            for i, (q, a) in enumerate(q_list):
                with ac1 if i%3==0 else ac2 if i%3==1 else ac3:
                    st.markdown(f"**{i+1}.** ${a}$")
