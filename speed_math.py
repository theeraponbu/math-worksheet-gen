import streamlit as st
import random
import pandas as pd

def generate_math_problems(num_items, digits, allow_carry, is_vertical):
    problems = []
    for i in range(num_items):
        if digits == 1: # หลักหน่วย
            a, b = random.randint(1, 9), random.randint(1, 9)
        elif digits == 2: # หลักสิบ
            if not allow_carry: # แบบไม่ทด
                a_unit, b_unit = random.randint(0, 4), random.randint(0, 4)
                a_ten, b_ten = random.randint(1, 4), random.randint(1, 4)
                a, b = (a_ten * 10 + a_unit), (b_ten * 10 + b_unit)
            else: # แบบมีทด (สุ่มปกติ)
                a, b = random.randint(10, 99), random.randint(10, 99)
        
        problems.append({"a": a, "b": b, "ans": a + b})
    return problems

def run_app():
    st.title("⚡ Speed Math Drills: Pro Edition")
    
    # ดึง Tier มาเช็ค (แต่เราจะเปิดให้เห็นฟีเจอร์ Pro ก่อนตามที่อาจารย์สั่ง)
    tier = st.session_state.get('tier', "Free Tier")
    
    with st.sidebar:
        st.header("⚙️ Problem Settings")
        # 1. เซตจำนวนข้อ
        num_probs = st.number_input("จำนวนข้อทั้งหมด", 10, 100, 20)
        
        # 2. เซตระดับความยาก (หลัก)
        digit_choice = st.selectbox("ระดับความยาก", ["1 หลัก (0-9)", "2 หลัก (10-99)", "3 หลัก (100-999)"])
        digits = int(digit_choice[0])
        
        # 3. เซตแบบ "มีตัวทด" หรือ "ไม่มีตัวทด" (ฟีเจอร์เด็ดสำหรับเด็กเล็ก)
        allow_carry = st.checkbox("อนุญาตให้มีตัวทด (Carry Over)", value=True)
        
        # 4. เซตแนวตั้งหรือแนวนอน
        layout_style = st.radio("รูปแบบโจทย์", ["แนวตั้ง (Vertical)", "แนวนอน (Horizontal)"])
        
        st.markdown("---")
        main_color = st.color_picker("สีธีมใบงาน", "#2e7d32")

    # --- การประมวลผล ---
    if 'current_problems' not in st.session_state or st.button("🔀 เจนโจทย์ใหม่"):
        st.session_state.current_problems = generate_math_problems(num_probs, digits, allow_carry, "Vertical" in layout_style)

    # --- ส่วน Preview ใบงาน ---
    st.subheader("📄 Preview: ใบงานการบวกเลข")
    
    # จัดหน้ากระดาษจำลอง
    with st.container():
        st.markdown(f"""
            <div style="border: 2px solid {main_color}; padding: 20px; border-radius: 10px; background-color: white;">
                <h2 style="color: {main_color}; text-align: center;">แบบฝึกหัดการบวกเลข ({digit_choice})</h2>
                <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                    <span>ชื่อ-นามสกุล: __________________________</span>
                    <span>คะแนน: ________/{num_probs}</span>
                </div>
                <hr>
            </div>
        """, unsafe_allow_html=True)

        # แสดงโจทย์เป็น Grid
        cols = st.columns(4)
        for idx, p in enumerate(st.session_state.current_problems):
            with cols[idx % 4]:
                if "Vertical" in layout_style:
                    st.markdown(f"""
                        <div style="text-align: right; font-family: monospace; font-size: 20px; margin: 10px; padding: 10px; border-bottom: 1px solid #eee;">
                            {idx+1}) &nbsp;&nbsp;{p['a']}<br>
                            +&nbsp;{p['b']}<br>
                            <hr style="margin: 5px 0;">
                            <br>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='font-size: 18px; margin: 10px;'>{idx+1}) {p['a']} + {p['b']} = ____</div>", unsafe_allow_html=True)

    # --- ฟีเจอร์ Pro: ใบเฉลย ---
    st.markdown("---")
    with st.expander("🔑 ดูใบเฉลย (Answer Key - Pro Only)"):
        ans_cols = st.columns(5)
        for idx, p in enumerate(st.session_state.current_problems):
            ans_cols[idx % 5].write(f"ข้อ {idx+1}: **{p['ans']}**")

    # --- ระบบดาวน์โหลด (พร้อมเช็คสิทธิ์) ---
    if st.button("📥 ดาวน์โหลดใบงาน PDF"):
        if tier == "Free Tier":
            st.error("🔒 ฟีเจอร์ดาวน์โหลด PDF สำหรับสมาชิก Pro เท่านั้น หรือใช้ 1 เครดิต")
        else:
            st.success("กำลังสร้างไฟล์ PDF คุณภาพสูง...")
