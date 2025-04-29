import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
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
    service = service_var.get()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    if not name or not phone or not service:
        messagebox.showwarning("Missing Information", "Please fill all fields.")
        return

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO attendance (name, phone, service, date, time)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, phone, service, date, time))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Attendance registered successfully!")
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    service_var.set('')

def view_records():
    records_window = tk.Toplevel(root)
    records_window.title("Attendance Records")
    records_window.geometry("600x400")

    tree = ttk.Treeview(records_window, columns=("Name", "Phone", "Service", "Date", "Time"), show='headings')
    tree.heading("Name", text="Name")
    tree.heading("Phone", text="Phone")
    tree.heading("Service", text="Service")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT name, phone, service, date, time FROM attendance')
    rows = c.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

# Initialize database
init_db()

# Main Application Window
root = tk.Tk()
root.title("Sunday & Tuesday Service Attendance")
root.geometry("400x300")

# Labels and Entries
tk.Label(root, text="Full Name:").pack(pady=5)
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Phone Number:").pack(pady=5)
entry_phone = tk.Entry(root, width=40)
entry_phone.pack()

tk.Label(root, text="Service:").pack(pady=5)
service_var = tk.StringVar()
service_combo = ttk.Combobox(root, textvariable=service_var, state="readonly", values=["Sunday Service", "Tuesday Service"])
service_combo.pack()

# Buttons
tk.Button(root, text="Register Attendance", command=register_attendance).pack(pady=10)
tk.Button(root, text="View Attendance Records", command=view_records).pack()

root.mainloop()
