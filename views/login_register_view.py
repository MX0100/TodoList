import tkinter as _tk
from tkinter import ttk as tk
from tkinter import messagebox
from controllers.user_controller import UserController
from tkinter import TclError
from tkinter import PhotoImage
import os

class LoginRegisterWindow:
    def __init__(self, root, to_do_app,user_controller):
        self.root = root
        self.root.geometry("580x380")
        self.to_do_app = to_do_app
        self.user_controller = user_controller

        cover_path = os.sep.join([
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            "resources/purple_book.png"
        ])

        # Load the image
        self.bg = PhotoImage(file=cover_path)

        # Create a canvas
        self.canvas = _tk.Canvas(root, width=580, height=380)
        self.canvas.pack(fill="both", expand=True)
        
        # Add the image to the canvas
        self.canvas.create_image(-30, -60, image=self.bg, anchor="nw")

        # Create a frame
        self.login_frame = _tk.Frame(root, background='#C5E9F1')
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)
        self.username_entry.bind('<Return>', self.entry_next)

        tk.Label(self.login_frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)
        self.password_entry.bind('<Return>', self.login)

        self.login_btn = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_btn.grid(row=2, column=0, columnspan=2)
        self.login_btn.bind('<Return>', self.login)

        self.register_btn = tk.Button(self.login_frame, text="Register", command=self.register)
        self.register_btn.grid(row=3, column=0, columnspan=2)
        self.register_btn.bind('<Return>', self.register)


    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = self.user_controller.login_user(username, password)
        if success:
            showMessage(message, type='success', timeout=2000)
            self.canvas.destroy()  # Destroy the login canvas
            self.to_do_app.show_main_window()
        else:
            showMessage(message, type='error')

    def register(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = self.user_controller.register_user(username, password)
        if success:
            showMessage(message, type='success', timeout=2000)
        else:
            showMessage(message, type='error')

    def entry_next(self, event):
        event.widget.tk_focusNext().focus()
        return("break")

def showMessage(message, type='info', timeout=30000):
    import tkinter as tk
    from tkinter import messagebox as msgb

    root = tk.Tk()
    root.withdraw()
    try:
        root.after(timeout, root.destroy)
        if type == 'info':
            msgb.showinfo('Info', message, master=root)
        elif type == 'success':
            msgb.showinfo('Success', message, master=root)
        elif type == 'warning':
            msgb.showwarning('Warning', message, master=root)
        elif type == 'error':
            msgb.showerror('Error', message, master=root)
    except Exception as e:
        print(e)

    if root is not None:
        try:
            root.destroy()
        except TclError as e:
            print(e)

        root = None
