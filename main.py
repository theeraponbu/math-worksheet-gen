import streamlit as st
import hashlib
import hmac
from datetime import datetime

# นำเข้าโมดูลของอาจารย์
import fraction_factory
import speed_math
import shape_master
import graphing_notebook
import clock_generator
import pdf_editor

# --- 1. CONFIGURATION & SECURITY ---
st.set_page_config(page_title="MathPrepAI Ultimate Pro", layout="wide")
SECRET_KEY = "MATH_PREP_SECRET_99" # ต้องตรงกับใน WordPress Snippet

def validate_access(token, uid):
    if not token or not uid: return False
    timestamp = datetime.now().strftime('%Y%m%d%H')
    expected_token = hmac.new(
        SECRET_KEY.encode(),
        (str(uid) + timestamp).encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(token, expected_token)

# --- 2. GET ACCESS DATA FROM URL ---
# ดึงค่าครั้งเดียวตอนโหลดแอปเพื่อป้องกัน Redirect Loop
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

# --- 3. CHECK ACCESS ---
if not st.session_state.access_verified:
    st.error("❌ Access Denied: กรุณาเข้าใช้งานผ่านหน้า Dashboard ของ MathPrepAI.com")
    st.stop()

user_tier = st.session_state.user_tier

# --- 4. NAVIGATION ---
if 'menu_choice' not in st.session_state:
    st.session_state.menu_choice = "🏠 Dashboard"

menu_list = [
    "🏠 Dashboard", "🧩 Fraction Factory", "⚡ Speed Math Drills", 
    "📐 Shape Master", "📉 Graphing Notebook", "🕒 Time & Clock", "📑 PDF Editor & Merger"
]

# Sidebar สำหรับเลือกเครื่องมือ
st.sidebar.title("🎓 MathPrepAI Workspace")
menu = st.sidebar.radio("SELECT TOOL:", menu_list, index=menu_list.index(st.session_state.menu_choice))
st.session_state.menu_choice = menu

st.sidebar.markdown("---")
if "pro" in user_tier:
    st.sidebar.success(f"🚀 {user_tier.upper()} ACTIVE")
else:
    st.sidebar.warning("🆓 FREE VERSION (Limited)")

# --- 5. ROUTING LOGIC ---
if menu == "🏠 Dashboard":
    st.title("Welcome to MathPrepAI Global Dashboard")
    st.write(f"Logged in User ID: **{st.session_state.uid}** | Tier: **{user_tier}**")
    st.markdown("---")
    
    # วาดปุ่มทางลัด (เหมือนโค้ดเก่าของอาจารย์)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 🧩 Fraction Factory")
        if st.button("Launch", key="btn_frac"):
            st.session_state.menu_choice = "🧩 Fraction Factory"
            st.rerun()
    # ... (อาจารย์สามารถก๊อปปี้ส่วน col2, col3 จากโค้ดเก่ามาใส่ต่อได้เลยครับ)

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
