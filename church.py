import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

# Create or ensure the CSV file exists
filename = "attendance_records.csv"
if not os.path.exists(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone Number", "Service", "Date", "Time"])

def register_attendance():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    service = service_var.get()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    if not name or not phone or not service:
        messagebox.showwarning("Missing Information", "Please fill out all fields.")
        return

    # Save to CSV
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, phone, service, date, time])

    messagebox.showinfo("Success", f"Attendance recorded for {name}!")
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    service_var.set("Select Service")

# GUI Setup
root = tk.Tk()
root.title("Sunday Service Attendance Registration")
root.geometry("400x300")
root.resizable(False, False)

# Labels and Entry fields
tk.Label(root, text="Name:", font=("Arial", 12)).pack(pady=5)
entry_name = tk.Entry(root, font=("Arial", 12))
entry_name.pack(pady=5)

tk.Label(root, text="Phone Number:", font=("Arial", 12)).pack(pady=5)
entry_phone = tk.Entry(root, font=("Arial", 12))
entry_phone.pack(pady=5)

tk.Label(root, text="Service Attended:", font=("Arial", 12)).pack(pady=5)
service_var = tk.StringVar(root)
service_var.set("Select Service")
services = ["First Service", "Second Service", "Third Service", "Evening Service"]
service_menu = tk.OptionMenu(root, service_var, *services)
service_menu.config(font=("Arial", 12))
service_menu.pack(pady=5)

# Submit Button
submit_btn = tk.Button(root, text="Register Attendance", font=("Arial", 12), command=register_attendance)
submit_btn.pack(pady=20)

root.mainloop()
