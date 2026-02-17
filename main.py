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

# --- 2. THE TESTING SUITE (ADMIN TOGGLE) ---
# ส่วนนี้คือ "สวิตช์ลับ" ที่เราคุยกันเพื่อให้อาจารย์ทดสอบสิทธิ์การใช้งาน 3 ระดับ
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

# เก็บสถานะ Tier ไว้ใน Session State เพื่อให้ไฟล์อื่นเรียกใช้ได้
st.session_state.tier = user_tier

# แสดงสถานะปัจจุบันแบบมืออาชีพ
if user_tier == "Commercial Enterprise (Full Access)":
    st.sidebar.success("🚀 FULL COMMERCIAL ACCESS")
elif user_tier == "Personal Pro (Personal Use)":
    st.sidebar.info("👤 PERSONAL PRO ACTIVE")
else:
    st.sidebar.warning("🆓 FREE VERSION ACTIVE")

st.sidebar.markdown("---")

# --- 3. NAVIGATION MENU ---
st.sidebar.title("🎓 MathPrepAI Workspace")
menu = st.sidebar.radio(
    "SELECT TOOL:",
    [
        "🏠 Dashboard",
        "🧩 Fraction Factory",
        "⚡ Speed Math Drills",
        "📐 Shape Master",
        "📉 Graphing Notebook",
        "🕒 Time & Clock",
        "📑 PDF Editor & Merger"
    ]
)

# --- 4. ROUTING LOGIC (การเปลี่ยนหน้า) ---
if menu == "🏠 Dashboard":
    st.title("Welcome to MathPrepAI Global Dashboard")
    st.write(f"Current Access: **{user_tier}**")
    st.markdown("---")

    # ส่วนแสดงการ์ดเครื่องมือ (6 การ์ด)
    st.subheader("Your Toolkit")
    
    # แถวที่ 1
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 🧩 Fraction Factory\nVisual fraction models with pro themes.")
        if st.button("Launch Fraction Factory"):
            st.warning("Please use the sidebar to navigate.") # หรือจะเขียนระบบเปลี่ยนหน้าอัตโนมัติเพิ่มได้
            
    with col2:
        st.success("### ⚡ Speed Math\nHigh-speed arithmetic drill generator.")
        
    with col3:
        st.warning("### 📐 Shape Master\nGeometric shapes with area calculations.")

    # แถวที่ 2
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1:
        st.error("### 📉 Graphing\nProfessional coordinate plane plotter.")
        
    with row2_col2:
    # ใช้ st.info จะดูสะอาดตาและไม่มีเมนูเทคนิคโผล่มาครับ
    st.info("### 🕒 Time & Clock\nHigh-fidelity analog clock generator.")
    if st.button("Launch Clock Master", key="launch_clock"):
        st.session_state.menu_choice = "🕒 Time & Clock"
        st.rerun()
        
    with row2_col3:
        st.write("### 📑 PDF Editor\nAdvanced PDF management & merging.")

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

# --- 5. FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"© 2026 MathPrepAI Global | Status: {user_tier}")
