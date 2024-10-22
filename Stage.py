import streamlit as st
from Electricity_bill import calculate_electricity_bill  # แก้ไขการนำเข้าให้เรียกฟังก์ชันที่ถูกต้อง
from Water_bill import calculate_water_bill  # แก้ไขการนำเข้าให้เรียกฟังก์ชันที่ถูกต้อง

# กำลังไฟของเครื่องใช้ไฟฟ้าเป็นวัตต์
appliances = {
    "พัดลม": 75,
    "ตู้เย็น": 150,
    "ทีวี": 100,
    "เครื่องปรับอากาศ": 1500,
    "เครื่องซักผ้า": 500,
    "เครื่องทำน้ำอุ่น": 3000,
    "หม้อหุงข้าว": 800,
    "หลอดไฟ": 10,
    "โคมไฟ": 15,
    "ที่ชาร์จแบตโทรศัพท์": 5,
    "คอมพิวเตอร์": 300,
    "โน๊ตบุ๊ค": 50
}

# แสดงชื่อโปรแกรม
st.title("โปรแกรมคำนวณค่าไฟฟ้าและค่าน้ำ")

# ส่วนสำหรับคำนวณค่าไฟฟ้า
st.subheader("คำนวณค่าไฟฟ้า (รวมค่า FT)")
selected_appliances = st.multiselect("เลือกเครื่องใช้ไฟฟ้า", list(appliances.keys()))

price_per_unit = st.number_input("กรอกค่าไฟต่อหน่วย (บาทต่อ kWh)", min_value=0.0, value=4.5, step=0.1)
ft_rate = st.number_input("กรอกค่า FT ต่อหน่วย (บาทต่อ kWh)", min_value=0.0, value=0.1, step=0.01)

if st.button("คำนวณค่าไฟ"):
    total_cost_with_ft_all = 0
    total_cost_all = 0
    total_ft_cost_all = 0

    for appliance_name in selected_appliances:
        power_watt = appliances[appliance_name]
        
        quantity = st.number_input(f"กรอกจำนวนเครื่องใช้ไฟฟ้าสำหรับ {appliance_name}", min_value=1, value=1, step=1, key=f"{appliance_name}_quantity")
        hours_per_day = st.number_input(f"กรอกจำนวนชั่วโมงที่ใช้ต่อวันสำหรับ {appliance_name}", min_value=0.0, value=8.0, step=1.0, key=f"{appliance_name}_hours")
        days = st.number_input(f"กรอกจำนวนวันที่ใช้สำหรับ {appliance_name}", min_value=1, value=30, step=1, key=f"{appliance_name}_days")

        # เรียกใช้ฟังก์ชันที่ถูกต้องเพื่อคำนวณค่าไฟฟ้า
        total_cost_with_ft, total_cost, ft_cost = calculate_electricity_bill(power_watt, hours_per_day, days, price_per_unit, ft_rate, quantity)
        
        total_cost_with_ft_all += total_cost_with_ft
        total_cost_all += total_cost
        total_ft_cost_all += ft_cost
        
        st.write(f"ค่าไฟของ {quantity} เครื่อง {appliance_name} (ไม่รวม FT): {total_cost:.2f} บาท")
        st.write(f"ค่า FT ของ {quantity} เครื่อง {appliance_name}: {ft_cost:.2f} บาท")
        st.write(f"ค่าไฟของ {quantity} เครื่อง {appliance_name} (รวม FT): {total_cost_with_ft:.2f} บาท")
        st.write("---")

    st.write(f"ค่าไฟรวมทั้งหมด (ไม่รวม FT): {total_cost_all:.2f} บาท")
    st.write(f"ค่า FT รวมทั้งหมด: {total_ft_cost_all:.2f} บาท")
    st.write(f"ค่าไฟรวมทั้งหมด (รวม FT): {total_cost_with_ft_all:.2f} บาท")

# ส่วนสำหรับคำนวณค่าน้ำ
st.subheader("คำนวณค่าน้ำ")
volume_used = st.number_input("กรอกจำนวนการใช้น้ำ (ลูกบาศก์เมตร)", min_value=0.0, value=0.0, step=0.1)
price_per_cubic_meter = st.number_input("กรอกค่าความน้ำน้อยต่อเมตร (บาทต่อ ลูกบาศก์เมตร)", min_value=0.0, value=10.0, step=0.1)

if st.button("คำนวณค่าน้ำ"):
    # เรียกใช้ฟังก์ชันที่ถูกต้องเพื่อคำนวณค่าน้ำ
    total_water_cost = calculate_water_bill(volume_used, price_per_cubic_meter)
    st.write(f"ค่าน้ำรวม: {total_water_cost:.2f} บาท")
