import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Honey.Chintu",  # Replace with your actual password
            database="event_management"
        )
        print("✅ Database Connected Successfully!")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
        return None
