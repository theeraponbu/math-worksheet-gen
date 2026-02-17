import streamlit as st
import random
from fpdf import FPDF
import io

# --- 1. PDF ENGINE CLASS ---
class SpeedMathPDF(FPDF):
    def header_setup(self, title, school, teacher):
        # ตั้งค่าฟอนต์มาตรฐานที่มากับ Library เพื่อความเร็วในการดาวน์โหลด
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, school.upper(), ln=True, align='C')
        
        self.set_font('Helvetica', 'B', 22)
        self.cell(0, 15, title, ln=True, align='C')
        
        self.set_font('Helvetica', '', 10)
        col_width = self.w / 2 - 10
        self.cell(col_width, 10, f"Teacher: {teacher}", ln=False)
        self.cell(0, 10, "Name: __________________________  Score: ______", ln=True, align='R')
        
        # เส้นคั่นหัวกระดาษ (Header Line)
        self.set_draw_color(46, 125, 50) # สีเขียวตามธีม
        self
