import streamlit as st
from Electricity_bill import calculate_electricity_bill  # นำเข้าโมดูลสำหรับคำนวณค่าไฟฟ้า
from Water_bill import calculate_water_bill  # นำเข้าโมดูลสำหรับคำนวณค่าน้ำ

# กำหนดพลังงานของเครื่องใช้ไฟฟ้าเป็นวัตต์
appliances = {
    "พัดลม": 75,
    "ตู้เย็น": 70,
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

# เพิ่ม CSS สำหรับสไตล์โดยมีพื้นหลังเป็นภาพ
st.markdown("""
    <style>
    .stApp {
        background-image: url('img//ฺBack.jpg'); 
        background-size: cover; /* ปรับให้ภาพครอบคลุมหน้าจอทั้งหมด */
        background-position: center; /* จัดให้อยู่ตรงกลาง */
        color: #333333;
        font-family: 'Arial', sans-serif; /* กำหนดฟอนต์ */
    }
    h1, h2, h3 {
        color: #6a1b9a; /* กำหนดสีฟอนต์สำหรับหัวข้อ */
    }
    .stButton > button {
        background-color: #ffd1dc; /* สีพื้นหลังของปุ่ม */
        color: #333; /* สีข้อความในปุ่ม */
        border-radius: 10px; /* ขอบมน */
        padding: 10px 20px; /* ขนาดของปุ่ม */
        font-size: 18px; /* ขนาดฟอนต์ของข้อความในปุ่ม */
        transition: background-color 0.3s; /* การเปลี่ยนสีเมื่อเลื่อนเมาส์ */
    }
    .stButton > button:hover {
        background-color: #f8b8c4; /* สีพื้นหลังของปุ่มเมื่อเลื่อนเมาส์ */
        color: white; /* สีข้อความเมื่อเลื่อนเมาส์ */
    }
    .stNumberInput input {
        background-color: #f0f4c3; /* สีพื้นหลังของช่องกรอกจำนวน */
        border: 1px solid #dcedc8; /* เส้นขอบ */
        border-radius: 8px; /* ขอบมน */
    }
    .stCheckbox {
        background-color: #e1bee7; /* สีพื้นหลังของ Checkbox */
        padding: 10px; /* ขนาดของ Checkbox */
        border-radius: 8px; /* ขอบมน */
    }
    .result-box {
        background-color: rgba(243, 229, 245, 0.9); /* กล่องผลลัพธ์ที่มีความโปร่งใส */
        padding: 15px; /* ขนาดของกล่อง */
        border-radius: 10px; /* ขอบมน */
        margin-bottom: 20px; /* ระยะห่างด้านล่าง */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* เงา */
    }
    .input-box {
        background-color: rgba(255, 243, 224, 0.8); /* สีพื้นหลังของกล่องกรอกข้อมูล */
        padding: 15px; /* ขนาดของกล่อง */
        border-radius: 10px; /* ขอบมน */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* เงา */
        margin-bottom: 20px; /* ระยะห่างด้านล่าง */
    }
    </style>
    """, unsafe_allow_html=True)  # อนุญาตให้ใช้ HTML ที่ไม่ปลอดภัย

# เริ่มต้นสถานะเซสชันเพื่อติดตามข้อมูลต่าง ๆ
if 'appliance_counts' not in st.session_state:
    st.session_state.appliance_counts = {appliance: 0 for appliance in appliances.keys()}  # จำนวนเครื่องใช้ไฟฟ้า
    st.session_state.appliance_hours = {appliance: 0.0 for appliance in appliances.keys()}  # ชั่วโมงที่ใช้
    st.session_state.appliance_days = {appliance: 1 for appliance in appliances.keys()}  # จำนวนวันที่ใช้

# แสดงชื่อโปรแกรม
st.title("RentSmart")

# แบ่งหน้าจออกเป็นสองคอลัมน์: คอลัมน์สำหรับกรอกข้อมูลด้านซ้าย และคอลัมน์สำหรับผลลัพธ์ด้านขวา
col1, col2 = st.columns(2)

# คอลัมน์ซ้าย (กรอกข้อมูล)
with col1:
    st.subheader("กรอกข้อมูล")  # หัวข้อสำหรับกรอกข้อมูล
    st.markdown('<div class="input-box">', unsafe_allow_html=True)  # เริ่มต้นกล่องกรอกข้อมูล

    # แสดงรายการเครื่องใช้ไฟฟ้าเป็น Checkbox
    for appliance in appliances.keys():
        if st.checkbox(appliance, key=f"{appliance}_checkbox"):  # ถ้าผู้ใช้เลือกเครื่องใช้ไฟฟ้า
            # กรอกจำนวนเครื่องใช้ไฟฟ้า
            quantity = st.number_input(f"กรอกจำนวน {appliance}:", min_value=1, value=1, key=f"{appliance}_quantity", step=1)
            st.session_state.appliance_counts[appliance] = quantity  # บันทึกจำนวนเครื่องใช้ไฟฟ้า

            # กรอกชั่วโมงที่ใช้ต่อวัน
            hours_per_day = st.number_input(f"กรอกจำนวนชั่วโมงที่ใช้ต่อวันสำหรับ {appliance}:",
                                            min_value=0.0, value=0.0, step=0.5, key=f"{appliance}_hours")
            st.session_state.appliance_hours[appliance] = hours_per_day  # บันทึกชั่วโมงที่ใช้

            # กรอกจำนวนวันที่ใช้
            days = st.number_input(f"กรอกจำนวนวันที่ใช้สำหรับ {appliance}:",
                                min_value=1, value=1, step=1, key=f"{appliance}_days")
            st.session_state.appliance_days[appliance] = days  # บันทึกจำนวนวันที่ใช้

    # กรอกค่าไฟฟ้าและค่าน้ำ
    price_per_unit = st.number_input("กรอกค่าไฟต่อหน่วย (บาทต่อ kWh)", min_value=0.0, value=4.5, step=0.1)  # ค่าไฟฟ้าต่อหน่วย
    ft_rate = st.number_input("กรอกค่า FT ต่อหน่วย (บาทต่อ kWh)", min_value=0.0, value=0.1, step=0.01)  # ค่า FT

    # กรอกข้อมูลการใช้น้ำ
    volume_used = st.number_input("กรอกจำนวนการใช้น้ำ (ลูกบาศก์เมตร)", min_value=0.0, value=0.0, step=0.1)  # ปริมาณน้ำที่ใช้
    price_per_cubic_meter = st.number_input("กรอกค่าความน้ำน้อยต่อเมตร (บาทต่อ ลูกบาศก์เมตร)", min_value=0.0, value=10.0, step=0.1)  # ค่าน้ำต่อลูกบาศก์เมตร

    # กรอกค่าเช่าและเงินเดือน
    rent = st.number_input("กรอกค่าเช่าบ้าน (บาท)", min_value=0.0, value=5000.0, step=100.0)  # ค่าเช่าบ้าน
    salary = st.number_input("กรอกเงินเดือน (บาท)", min_value=0.0, value=30000.0, step=100.0)  # เงินเดือน

    st.markdown('</div>', unsafe_allow_html=True)  # สิ้นสุดกล่องกรอกข้อมูล

# คอลัมน์ขวา (ผลลัพธ์)
with col2:
    st.subheader("ผลลัพธ์")  # หัวข้อสำหรับผลลัพธ์
    
    if st.button("คำนวณค่าใช้จ่าย"):  # ปุ่มสำหรับคำนวณค่าใช้จ่าย
        total_cost_with_ft_all = 0  # ตัวแปรสำหรับเก็บค่าใช้จ่ายทั้งหมดรวม FT
        total_water_cost = 0  # ตัวแปรสำหรับเก็บค่าค่าน้ำทั้งหมด

        # คำนวณค่าไฟฟ้า
        for appliance_name, quantity in st.session_state.appliance_counts.items():
            if quantity > 0:  # ถ้ามีการเลือกเครื่องใช้ไฟฟ้า
                power_watt = appliances[appliance_name]  # รับค่าพลังงานของเครื่องใช้ไฟฟ้า

                hours_per_day = st.session_state.appliance_hours[appliance_name]  # รับชั่วโมงที่ใช้
                days = st.session_state.appliance_days[appliance_name]  # รับจำนวนวันที่ใช้

                # เรียกใช้ฟังก์ชันสำหรับคำนวณค่าไฟฟ้า
                total_cost_with_ft, total_cost, ft_cost = calculate_electricity_bill(power_watt, hours_per_day, days, price_per_unit, ft_rate, quantity)

                total_cost_with_ft_all += total_cost_with_ft  # เพิ่มค่าใช้จ่ายรวม FT

                # แสดงข้อมูลที่คำนวณได้สำหรับแต่ละเครื่องใช้ไฟฟ้า
                st.write(f"สำหรับ {quantity} เครื่องใช้ไฟฟ้า {appliance_name}:")
                st.write(f"  ค่าไฟ (รวม FT): {total_cost_with_ft:.2f} บาท")  # แสดงค่าไฟรวม FT
                st.write(f"  ค่า FT: {ft_cost:.2f} บาท")  # แสดงค่า FT
                st.write("---")  # เส้นแบ่ง

        # คำนวณค่าค่าน้ำ
        total_water_cost = calculate_water_bill(volume_used, price_per_cubic_meter)  # เรียกฟังก์ชันคำนวณค่าน้ำ

        # สรุปค่าใช้จ่ายทั้งหมด
        total_expenses = total_cost_with_ft_all + total_water_cost + rent  # คำนวณค่าใช้จ่ายรวม
        remaining_money = salary - total_expenses  # คำนวณยอดเงินที่เหลือหลังหักค่าใช้จ่าย

        st.markdown(f"""
            <div class="result-box">
            <h3>ค่าใช้จ่ายทั้งหมด</h3>
            <p>ค่าไฟรวมทั้งหมด (รวม FT): {total_cost_with_ft_all:.2f} บาท</p>  # แสดงค่าไฟรวม
            <p>ค่าน้ำรวม: {total_water_cost:.2f} บาท</p>  # แสดงค่าน้ำรวม
            <p>ค่าเช่าบ้าน: {rent:.2f} บาท</p>  # แสดงค่าเช่าบ้าน
            <p>ยอดเงินเดือน: {salary:.2f} บาท</p>  # แสดงเงินเดือน
            <p><strong>ยอดเงินเหลือหลังจากหักค่าใช้จ่ายทั้งหมด: {remaining_money:.2f} บาท</strong></p>  # แสดงยอดเงินเหลือ
            </div>
        """, unsafe_allow_html=True)  # แสดงผลลัพธ์ในกล่อง
