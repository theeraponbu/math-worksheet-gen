import streamlit as st
import fraction_factory
import speed_math
import shape_master
import graphing_notebook
import clock_generator
import pdf_editor

# --- 1. GLOBAL CONFIGURATION ---
st.set_page_config(
    page_title="MathPrepAI Ultimate Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. STATE MANAGEMENT (ควบคุมการเปลี่ยนหน้า) ---
# ตรวจสอบว่ามีค่า menu_choice ในระบบหรือยัง ถ้าไม่มีให้เริ่มที่ Dashboard
if 'menu_choice' not in st.session_state:
    st.session_state.menu_choice = "🏠 Dashboard"

# --- 3. THE TESTING SUITE (ADMIN TOGGLE) ---
st.sidebar.title("🔐 Tier Testing (Admin)")
user_tier = st.sidebar.radio(
    "Switch Access Level:",
    [
        "Free Tier (Teaching Only)", 
        "Personal Pro (Personal Use)", 
        "Commercial Enterprise (Full Access)"
    ],
    help="Select a tier to test features and licensing watermarks."
)

# ส่งค่า Tier ไปยัง Session State ให้ไฟล์อื่นใช้งาน
st.session_state.tier = user_tier

if user_tier == "Commercial Enterprise (Full Access)":
    st.sidebar.success("🚀 FULL COMMERCIAL ACCESS")
elif user_tier == "Personal Pro (Personal Use)":
    st.sidebar.info("👤 PERSONAL PRO ACTIVE")
else:
    st.sidebar.warning("🆓 FREE VERSION ACTIVE")

st.sidebar.markdown("---")

# --- 4. NAVIGATION MENU (SYNCED WITH DASHBOARD) ---
menu_list = [
    "🏠 Dashboard", 
    "🧩 Fraction Factory", 
    "⚡ Speed Math Drills", 
    "📐 Shape Master", 
    "📉 Graphing Notebook", 
    "🕒 Time & Clock", 
    "📑 PDF Editor & Merger"
]

# ค้นหาตำแหน่งของเมนูปัจจุบันเพื่อทำ Default Index ให้ Sidebar เลื่อนตาม
try:
    current_index = menu_list.index(st.session_state.menu_choice)
except ValueError:
    current_index = 0

st.sidebar.title("🎓 MathPrepAI Workspace")
menu = st.sidebar.radio("SELECT TOOL:", menu_list, index=current_index)

# อัปเดตค่าที่เลือกจาก Sidebar กลับเข้าสู่ Session State
st.session_state.menu_choice = menu

# --- 5. ROUTING LOGIC (การแสดงผลแต่ละหน้า) ---

if menu == "🏠 Dashboard":
    st.title("Welcome to MathPrepAI Global Dashboard")
    st.write(f"Current Access: **{user_tier}**")
    st.markdown("---")

    st.subheader("Your Toolkit")
    
    # --- ROW 1 ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 🧩 Fraction Factory\nVisual fraction models with pro themes.")
        if st.button("Launch Tool", key="btn_frac"):
            st.session_state.menu_choice = "🧩 Fraction Factory"
            st.rerun()
            
    with col2:
        st.success("### ⚡ Speed Math\nHigh-speed arithmetic drill generator.")
        if st.button("Launch Tool", key="btn_speed"):
            st.session_state.menu_choice = "⚡ Speed Math Drills"
            st.rerun()
        
    with col3:
        st.warning("### 📐 Shape Master\nGeometric shapes with area calculations.")
        if st.button("Launch Tool", key="btn_shape"):
            st.session_state.menu_choice = "📐 Shape Master"
            st.rerun()

    # --- ROW 2 ---
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1:
        st.error("### 📉 Graphing\nProfessional coordinate plane plotter.")
        if st.button("Launch Tool", key="btn_graph"):
            st.session_state.menu_choice = "📉 Graphing Notebook"
            st.rerun()
        
    with row2_col2:
        st.info("### 🕒 Time & Clock\nHigh-fidelity analog clock generator.")
        if st.button("Launch Tool", key="btn_clock"):
            st.session_state.menu_choice = "🕒 Time & Clock"
            st.rerun()
        
    with row2_col3:
        st.write("### 📑 PDF Editor\nAdvanced PDF management & merging.")
        if st.button("Launch Tool", key="btn_pdf"):
            st.session_state.menu_choice = "📑 PDF Editor & Merger"
            st.rerun()

elif menu == "🧩 Fraction Factory":
    fraction_factory.run_app()

elif menu == "⚡ Speed Math Drills":
    speed_math.run_app()

elif menu == "📐 Shape Master":
    shape_master.run_app()

elif menu == "📉 Graphing Notebook":
    graphing_notebook.run_app()

elif menu == "🕒 Time & Clock":
    clock_generator.run_app()

elif menu == "📑 PDF Editor & Merger":
    pdf_editor.run_app()

# --- 6. FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"© 2026 MathPrepAI Global | Status: {user_tier}")
