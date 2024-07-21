from functools import wraps
from models.user_manager import UserManager
from tkinter import messagebox


def auth_required(func):
    @wraps(func)
    def wrapper(self,*args, **kwargs):
        user = self.user_controller.get_current_user_id()
        if user is None:
            messagebox.showwarning("Warning", "You must be logged in to perform this action")
            return
        return func(self,*args, **kwargs)

    return wrapper
