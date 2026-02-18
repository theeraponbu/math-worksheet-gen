import streamlit as st
import fraction_factory
import speed_math
import shape_master
import graphing_notebook
import clock_generator
import pdf_editor
import hashlib
import hmac
from datetime import datetime

# --- 1. ระบบรักษาความปลอดภัย (ต้องตรงกับใน WordPress) ---
SECRET_KEY = "MATH_PREP_SECRET_99" # รหัสลับเดียวกับที่ใส่ใน WPCode

def validate_access(token, uid, tier):
    if not token or not uid:
        return False
    
    # คำนวณ Hash เพื่อตรวจสอบว่า Token นี้ส่งมาจากเว็บเราจริงๆ หรือไม่
    timestamp = datetime.now().strftime('%Y%m%d%H')
    expected_token = hmac.new(
        SECRET_KEY.encode(),
        (str(uid) + timestamp).encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(token, expected_token)

# --- 2. ฟังก์ชันตรวจสอบสิทธิ์สมาชิก ---
def get_tier_config(tier):
    if tier == 'pro_teacher' or tier == 'pro_seller':
        return {
            "is_pro": True,
            "max_pages": 30,
            "has_watermark": False,
            "show_branding": True # เช่น ชื่อครู/ชื่อโรงเรียน
        }
    else:
        return {
            "is_pro": False,
            "max_pages": 1,
            "has_watermark": True,
            "show_branding": False
        }

# --- 3. ส่วนหลักของแอป (Main Engine) ---
def run_math_engine():
    # ดึงค่าจาก URL ที่ WordPress ส่งมา
    query_params = st.query_params
    token = query_params.get("token")
    uid = query_params.get("uid")
    tier = query_params.get("tier", "free")

    # ตรวจสอบความปลอดภัย
    if not validate_access(token, uid, tier):
        st.error("❌ Access Denied: กรุณาเข้าใช้งานผ่านหน้า Dashboard ของ MathPrepAI.com")
        st.info("หากคุณล็อกอินแล้วแต่ยังเห็นข้อความนี้ โปรดรีเฟรชหน้า Dashboard อีกครั้ง")
        st.stop()

    # ดึงการตั้งค่าตามระดับสมาชิก
    config = get_tier_config(tier)

    # --- เริ่มแสดงผลหน้าจอ (UI) ---
    st.title("➕ Vertical Addition Worksheet")
    
    if not config["is_pro"]:
        st.warning("🔓 คุณกำลังใช้งานเวอร์ชันฟรี (ดาวน์โหลดได้ 1 หน้าและมีลายน้ำ)")
    
    # --- ใส่โค้ดสร้างโจทย์คณิตศาสตร์ที่ทำค้างไว้ตรงนี้ ---
    # (ใช้ค่า config["max_pages"] และ config["has_watermark"] ในการคุม PDF)
    
    st.write(f"Logged in as User ID: {uid} | Tier: {tier}")

if __name__ == "__main__":
    run_math_engine()
