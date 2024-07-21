# db/database.py
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="todo_app.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    description TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    start_date DATE,
                    end_date DATE,
                    repeat INTEGER,  
                    completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)),
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)

    def add_user(self, username, password):
        with self.connection:
            self.connection.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

    def get_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return cursor.fetchone()

    def get_user_by_username(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

    def add_task_with_dates(self, description, user_id, start_date, end_date, repeat_value):
        with self.connection:
            self.connection.execute(
                "INSERT INTO tasks (description, completed, user_id, start_date, end_date, repeat) VALUES (?, ?, ?, ?, ?, ?)",
                (description, 0, user_id, start_date, end_date, repeat_value))

    def update_task_with_description(self, task_id, description):
        with self.connection:
            self.connection.execute(
                "UPDATE tasks set description = ? WHERE id = ?",
                (description, task_id))


    def get_tasks(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY id", (user_id,))
        return cursor.fetchall()

    def get_general_tasks(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE user_id = ? and start_date is null and tasks.end_date is null ORDER BY id",
            (user_id,))
        return cursor.fetchall()

    def get_scheduled_tasks(self, user_id):
        cursor = self.connection.cursor()
        today = datetime.today().strftime('%Y-%m-%d')
        cursor.execute(
            "SELECT * FROM tasks WHERE user_id = ? and (start_date is not null or tasks.end_date is not null) and (start_date >= ? or end_date <= ?) ORDER BY start_date",
            (user_id, today, today))
        return cursor.fetchall()

    def get_tasks_by_date(self, user_id, date):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM tasks 
            WHERE user_id = ? AND date(start_date) <= date(?) AND date(end_date) >= date(?)
            ORDER BY id
        """, (user_id, date, date))
        return cursor.fetchall()

    def delete_task(self, task_id):
        with self.connection:
            self.connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))



    def toggle_task_completion(self, task_id, completed):
        with self.connection:
            self.connection.execute(
                "UPDATE tasks set completed = ? WHERE id = ?",
                (completed, task_id))

