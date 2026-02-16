import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

def draw_fraction_circle(numerator, denominator):
    fig, ax = plt.subplots(figsize=(3, 3))
    # สร้าง Pie Chart
    sizes = [1] * denominator
    colors = ['#4CAF50' if i < numerator else '#FFFFFF' for i in range(denominator)]
    ax.pie(sizes, colors=colors, startangle=90, wedgeprops={'edgecolor': 'black', 'linewidth': 1})
    ax.set_title(f"Fraction: {numerator}/{denominator}")
    return fig

def draw_fraction_bar(numerator, denominator):
    fig, ax = plt.subplots(figsize=(5, 1))
    for i in range(denominator):
        color = '#2196F3' if i < numerator else '#FFFFFF'
        rect = plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(rect)
    ax.set_xlim(0, denominator)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    plt.axis('off')
    ax.set_title(f"Fraction: {numerator}/{denominator}")
    return fig

# --- UI Layout ---
st.title("🧩 Fraction Factory (Pro Version)")
st.subheader("สร้างโจทย์เศษส่วนพร้อมรูปภาพสำหรับคุณครู")

col1, col2 = st.columns(2)

with col1:
    type_shape = st.selectbox("เลือกรูปแบบรูปภาพ", ["วงกลm (Circle)", "แท่งสี่เหลี่ยม (Bar)"])
    denominator = st.number_input("ตัวส่วน (Denominator)", min_value=1, max_value=20, value=4)
    numerator = st.number_input("ตัวเศษ (Numerator)", min_value=0, max_value=denominator, value=1)

with col2:
    st.write("### ตัวอย่างรูปภาพ")
    if "วงกลม" in type_shape:
        fig = draw_fraction_circle(numerator, denominator)
    else:
        fig = draw_fraction_bar(numerator, denominator)
    st.pyplot(fig)

# --- PDF Generation (ตัวอย่างเบื้องต้น) ---
if st.button("📥 Export as PDF (Worksheet)"):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 800, "MathPrepAI: Fraction Worksheet")
    c.setFont("Helvetica", 12)
    c.drawString(100, 780, f"Name:................................................ Score:........../..........")
    
    # วาดโจทย์ข้อที่ 1 (ตัวอย่าง)
    c.drawString(100, 700, f"1) Write the fraction shown in the picture:")
    # ในขั้นตอนนี้เวอร์ชันเต็มจะใช้การ loop สุ่มโจทย์และวางรูปภาพลงใน PDF
    c.drawString(100, 600, "( [Image will be rendered here in full version] )")
    
    c.showPage()
    c.save()
    
    st.download_button(
        label="Download Worksheet",
        data=buf.getvalue(),
        file_name="fraction_worksheet.pdf",
        mime="application/pdf"
    )

st.info("💡 นี่คือ Prototype ส่วนการวาดรูปและคำนวณ ในเวอร์ชันขายจริง ระบบจะทำการ 'สุ่มโจทย์ 10-20 ข้อ' ลงในหน้าเดียวให้อัตโนมัติครับ")
