import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Honey.Chintu',
        database='event_management'
    )

def create_event():
    event_name = event_name_entry.get()
    event_description = event_desc_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    teacher_id = 1  # Replace with logged-in teacher's ID
    
    if not event_name or not start_date or not end_date:
        messagebox.showerror("Error", "Event Name, Start Date, and End Date are required!")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO events (name, description, teacher_id, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (event_name, event_description, teacher_id, start_date, end_date))
        conn.commit()
        messagebox.showinfo("Success", "Event created successfully!")
        load_events()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        cursor.close()
        conn.close()

def load_events():
    for row in tree.get_children():
        tree.delete(row)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, start_date, end_date FROM events")
    events = cursor.fetchall()
    conn.close()
    
    for event in events:
        tree.insert("", "end", values=event)

def submit_assignment():
    event_id = event_id_entry.get()
    student_id = student_id_entry.get()
    file_path = file_path_entry.get()
    
    if not event_id or not student_id or not file_path:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO assignments (event_id, student_id, file_path, status)
            VALUES (%s, %s, %s, 'Pending')
        """, (event_id, student_id, file_path))
        conn.commit()
        messagebox.showinfo("Success", "Assignment submitted successfully!")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        cursor.close()
        conn.close()

def view_assignments(teacher_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Get assignments related to events managed by this teacher
    query = """
    SELECT assignments.id, events.name, users.username, assignments.file_path, assignments.status
    FROM assignments
    JOIN events ON assignments.event_id = events.id
    JOIN users ON assignments.student_id = users.id
    WHERE events.teacher_id = %s
    """
    cursor.execute(query, (teacher_id,))
    assignments = cursor.fetchall()
    conn.close()

    # Create a new window for viewing assignments
    view_window = tk.Toplevel()
    view_window.title("Submitted Assignments")

    # Table for displaying assignments
    tree = ttk.Treeview(view_window, columns=("ID", "Event", "Student", "File", "Status"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Event", text="Event")
    tree.heading("Student", text="Student")
    tree.heading("File", text="File")
    tree.heading("Status", text="Status")

    # Insert assignments into the table
    for assignment in assignments:
        tree.insert("", "end", values=assignment)

    tree.pack(expand=True, fill="both")

# Example usage (Replace `teacher_id` with actual ID)
# view_assignments(teacher_id)
# Tkinter UI
root = tk.Tk()
root.title("Event Management System")

tk.Label(root, text="Event Name:").grid(row=0, column=0)
event_name_entry = tk.Entry(root)
event_name_entry.grid(row=0, column=1)

tk.Label(root, text="Description:").grid(row=1, column=0)
event_desc_entry = tk.Entry(root)
event_desc_entry.grid(row=1, column=1)

tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0)
start_date_entry = tk.Entry(root)
start_date_entry.grid(row=2, column=1)

tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=3, column=0)
end_date_entry = tk.Entry(root)
end_date_entry.grid(row=3, column=1)

tk.Button(root, text="Create Event", command=create_event).grid(row=4, column=0, columnspan=2)

# Event Listing
columns = ("ID", "Name", "Start Date", "End Date")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.grid(row=5, column=0, columnspan=2)

load_events()

# Assignment Submission
tk.Label(root, text="Event ID:").grid(row=6, column=0)
event_id_entry = tk.Entry(root)
event_id_entry.grid(row=6, column=1)

tk.Label(root, text="Student ID:").grid(row=7, column=0)
student_id_entry = tk.Entry(root)
student_id_entry.grid(row=7, column=1)

tk.Label(root, text="File Path:").grid(row=8, column=0)
file_path_entry = tk.Entry(root)
file_path_entry.grid(row=8, column=1)

tk.Button(root, text="Submit Assignment", command=submit_assignment).grid(row=9, column=0, columnspan=2)

root.mainloop()
