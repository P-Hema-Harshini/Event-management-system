import tkinter as tk
from tkinter import messagebox
from event_management import create_event, view_events
from assignments import view_assignments, submit_assignment

def open_create_event(teacher_id):
    create_event(teacher_id)

def open_view_events():
    view_events()

def open_view_assignments(user_id, role):
    view_assignments(user_id, role)

def open_submit_assignment(user_id):
    submit_assignment(user_id)

def home_page(user_id, role):
    root = tk.Tk()
    root.title("Event Management System - Home")
    root.geometry("400x400")

    tk.Label(root, text=f"Welcome {role}!", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="📅 View All Events", command=open_view_events).pack(pady=5)

    if role == "Admin":
        tk.Button(root, text="🛠 Manage Users", command=lambda: messagebox.showinfo("Admin", "User management coming soon!")).pack(pady=5)
        tk.Button(root, text="📂 Manage Events", command=lambda: messagebox.showinfo("Admin", "Event management coming soon!")).pack(pady=5)

    elif role == "Teacher":
        tk.Button(root, text="➕ Create Event", command=lambda: open_create_event(user_id)).pack(pady=5)
        tk.Button(root, text="📜 View Assignments", command=lambda: open_view_assignments(user_id, role)).pack(pady=5)

    elif role == "Student":
        tk.Button(root, text="📩 Submit Assignment", command=lambda: open_submit_assignment(user_id)).pack(pady=5)
        tk.Button(root, text="📜 My Assignments", command=lambda: open_view_assignments(user_id, role)).pack(pady=5)

    tk.Button(root, text="🔑 Logout", command=root.destroy).pack(pady=10)

    root.mainloop()
