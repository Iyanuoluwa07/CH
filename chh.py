import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import datetime

# Set up the database
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            service TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_attendance():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    address = entry_address.get().strip()
    service = service_var.get()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    if not name or not phone or not address or not service:
        messagebox.showwarning("Missing Information", "Please fill all fields.")
        return

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO attendance (name, phone, address, service, date, time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, phone, address, service, date, time))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Attendance registered successfully!")
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    service_var.set('')

def view_records():
    records_window = tk.Toplevel(root)
    records_window.title("Attendance Records")
    records_window.geometry("800x400")

    tree = ttk.Treeview(records_window, columns=("Name", "Phone", "Address", "Service", "Date", "Time"), show='headings')
    for col in ("Name", "Phone", "Address", "Service", "Date", "Time"):
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)
    tree.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT name, phone, address, service, date, time FROM attendance')
    rows = c.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

def export_to_csv():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filename:
        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        c.execute('SELECT name, phone, address, service, date, time FROM attendance')
        rows = c.fetchall()
        conn.close()

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Address", "Service", "Date", "Time"])
            writer.writerows(rows)

        messagebox.showinfo("Export Successful", f"Data exported successfully to {filename}")

# Initialize database
init_db()

# Main Application Window
root = tk.Tk()
root.title("Church Attendance Registration")
root.geometry("450x500")
root.resizable(False, False)

# Styling
style = ttk.Style()
style.theme_use('default')  # Optional if you have a theme file
style.theme_use('default')

style.configure('TLabel', font=('Segoe UI', 10))
style.configure('TButton', font=('Segoe UI', 10), padding=6)
style.configure('TEntry', font=('Segoe UI', 10))
style.configure('TCombobox', font=('Segoe UI', 10))

# Frame for form
form_frame = ttk.Frame(root, padding=20)
form_frame.pack(fill=tk.BOTH, expand=True)

# Title
title_label = ttk.Label(form_frame, text="Attendance Registration", font=('Segoe UI', 16, 'bold'))
title_label.pack(pady=10)

# Form Fields
ttk.Label(form_frame, text="Full Name:").pack(anchor=tk.W, pady=2)
entry_name = ttk.Entry(form_frame, width=40)
entry_name.pack(pady=5)

ttk.Label(form_frame, text="Phone Number:").pack(anchor=tk.W, pady=2)
entry_phone = ttk.Entry(form_frame, width=40)
entry_phone.pack(pady=5)

ttk.Label(form_frame, text="Address:").pack(anchor=tk.W, pady=2)
entry_address = ttk.Entry(form_frame, width=40)
entry_address.pack(pady=5)

ttk.Label(form_frame, text="Service:").pack(anchor=tk.W, pady=2)
service_var = tk.StringVar()
service_combo = ttk.Combobox(form_frame, textvariable=service_var, state="readonly", values=["Sunday Service", "Tuesday Service"], width=38)
service_combo.pack(pady=5)

# Buttons
button_frame = ttk.Frame(form_frame)
button_frame.pack(pady=20)

ttk.Button(button_frame, text="Register Attendance", command=register_attendance).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="View Records", command=view_records).grid(row=0, column=1, padx=10)
ttk.Button(form_frame, text="Export Records to CSV", command=export_to_csv).pack(pady=5)

root.mainloop()
