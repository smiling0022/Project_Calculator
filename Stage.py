import streamlit as st

# ฟังก์ชันคำนวณค่าไฟ รวมค่า FT
def calculate_electricity_bill(power_watt, hours_per_day, days, price_per_unit, ft_rate, quantity):
    # คำนวณจำนวนกิโลวัตต์ชั่วโมงที่ใช้ (คูณด้วยจำนวนเครื่องใช้ไฟฟ้า)
    total_energy_kWh = (power_watt * hours_per_day * days * quantity) / 1000
    
    # คำนวณค่าไฟฟ้า (ไม่รวม FT)
    total_cost = total_energy_kWh * price_per_unit
    
    # บวกค่า FT เข้าไปในค่าไฟ
    ft_cost = total_energy_kWh * ft_rate
    total_cost_with_ft = total_cost + ft_cost
    
    return total_cost_with_ft, total_cost, ft_cost

# ข้อมูลเครื่องใช้ไฟฟ้า
appliances = {
    "พัดลม": 75,
    "ตู้เย็น": 150,
    "ทีวี": 100,
    "เครื่องปรับอากาศ": 1500,
    "เครื่องซักผ้า": 500
}

# แสดงหัวข้อในหน้า Streamlit
st.title("โปรแกรมคำนวณค่าไฟฟ้า (รวมค่า FT)")

# ตัวเลือกเครื่องใช้ไฟฟ้า (แบบ Multiselect)
selected_appliances = st.multiselect("เลือกเครื่องใช้ไฟฟ้า", list(appliances.keys()))

# ฟอร์มให้ผู้ใช้กรอกข้อมูลค่าไฟต่อหน่วย และค่า FT ต่อหน่วย (ค่าเดียวกันสำหรับทุกเครื่องใช้ไฟฟ้า)
price_per_unit = st.number_input("กรอกค่าไฟต่อหน่วย (บาทต่อ kWh)", min_value=0.0, value=4.5, step=0.1)
ft_rate = st.number_input("กรอกค่า FT ต่อหน่วย (บาทต่อ kWh)", min_value=0.0, value=0.1, step=0.01)

# การคำนวณและแสดงผล
if st.button("คำนวณค่าไฟ"):
    total_cost_with_ft_all = 0  # เก็บค่าไฟรวมทั้งหมด (รวมค่า FT)
    total_cost_all = 0          # เก็บค่าไฟรวมทั้งหมด (ไม่รวม FT)
    total_ft_cost_all = 0       # เก็บค่า FT รวมทั้งหมด

    # วนลูปผ่านเครื่องใช้ไฟฟ้าทั้งหมดที่เลือก
    for appliance_name in selected_appliances:
        power_watt = appliances[appliance_name]
        
        # ให้ผู้ใช้กรอกจำนวนเครื่องใช้ไฟฟ้า, จำนวนชั่วโมง และจำนวนวันที่แตกต่างกันสำหรับแต่ละเครื่องใช้ไฟฟ้า
        quantity = st.number_input(f"กรอกจำนวนเครื่องใช้ไฟฟ้าสำหรับ {appliance_name}", min_value=1, value=1, step=1, key=f"{appliance_name}_quantity")
        hours_per_day = st.number_input(f"กรอกจำนวนชั่วโมงที่ใช้ต่อวันสำหรับ {appliance_name}", min_value=0.0, value=8.0, step=1.0, key=f"{appliance_name}_hours")
        days = st.number_input(f"กรอกจำนวนวันที่ใช้สำหรับ {appliance_name}", min_value=1, value=30, step=1, key=f"{appliance_name}_days")

        # คำนวณค่าไฟฟ้าสำหรับเครื่องใช้ไฟฟ้าแต่ละชิ้น
        total_cost_with_ft, total_cost, ft_cost = calculate_electricity_bill(power_watt, hours_per_day, days, price_per_unit, ft_rate, quantity)
        
        # สะสมค่าไฟ
        total_cost_with_ft_all += total_cost_with_ft
        total_cost_all += total_cost
        total_ft_cost_all += ft_cost
        
        # แสดงผลค่าไฟของเครื่องใช้ไฟฟ้าแต่ละชิ้น
        st.write(f"ค่าไฟของ {quantity} เครื่อง {appliance_name} (ไม่รวม FT): {total_cost:.2f} บาท")
        st.write(f"ค่า FT ของ {quantity} เครื่อง {appliance_name}: {ft_cost:.2f} บาท")
        st.write(f"ค่าไฟของ {quantity} เครื่อง {appliance_name} (รวม FT): {total_cost_with_ft:.2f} บาท")
        st.write("---")

    # แสดงผลรวมค่าไฟของเครื่องใช้ไฟฟ้าทั้งหมด
    st.write(f"ค่าไฟรวมทั้งหมด (ไม่รวม FT): {total_cost_all:.2f} บาท")
    st.write(f"ค่า FT รวมทั้งหมด: {total_ft_cost_all:.2f} บาท")
    st.write(f"ค่าไฟรวมทั้งหมด (รวม FT): {total_cost_with_ft_all:.2f} บาท")
