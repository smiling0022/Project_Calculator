import streamlit as st
from Electricity_bill import calculate_electricity_bill  # ฟังก์ชันการคำนวณค่าไฟฟ้า
from Water_bill import calculate_water_bill  # ฟังก์ชันการคำนวณค่าน้ำ

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

# เริ่มเซสชันเพื่อติดตามข้อมูลต่างๆ
if 'appliance_counts' not in st.session_state:
    st.session_state.appliance_counts = {appliance: 0 for appliance in appliances.keys()}
    st.session_state.appliance_hours = {appliance: 0.0 for appliance in appliances.keys()}  # ใช้ float
    st.session_state.appliance_days = {appliance: 1 for appliance in appliances.keys()}  # ตั้งค่าเริ่มต้นเป็น 1

# แสดงชื่อโปรแกรม
st.title("โปรแกรมคำนวณค่าไฟฟ้าและค่าน้ำ พร้อมค่าเช่าบ้าน")

# ส่วนสำหรับคำนวณค่าไฟฟ้าและค่าน้ำ
st.subheader("คำนวณค่าไฟฟ้า (รวมค่า FT) และค่าน้ำ")

# แสดงรายชื่อเครื่องใช้ไฟฟ้าในรูปแบบติ๊ก
for appliance in appliances.keys():
    if st.checkbox(appliance, key=f"{appliance}_checkbox"):
        # กรอกจำนวนเครื่องใช้ไฟฟ้า
        quantity = st.number_input(f"กรอกจำนวน {appliance}:", min_value=1, value=1, key=f"{appliance}_quantity", step=1)
        st.session_state.appliance_counts[appliance] = quantity

        # กรอกจำนวนชั่วโมงที่ใช้ต่อวัน
        hours_per_day = st.number_input(f"กรอกจำนวนชั่วโมงที่ใช้ต่อวันสำหรับ {appliance}:",
                                         min_value=0.0, value=0.0, step=0.5, key=f"{appliance}_hours")
        st.session_state.appliance_hours[appliance] = hours_per_day

        # กรอกจำนวนวันที่ใช้
        days = st.number_input(f"กรอกจำนวนวันที่ใช้สำหรับ {appliance}:",
                               min_value=1, value=1, step=1, key=f"{appliance}_days")
        st.session_state.appliance_days[appliance] = days

# กรอกค่าความไฟฟ้า
price_per_unit = st.number_input("กรอกค่าไฟต่อหน่วย (บาทต่อ kWh)", min_value=0.0, value=4.5, step=0.1)
ft_rate = st.number_input("กรอกค่า FT ต่อหน่วย (บาทต่อ kWh)", min_value=0.0, value=0.1, step=0.01)

# ส่วนสำหรับค่าน้ำ
volume_used = st.number_input("กรอกจำนวนการใช้น้ำ (ลูกบาศก์เมตร)", min_value=0.0, value=0.0, step=0.1)
price_per_cubic_meter = st.number_input("กรอกค่าความน้ำน้อยต่อเมตร (บาทต่อ ลูกบาศก์เมตร)", min_value=0.0, value=10.0, step=0.1)

# ค่าเช่าบ้านและเงินเดือน
rent = st.number_input("กรอกค่าเช่าบ้าน (บาท)", min_value=0.0, value=5000.0, step=100.0)
salary = st.number_input("กรอกเงินเดือน (บาท)", min_value=0.0, value=30000.0, step=100.0)

if st.button("คำนวณค่าใช้จ่าย"):
    total_cost_with_ft_all = 0
    total_water_cost = 0

    # คำนวณค่าไฟฟ้า
    for appliance_name, quantity in st.session_state.appliance_counts.items():
        if quantity > 0:  # ถ้ามีการเลือกเครื่องใช้ไฟฟ้า
            power_watt = appliances[appliance_name]

            hours_per_day = st.session_state.appliance_hours[appliance_name]
            days = st.session_state.appliance_days[appliance_name]

            # เรียกใช้ฟังก์ชันที่ถูกต้องเพื่อคำนวณค่าไฟฟ้า
            total_cost_with_ft, total_cost, ft_cost = calculate_electricity_bill(power_watt, hours_per_day, days, price_per_unit, ft_rate, quantity)

            total_cost_with_ft_all += total_cost_with_ft

            # แสดงข้อมูลที่คำนวณสำหรับเครื่องใช้ไฟฟ้าแต่ละชนิด
            st.write(f"สำหรับ {quantity} เครื่องใช้ไฟฟ้า {appliance_name}:")
            st.write(f"  ค่าไฟ (รวม FT): {total_cost_with_ft:.2f} บาท")
            st.write(f"  ค่า FT: {ft_cost:.2f} บาท")
            st.write("---")

    # คำนวณค่าน้ำ
    total_water_cost = calculate_water_bill(volume_used, price_per_cubic_meter)

    # สรุปผลค่าใช้จ่ายทั้งหมด
    total_expenses = total_cost_with_ft_all + total_water_cost + rent
    remaining_money = salary - total_expenses

    st.write(f"ค่าไฟรวมทั้งหมด (รวม FT): {total_cost_with_ft_all:.2f} บาท")
    st.write(f"ค่าน้ำรวม: {total_water_cost:.2f} บาท")
    st.write(f"ค่าเช่าบ้าน: {rent:.2f} บาท")
    st.write(f"ยอดเงินเดือน: {salary:.2f} บาท")
    st.write(f"ยอดเงินเหลือหลังจากหักค่าใช้จ่ายทั้งหมด: {remaining_money:.2f} บาท")
