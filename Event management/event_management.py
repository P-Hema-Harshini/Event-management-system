import tkinter as tk
from tkinter import messagebox
from database_setup import connect_db

def create_event(teacher_id):
    def save_event():
        name = entry_name.get()
        description = entry_desc.get()
        start_date = entry_start.get()
        end_date = entry_end.get()

        if not name or not start_date or not end_date:
            messagebox.showerror("Error", "Please fill all required fields")
            return

        conn = connect_db()
        cursor = conn.cursor()

        query = """INSERT INTO events (name, description, teacher_id, start_date, end_date) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (name, description, teacher_id, start_date, end_date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Event Created Successfully")
        event_window.destroy()

    event_window = tk.Tk()
    event_window.title("Create Event")

    tk.Label(event_window, text="Event Name:").pack()
    entry_name = tk.Entry(event_window)
    entry_name.pack()

    tk.Label(event_window, text="Description:").pack()
    entry_desc = tk.Entry(event_window)
    entry_desc.pack()

    tk.Label(event_window, text="Start Date (YYYY-MM-DD):").pack()
    entry_start = tk.Entry(event_window)
    entry_start.pack()

    tk.Label(event_window, text="End Date (YYYY-MM-DD):").pack()
    entry_end = tk.Entry(event_window)
    entry_end.pack()

    tk.Button(event_window, text="Create", command=save_event).pack()

    event_window.mainloop()

def view_events():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, start_date, end_date FROM events")
    events = cursor.fetchall()
    conn.close()

    event_window = tk.Tk()
    event_window.title("All Events")

    tk.Label(event_window, text="Events", font=("Arial", 14)).pack(pady=5)

    for event in events:
        event_text = f"{event[0]} - {event[1]} ({event[2]} to {event[3]})"
        tk.Label(event_window, text=event_text).pack()

    event_window.mainloop()
