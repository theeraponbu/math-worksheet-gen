import streamlit as st

# ตั้งค่าหน้ากระดาษให้ดูเป็นมืออาชีพ
st.set_page_config(page_title="MathPrepAI Workspace", layout="wide")

# ส่วนของแถบเมนูด้านข้าง
st.sidebar.image("https://mathprepai.com/wp-content/uploads/logo.png", width=200) # ใส่ลิงก์โลโก้เว็บอาจารย์
st.sidebar.title("🛠️ เมนูเครื่องมือ")
choice = st.sidebar.radio("เลือกแอปที่ต้องการใช้งาน:", 
                         ["🏠 หน้าแรก", "🧩 Fraction Factory", "⚡ Speed Math (Coming Soon)"])

# --- ตรรกะการเลือกหน้า ---
if choice == "🏠 หน้าแรก":
    st.title("ยินดีต้อนรับสู่ MathPrepAI Pro Workspace")
    st.write("กรุณาเลือกเครื่องมือที่แถบด้านซ้ายเพื่อเริ่มต้นสร้างใบงานครับ")
    
    # โชว์ Card แนะนำสั้นๆ
    col1, col2 = st.columns(2)
    with col1:
        st.info("🧩 **Fraction Factory**: สร้างรูปภาพเศษส่วนและใบงาน")
    with col2:
        st.warning("⚡ **Speed Math**: สร้างโจทย์คิดเลขเร็ว (เร็วๆ นี้)")

elif choice == "🧩 Fraction Factory":
    # เรียกไฟล์แอปเศษส่วนมาแสดง
    try:
        import fraction_factory
        # ถ้าอาจารย์ปรับโค้ดใน fraction_factory เป็นฟังก์ชัน ก็เรียกใช้ที่นี่ครับ
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดแอป: {e}")
