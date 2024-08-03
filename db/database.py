# db/database.py
import sqlite3
import hashlib
import os
from datetime import datetime
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.exceptions import InvalidKey


class RDBMSFactory:
    def __init__(self):
        pass

    def make_database(self, provider_name, uri_or_path, env='production'):
        provider_name = provider_name.lower()

        if provider_name == "sqlite":
            provider = sqlite3.connect(uri_or_path)
        elif provider_name == "mysql":
            pass
        elif provider_name == "oracle":
            pass
        elif provider_name.strip() == "microsoftsqlserver":
            pass
        else:
            raise Exception("DB provider not supported.")
        return provider

class Database:
    def __init__(self, uri_or_path="todo_app.db"):
        db_provider = RDBMSFactory().make_database('sqlite', uri_or_path)
        self.connection = db_provider
        self.create_tables()
        self.observers = set()

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

    def hash_password(self, password):
        # Salt should be securely stored and reused for the same user.
        salt = b'\x8F' * 16
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        return (salt + key).hex()  # Store salt + hash in database

    def verify_password(self, stored_password, provided_password):
        # salt = bytes.fromhex(stored_password[:32])
        # stored_key = bytes.fromhex(stored_password[32:])
        salt = stored_password[:16]
        stored_key = stored_password[16:]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        try:
            kdf.verify(provided_password.encode(), stored_key)
            return True
        except InvalidKey:
            return False

    def add_user(self, username, password):
        hashed_password = self.hash_password(password)
        with self.connection:
            self.connection.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.notify_observers()

    def get_user(self, username, password):
        hashed_password = self.hash_password(password)
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()
        if user and self.verify_password(bytes.fromhex(user[2]), password):
            return user
        return None

    def get_user_by_username(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

    def add_task_with_dates(self, description, user_id, start_date, end_date, repeat_value, password):
        encrypted_description = self.encrypt(description, password)
        with self.connection:
            self.connection.execute(
                "INSERT INTO tasks (description, completed, user_id, start_date, end_date, repeat) VALUES (?, ?, ?, ?, ?, ?)",
                (encrypted_description.hex(), 0, user_id, start_date, end_date, repeat_value))
            self.notify_observers()

    def update_task_with_description(self, task_id, description, password):
        encrypted_description = self.encrypt(description, password)
        with self.connection:
            self.connection.execute(
                "UPDATE tasks set description = ? WHERE id = ?",
                (encrypted_description.hex(), task_id))
            self.notify_observers()


    def get_tasks(self, user_id, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY id", (user_id,))
        tasks = cursor.fetchall()
        decrypted_tasks = []
        for task in tasks:
            decrypted_description = self.decrypt(bytes.fromhex(task[1]), password)
            decrypted_tasks.append((task[0], decrypted_description, task[2], task[3], task[4], task[5], task[6], task[7]))
        return decrypted_tasks

    def get_general_tasks(self, user_id, password):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE user_id = ? and start_date is null and tasks.end_date is null ORDER BY id",
            (user_id,))
        tasks = cursor.fetchall()
        decrypted_tasks = []
        for task in tasks:
            decrypted_description = self.decrypt(bytes.fromhex(task[1]), password)
            decrypted_tasks.append((task[0], decrypted_description, task[2], task[3], task[4], task[5], task[6], task[7]))
        return decrypted_tasks

    def get_scheduled_tasks(self, user_id, password):
        cursor = self.connection.cursor()
        today = datetime.today().strftime('%Y-%m-%d')
        cursor.execute(
            "SELECT * FROM tasks WHERE user_id = ? and (start_date is not null or tasks.end_date is not null) and (start_date >= ? or end_date <= ?) ORDER BY start_date",
            (user_id, today, today))
        tasks = cursor.fetchall()
        decrypted_tasks = []
        for task in tasks:
            decrypted_description = self.decrypt(bytes.fromhex(task[1]), password)
            decrypted_tasks.append((task[0], decrypted_description, task[2], task[3], task[4], task[5], task[6], task[7]))
        return decrypted_tasks

    def get_tasks_by_date(self, user_id, date, password):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM tasks 
            WHERE user_id = ? AND date(start_date) <= date(?) AND date(end_date) >= date(?)
            ORDER BY id
        """, (user_id, date, date))
        tasks = cursor.fetchall()
        decrypted_tasks = []
        for task in tasks:
            decrypted_description = self.decrypt(bytes.fromhex(task[1]), password)
            decrypted_tasks.append((task[0], decrypted_description, task[2], task[3], task[4], task[5], task[6], task[7]))
        return decrypted_tasks

    def delete_task(self, task_id):
        with self.connection:
            self.connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.notify_observers()

    def toggle_task_completion(self, task_id, completed):
        with self.connection:
            self.connection.execute(
                "UPDATE tasks set completed = ? WHERE id = ?",
                (completed, task_id))
            self.notify_observers()


    def encrypt(self, plaintext, password):
        salt = b'\x00' * 16  # Replace with a secure salt, must be stored and reused for the same user.
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted

    def decrypt(self, encrypted, password):
        salt = b'\x00' * 16  # Replace with a secure salt, must be stored and reused for the same user.
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        iv = encrypted[:16]
        encrypted = encrypted[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = PKCS7(128).unpadder()
        decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
        return decrypted.decode()

    def add_observer(self, observer):
        self.observers.add(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()
