# water_calculator.py

def calculate_water_bill(volume_used, price_per_cubic_meter):
    # คำนวณค่าใช้น้ำจากจำนวนที่ใช้ (ลบค่าเป็นเมตร)
    total_cost = volume_used * price_per_cubic_meter
    return total_cost

