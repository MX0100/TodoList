import sqlite3

def update_table_structure(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN start_date DATE")
        cursor.execute("ALTER TABLE tasks ADD COLUMN end_date DATE")
        cursor.execute("ALTER TABLE tasks ADD COLUMN repeat TEXT")
        print("Table structure updated successfully")
    except sqlite3.OperationalError as e:
        print(f"Error updating table structure: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_name = 'todo_app.db'
    update_table_structure(db_name)
