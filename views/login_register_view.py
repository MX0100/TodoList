import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController

class LoginRegisterWindow:
    def __init__(self, root, to_do_app):
        self.root = root
        self.to_do_app = to_do_app
        self.user_controller = UserController()

        self.login_frame = tk.Frame(root)
        self.login_frame.pack(pady=10)

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_btn = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_btn.grid(row=2, column=0, columnspan=2)

        self.register_btn = tk.Button(self.login_frame, text="Register", command=self.register)
        self.register_btn.grid(row=3, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = self.user_controller.login_user(username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.to_do_app.show_main_window()
        else:
            messagebox.showerror("Error", message)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = self.user_controller.register_user(username, password)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
