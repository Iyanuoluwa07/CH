import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import sqlite3
import csv
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

# Global password
ADMIN_PASSWORD = "admin123"

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
            relationship_status TEXT NOT NULL,
            service TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Admin Login
def admin_login(callback_function):
    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    login_window.geometry("300x150")
    login_window.resizable(False, False)

    ttk.Label(login_window, text="Enter Admin Password:").pack(pady=10)
    password_var = tk.StringVar()
    password_entry = ttk.Entry(login_window, textvariable=password_var, show="*")
    password_entry.pack(pady=5)

    def check_password():
        if password_var.get() == ADMIN_PASSWORD:
            login_window.destroy()
            callback_function()
        else:
            messagebox.showerror("Error", "Incorrect Password")

    ttk.Button(login_window, text="Login", command=check_password).pack(pady=10)

# Register Attendance
def register_attendance():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    address = entry_address.get().strip()
    relationship_status = relationship_var.get()
    service = service_var.get()
    date = date_picker.get_date().strftime("%Y-%m-%d")
    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    if not name or not phone or not address or not relationship_status or not service or not date:
        messagebox.showwarning("Missing Information", "Please fill all fields.")
        return

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO attendance (name, phone, address, relationship_status, service, date, time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone, address, relationship_status, service, date, time))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Attendance registered successfully!")
    clear_form()

def clear_form():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    relationship_var.set('')
    service_var.set('')
    date_picker.set_date(datetime.today())

# View Records
def view_records():
    records_window = tk.Toplevel(root)
    records_window.title("Attendance Records")
    records_window.geometry("1200x600")
    records_window.resizable(True, True)

    search_frame = ttk.Frame(records_window, padding=10)
    search_frame.pack(fill=tk.X)

    tk.Label(search_frame, text="Search by Name or Phone:", font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=5)
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
    search_entry.pack(side=tk.LEFT, padx=5)

    def search_records():
        keyword = search_var.get().strip()
        for row in tree.get_children():
            tree.delete(row)

        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        c.execute('''
            SELECT name, phone, address, relationship_status, service, date, time
            FROM attendance
            WHERE name LIKE ? OR phone LIKE ?
        ''', (f'%{keyword}%', f'%{keyword}%'))
        rows = c.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", tk.END, values=row)

    ttk.Button(search_frame, text="Search", command=search_records).pack(side=tk.LEFT, padx=5)

    columns = ("Name", "Phone", "Address", "Relationship Status", "Service", "Date", "Time")
    tree = ttk.Treeview(records_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT name, phone, address, relationship_status, service, date, time FROM attendance')
    rows = c.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

# Export to CSV
def export_to_csv():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filename:
        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        c.execute('SELECT name, phone, address, relationship_status, service, date, time FROM attendance')
        rows = c.fetchall()
        conn.close()

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Address", "Relationship Status", "Service", "Date", "Time"])
            writer.writerows(rows)

        messagebox.showinfo("Export Successful", f"Data exported successfully to {filename}")

# Export to PDF
def export_to_pdf():
    filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if filename:
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        # Church Title
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width/2, height-50, "Chapel of Glory, Region 22")
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height-80, "Attendance Records")

        conn = sqlite3.connect('attendance.db')
        cur = conn.cursor()
        cur.execute('SELECT name, phone, address, relationship_status, service, date, time FROM attendance')
        rows = cur.fetchall()
        conn.close()

        y = height - 120
        c.setFont("Helvetica", 10)

        headers = ["Name", "Phone", "Address", "Status", "Service", "Date", "Time"]
        xlist = [50, 150, 280, 400, 480, 570, 660]
        for idx, header in enumerate(headers):
            c.drawString(xlist[idx], y, header)

        y -= 20

        for row in rows:
            for idx, item in enumerate(row):
                c.drawString(xlist[idx], y, str(item))
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50

        c.save()
        messagebox.showinfo("Export Successful", f"Data exported successfully to {filename}")

# Monthly Summary
def monthly_summary():
    summary_window = tk.Toplevel(root)
    summary_window.title("Monthly Attendance Summary")
    summary_window.geometry("700x500")

    tree = ttk.Treeview(summary_window, columns=("Month", "Service", "Count"), show="headings")
    tree.heading("Month", text="Month")
    tree.heading("Service", text="Service")
    tree.heading("Count", text="Attendance Count")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        SELECT strftime('%Y-%m', date) as month, service, COUNT(*)
        FROM attendance
        GROUP BY month, service
    ''')
    rows = c.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

# Initialize database
init_db()

# Main Application Window
root = tk.Tk()
root.title("Chapel of Glory, Region 22 - Attendance Registration")
root.geometry("700x850")
root.resizable(True, True)
root.state('zoomed')

# Styling
style = ttk.Style()
style.theme_use('default')
style.configure('TLabel', font=('Segoe UI', 12))
style.configure('TButton', font=('Segoe UI', 11), padding=6)
style.configure('TEntry', font=('Segoe UI', 11))
style.configure('TCombobox', font=('Segoe UI', 11))

# Banner
banner_frame = ttk.Frame(root)
banner_frame.pack(pady=10)

try:
    banner_image = Image.open("church_logo.png")  # Your logo file
    banner_image = banner_image.resize((400, 100))
    banner_photo = ImageTk.PhotoImage(banner_image)
    logo_label = ttk.Label(banner_frame, image=banner_photo)
    logo_label.pack()
except Exception:
    ttk.Label(banner_frame, text="Chapel of Glory, Region 22", font=("Segoe UI", 24, 'bold')).pack()

# Form Card
card_frame = tk.Frame(root, bg="#f9f9f9", bd=2, relief="groove", padx=30, pady=30)
card_frame.pack(fill=tk.BOTH, expand=True, padx=100, pady=20)

# Form Fields
ttk.Label(card_frame, text="Full Name:").pack(anchor=tk.W, pady=2)
entry_name = ttk.Entry(card_frame, width=50)
entry_name.pack(pady=5)

ttk.Label(card_frame, text="Phone Number:").pack(anchor=tk.W, pady=2)
entry_phone = ttk.Entry(card_frame, width=50)
entry_phone.pack(pady=5)

ttk.Label(card_frame, text="Address:").pack(anchor=tk.W, pady=2)
entry_address = ttk.Entry(card_frame, width=50)
entry_address.pack(pady=5)

ttk.Label(card_frame, text="Relationship Status:").pack(anchor=tk.W, pady=2)
relationship_var = tk.StringVar()
relationship_combo = ttk.Combobox(card_frame, textvariable=relationship_var, state="readonly", values=["Single", "Engaged", "Married"], width=48)
relationship_combo.pack(pady=5)

ttk.Label(card_frame, text="Service:").pack(anchor=tk.W, pady=2)
service_var = tk.StringVar()
service_combo = ttk.Combobox(card_frame, textvariable=service_var, state="readonly", values=["Sunday Service", "Tuesday Service"], width=48)
service_combo.pack(pady=5)

ttk.Label(card_frame, text="Service Date:").pack(anchor=tk.W, pady=2)
date_picker = DateEntry(card_frame, width=50, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
date_picker.pack(pady=5)

# Buttons
button_frame = ttk.Frame(card_frame)
button_frame.pack(pady=20)

ttk.Button(button_frame, text="Register Attendance", command=register_attendance).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Clear Form", command=clear_form).grid(row=0, column=1, padx=10)
ttk.Button(card_frame, text="View Records", command=lambda: admin_login(view_records)).pack(pady=5)
ttk.Button(card_frame, text="Export Records to CSV", command=lambda: admin_login(export_to_csv)).pack(pady=5)
ttk.Button(card_frame, text="Export Records to PDF", command=lambda: admin_login(export_to_pdf)).pack(pady=5)
ttk.Button(card_frame, text="Monthly Summary", command=lambda: admin_login(monthly_summary)).pack(pady=5)

root.mainloop()
