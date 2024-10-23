# Electricity_bill.py

def calculate_electricity_bill(power_watt, hours_per_day, days, price_per_unit, ft_rate, quantity):
    # คำนวณจำนวนกิโลวัตต์ชั่วโมงที่ใช้
    total_energy_kWh = (power_watt * hours_per_day * days * quantity) / 1000
    
    # คำนวณค่าใช้จ่าย (ไม่รวมค่า FT)
    total_cost = total_energy_kWh * price_per_unit
    
    # คำนวณค่า FT
    ft_cost = total_energy_kWh * ft_rate
    
    # รวมค่าใช้จ่ายกับค่า FT
    total_cost_with_ft = total_cost + ft_cost
    
    return total_cost_with_ft, total_cost, ft_cost