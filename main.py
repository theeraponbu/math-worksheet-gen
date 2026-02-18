import streamlit as st
import hashlib
import hmac
from datetime import datetime

# --- 1. CONFIGURATION (ต้องอยู่บรรทัดแรกสุดของคำสั่ง Streamlit) ---
st.set_page_config(
    page_title="MathPrepAI Ultimate Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. IMPORT MODULES (ดึงไฟล์งานของอาจารย์มาใช้) ---
try:
    import fraction_factory
    import speed_math
    import shape_master
    import graphing_notebook
    import clock_generator
    import pdf_editor
except ImportError as e:
    st.error(f"❌ ระบบขัดข้อง: ไม่พบไฟล์โมดูลสำคัญ ({e}) กรุณาตรวจสอบไฟล์ใน GitHub")

# --- 3. SECURITY & ACCESS CONTROL ---
SECRET_KEY = "MATH_PREP_SECRET_99" # ต้องตรงกับใน WordPress Snippet

def validate_access(token, uid):
    if not token or not uid:
        return False
    # ใช้เวลาสากล (UTC) เพื่อให้ตรงกับฝั่ง WordPress (gmdate)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H')
    expected_token = hmac.new(
        SECRET_KEY.encode(),
        (str(uid) + timestamp).encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(token, expected_token)

# --- 4. SESSION STATE MANAGEMENT (ป้องกัน Redirect Loop) ---
# ตรวจสอบสิทธิ์เพียงครั้งเดียวเมื่อโหลดแอปครั้งแรก
if 'access_verified' not in st.session_state:
    params = st.query_params
    token_rx = params.get("token")
    uid_rx = params.get("uid")
    tier_rx = params.get("tier", "free")
    
    if validate_access(token_rx, uid_rx):
        st.session_state.access_verified = True
        st.session_state.user_tier = tier_rx
        st.session_state.uid = uid_rx
    else:
        st.session_state.access_verified = False
        st.session_state.debug_info = {
            "uid": uid_rx,
            "token": token_rx,
            "time": datetime.utcnow().strftime('%Y%m%d%H')
        }

# --- 5. ENFORCE ACCESS CONTROL ---
if st.session_state.access_verified is False:
    st.error("❌ Access Denied: กรุณาเข้าใช้งานผ่านหน้า Dashboard ของ MathPrepAI.com")
    
    # ส่วน Debug สำหรับอาจารย์ (ช่วยเช็คว่าทำไมรหัสไม่ตรงกัน)
    with st.expander("🔍 ข้อมูลทางเทคนิค (Technical Debug)"):
        debug = st.session_state.debug_info
        st.write(f"**Received UID:** {debug['uid']}")
        st.write(f"**Received Token:** {debug['token']}")
        st.write(f"**Server Time (UTC):** {debug['time']}")
        st.info("Tip: ตรวจสอบ Secret Key ใน WordPress และ Python ให้ตรงกัน")
    st.stop()

# ดึงค่ามาใช้งานเมื่อผ่านการตรวจสอบแล้ว
user_tier = st.session_state.user_tier
uid = st.session_state.uid

# --- 6. NAVIGATION LOGIC ---
if 'menu_choice' not in st.session_state:
    st.session_state.menu_choice = "🏠 Dashboard"

menu_list = [
    "🏠 Dashboard", 
    "🧩 Fraction Factory", 
    "⚡ Speed Math Drills", 
    "📐 Shape Master", 
    "📉 Graphing Notebook", 
    "🕒 Time & Clock", 
    "📑 PDF Editor & Merger"
]

# Sidebar การตั้งค่า
with st.sidebar:
    st.title("🎓 MathPrepAI Workspace")
    menu = st.radio("SELECT TOOL:", menu_list, index=menu_list.index(st.session_state.menu_choice))
    st.session_state.menu_choice = menu
    st.markdown("---")
    
    # แสดงสถานะ Tier
    if "pro" in user_tier.lower():
        st.success(f"🚀 {user_tier.upper()} ACTIVE")
    else:
        st.warning("🆓 FREE VERSION")
    
    st.caption(f"Member ID: {uid}")
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 MathPrepAI Global")

# --- 7. ROUTING & PAGE CONTENT ---

if menu == "🏠 Dashboard":
    st.title("Welcome to MathPrepAI Global Dashboard")
    st.write(f"Current Access: **{user_tier}** | User ID: **{uid}**")
    st.markdown("---")

    st.subheader("Your Toolkit")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 🧩 Fraction Factory\nVisual fraction models.")
        if st.button("Launch Tool", key="btn_frac"):
            st.session_state.menu_choice = "🧩 Fraction Factory"
            st.rerun()
            
    with col2:
        st.success("### ⚡ Speed Math\nArithmetic drill generator.")
        if st.button("Launch Tool", key="btn_speed"):
            st.session_state.menu_choice = "⚡ Speed Math Drills"
            st.rerun()
        
    with col3:
        st.warning("### 📐 Shape Master\nGeometric shapes.")
        if st.button("Launch Tool", key="btn_shape"):
            st.session_state.menu_choice = "📐 Shape Master"
            st.rerun()

    # (อาจารย์สามารถเพิ่ม Row 2 ตามโค้ดเดิมได้ที่นี่ครับ)

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
