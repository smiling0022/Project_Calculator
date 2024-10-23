def calculate_electricity_bill(power_watt, hours_per_day, days, price_per_unit, ft_rate, quantity):
    # คำนวณหน่วยไฟฟ้า (kWh)
    energy_kwh = (power_watt / 1000) * hours_per_day * days * quantity

    # คำนวณค่าไฟฟ้า
    total_cost = energy_kwh * price_per_unit

    # คำนวณค่า FT
    ft_cost = energy_kwh * ft_rate

    # ค่าไฟรวม FT
    total_cost_with_ft = total_cost + ft_cost

    return total_cost_with_ft, total_cost, ft_cost
