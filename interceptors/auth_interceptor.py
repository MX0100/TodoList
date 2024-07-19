from functools import wraps
from models.user_manager import UserManager
from tkinter import messagebox

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_manager = UserManager()
        if user_manager.get_current_user() is None:
            messagebox.showwarning("Warning", "You must be logged in to perform this action")
            return
        return func(*args, **kwargs)
    return wrapper
