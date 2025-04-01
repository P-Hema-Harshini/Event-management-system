import tkinter as tk
from tkinter import messagebox
import mysql.connector
from database_setup import connect_db  # Import database connection function

# Function to register a new user
def register():
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    role = role_var.get()  # Get the selected role

    if not name or not email or not password or not role:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, password, role))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            root.destroy()  # Close the window after registration
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            cursor.close()
            conn.close()

# Create Tkinter window
root = tk.Tk()
root.title("User Registration")
root.geometry("350x300")

# UI Elements
tk.Label(root, text="Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Email:").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, show="*")  # Hide password
password_entry.pack()

tk.Label(root, text="Role:").pack()
role_var = tk.StringVar()
role_var.set("Student")  # Default role
tk.OptionMenu(root, role_var, "Admin", "Teacher", "Student").pack()

register_button = tk.Button(root, text="Register", command=register)
register_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
