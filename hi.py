#carbon footprint calculator with tkinter and matplotlib
import tkinter as tk
from tkinter import messagebox, Toplevel
import matplotlib.pyplot as plt

#Calculation Functions 
def calculate_travel_emission(km, mode):
    factors = {"car": 0.21, "bike": 0.05, "bus": 0.1, "walk": 0.0}
    return km * factors.get(mode.lower(), 0)

def calculate_electricity_emission(units):
    return units * 0.85  # kg CO2 per kWh

def calculate_plastic_emission(bottles):
    return bottles * 0.1  # kg CO2 per bottle

#Appliance Electricity Calculator
def open_appliance_calculator():
    def add_appliance():
        try:
            power = float(entry_power.get())
            hours = float(entry_hours.get())
            units = (power * hours) / 1000
            appliances_listbox.insert(tk.END, f"{power}W × {hours}h = {units:.2f} units")
            total_units.set(total_units.get() + units)
            entry_power.delete(0, tk.END)
            entry_hours.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers!")

    def finalize_units():
        entry_units.delete(0, tk.END)
        entry_units.insert(0, f"{total_units.get():.2f}")
        win.destroy()

    win = Toplevel(root)
    win.title("⚡ Appliance Unit Calculator")
    win.geometry("400x400")
    win.config(bg="#f0f8ff")

    tk.Label(win, text="Appliance Power (Watts):", bg="#f0f8ff").pack(pady=5)
    entry_power = tk.Entry(win)
    entry_power.pack()

    tk.Label(win, text="Usage Hours:", bg="#f0f8ff").pack(pady=5)
    entry_hours = tk.Entry(win)
    entry_hours.pack()

    tk.Button(win, text="Add Appliance", command=add_appliance, bg="blue", fg="white").pack(pady=10)

    appliances_listbox = tk.Listbox(win, width=40, height=10)
    appliances_listbox.pack(pady=10)

    total_units.set(0.0)
    tk.Button(win, text="Use Total Units", command=finalize_units, bg="green", fg="white").pack(pady=10)

#Main Calculation
def calculate():
    try:
        km = float(entry_km.get())
        mode = travel_mode.get()
        units = float(entry_units.get())
        bottles = int(entry_bottles.get())

        # Daily emissions
        travel_emission = calculate_travel_emission(km, mode)
        electricity_emission = calculate_electricity_emission(units)
        plastic_emission = calculate_plastic_emission(bottles)
        total_daily = travel_emission + electricity_emission + plastic_emission
        total_monthly = total_daily * 30

        # Tips based on largest contributor
        emissions = {"Travel": travel_emission, "Electricity": electricity_emission, "Plastic": plastic_emission}
        largest = max(emissions, key=emissions.get)
        tips_dict = {
            "Travel": "Try walking, cycling, or carpooling more.",
            "Electricity": "Switch off unused devices and use LED bulbs.",
            "Plastic": "Reduce single-use plastic and recycle."
        }
        tip = tips_dict[largest]

        #Show result
        result = (
            f"🌍 Daily Carbon Footprint 🌍\n"
            f"Travel: {travel_emission:.2f} kg CO2\n"
            f"Electricity: {electricity_emission:.2f} kg CO2\n"
            f"Plastic: {plastic_emission:.2f} kg CO2\n"
            f"--------------------------\n"
            f"Total Daily: {total_daily:.2f} kg CO2\n"
            f"Total Monthly: {total_monthly:.2f} kg CO2\n"
            f"\n💡 Tip: {tip}"
        )
        messagebox.showinfo("Result", result)
        if total_daily >10:
            messagebox.showwarning("Warning", "Your carbon footprint is quite high! Consider making changes to reduce it.")
        elif total_daily >5:
            messagebox.showinfo("Info", "Your carbon footprint is moderate. There's room for improvement!")
        else:
            messagebox.showinfo("Great!", "Your carbon footprint is low! Keep up the good work!")
       #Pie Chart
        labels = list(emissions.keys())
        values = list(emissions.values())
        colors = ["#66b3ff", "#99ff99", "#ff9999"]
        plt.figure(figsize=(5,5))
        plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
        plt.title("Daily Carbon Footprint Breakdown")
        plt.show()

        #Bar Chart for Monthly Footprint
        plt.figure(figsize=(6,4))
        plt.bar(labels, [v*30 for v in values], color=colors)
        plt.title("Monthly Carbon Footprint (kg CO2)")
        plt.ylabel("CO2 Emission (kg)")
        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")

#GUI Setup
root = tk.Tk()
root.title("🌱 Carbon Footprint Calculator")
root.geometry("450x450")
root.config(bg="#e6ffe6")

total_units = tk.DoubleVar(value=0.0)

#Input Fields
tk.Label(root, text="Daily Travel (km):", bg="#e6ffe6").pack(pady=5)
entry_km = tk.Entry(root)
entry_km.pack()

tk.Label(root, text="Mode of Travel:", bg="#e6ffe6").pack(pady=5)
travel_mode = tk.StringVar(value="car")
tk.OptionMenu(root, travel_mode, "car", "bike", "bus", "walk").pack()

tk.Label(root, text="Electricity Usage (units):", bg="#e6ffe6").pack(pady=5)
entry_units = tk.Entry(root)
entry_units.pack()

tk.Button(root, text="⚡ Calculate Units from Appliances", command=open_appliance_calculator, bg="orange", fg="black").pack(pady=5)

tk.Label(root, text="Plastic Bottles Used:", bg="#e6ffe6").pack(pady=5)
entry_bottles = tk.Entry(root)
entry_bottles.pack()

tk.Button(root, text="Calculate Carbon Footprint", command=calculate, bg="green", fg="white").pack(pady=20)

root.mainloop()
