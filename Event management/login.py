import tkinter as tk
from tkinter import messagebox
from database_setup import connect_db
from main import home_page

def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT id, role FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_id, role = user
        messagebox.showinfo("Login Successful", f"Welcome {username} ({role})")
        root.destroy()  # Close login window
        home_page(user_id, role)  # Open Home Page AFTER successful login
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Create Login Window
root = tk.Tk()
root.title("Login - Event Management System")

tk.Label(root, text="Username:").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password:").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()
