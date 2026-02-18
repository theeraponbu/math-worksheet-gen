import streamlit as st
import hashlib
import hmac
from datetime import datetime

# นำเข้าโมดูลของอาจารย์ (มั่นใจว่าไฟล์เหล่านี้อยู่ใน GitHub เดียวกัน)
import fraction_factory
import speed_math
import shape_master
import graphing_notebook
import clock_generator
import pdf_editor

# --- 1. CONFIGURATION & SECURITY ---
st.set_page_config(page_title="MathPrepAI Ultimate Pro", layout="wide")
SECRET_KEY = "MATH_PREP_SECRET_99" 

def validate_access(token, uid):
    if not token or not uid: return False
    # บังคับใช้ UTC เพื่อให้ตรงกับ gmdate ใน PHP
    timestamp = datetime.utcnow().strftime('%Y%m%d%H')
    expected_token = hmac.new(
        SECRET_KEY.encode(),
        (str(uid) + timestamp).encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(token, expected_token)

# --- 2. GET ACCESS DATA FROM URL ---
if 'access_verified' not in st.session_state:
    params = st.query_params
    token = params.get("token")
    uid = params.get("uid")
    tier_from_url = params.get("tier", "free")
    
    if validate_access(token, uid):
        st.session_state.access_verified = True
        st.session_state.user_tier = tier_from_url
        st.session_state.uid = uid
    else:
        st.session_state.access_verified = False
        # เก็บค่าไว้ดูตอน Error โดยไม่ทำให้แอป Loop
        st.session_state.debug_msg = f"DEBUG: UID={uid}, Token={token}, Time={datetime.utcnow().strftime('%Y%m%d%H')}"

# --- 3. CHECK ACCESS ---
if st.session_state.access_verified is False:
    st.error("❌ Access Denied: กรุณาเข้าใช้งานผ่านหน้า Dashboard ของ MathPrepAI.com")
    if 'debug_msg' in st.session_state:
        st.warning(st.session_state.debug_msg)
    st.stop()

# --- 4. NAVIGATION ---
user_tier = st.session_state.user_tier
# ป้องกันค่า Error กรณีเข้าครั้งแรกแล้วไม่มีค่า
if 'menu_choice' not in st.session_state:
    st.session_state.menu_choice = "🏠 Dashboard"

menu_list = [
    "🏠 Dashboard", "🧩 Fraction Factory", "⚡ Speed Math Drills", 
    "📐 Shape Master", "📉 Graphing Notebook", "🕒 Time & Clock", "📑 PDF Editor & Merger"
]

st.sidebar.title("🎓 MathPrepAI Workspace")
menu = st.sidebar.radio("SELECT TOOL:", menu_list, index=menu_list.index(st.session_state.menu_choice))
st.session_state.menu_choice = menu

st.sidebar.markdown("---")
# เช็คคำว่า pro แบบไม่สนตัวพิมพ์เล็กใหญ่
if "pro" in user_tier.lower():
    st.sidebar.success(f"🚀 {user_tier.upper()} ACTIVE")
else:
    st.sidebar.warning("🆓 FREE VERSION (Limited)")

# --- 5. ROUTING LOGIC ---
if menu == "🏠 Dashboard":
    st.title("Welcome to MathPrepAI Global Dashboard")
    st.write(f"Logged in User ID: **{st.session_state.uid}** | Tier: **{user_tier}**")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 🧩 Fraction Factory")
        if st.button("Launch", key="btn_frac"):
            st.session_state.menu_choice = "🧩 Fraction Factory"
            st.rerun()
    # อาจารย์เพิ่มปุ่ม col2, col3 ต่อได้เลยครับ

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

st.sidebar.caption(f"© 2026 MathPrepAI | User: {st.session_state.uid}")
