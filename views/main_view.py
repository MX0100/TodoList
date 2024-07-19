import tkinter as tk
from tkinter import messagebox
from controllers.task_controller import TaskController
from controllers.user_controller import UserController
from views.login_register_view import LoginRegisterWindow
from interceptors.auth_interceptor import auth_required


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.user_controller = UserController()
        self.task_controller = TaskController()
        self.login_register_window = LoginRegisterWindow(root, self)
        self.tasks = []
        self.calendar_window = None  # 初始化 calendar_window 属性

    def show_main_window(self):
        from views.calendar_view import CalendarWindow  # 延迟导入以避免循环依赖
        self.calendar_window = CalendarWindow(self.root)

        self.login_register_window.login_frame.pack_forget()
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.task_entry = tk.Entry(self.frame, width=50)
        self.task_entry.grid(row=0, column=0)

        self.add_task_btn = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_task_btn.grid(row=0, column=1)

        self.show_calendar_btn = tk.Button(self.frame, text="Show Calendar", command=self.calendar_window.show_calendar)
        self.show_calendar_btn.grid(row=0, column=2)

        self.tasks_frame = tk.Frame(self.root)
        self.tasks_frame.pack(pady=10)

        self.load_tasks()

    @auth_required
    def add_task(self):
        task_description = self.task_entry.get()
        if task_description:
            current_user = self.user_controller.get_current_user()
            self.task_controller.add_task(task_description, current_user)
            self.task_entry.delete(0, tk.END)
            self.load_tasks()
        else:
            messagebox.showwarning("Warning", "Task description cannot be empty")

    def load_tasks(self):
        current_user = self.user_controller.get_current_user()
        self.tasks = self.task_controller.get_tasks(current_user)
        self.update_tasks()

    def update_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        for index, task in enumerate(self.tasks):
            task_frame = tk.Frame(self.tasks_frame)
            task_frame.pack(fill="x")

            task_check = tk.Checkbutton(task_frame, text=task[1], variable=tk.IntVar())
            task_check.pack(side="left")

            delete_btn = tk.Button(task_frame, text="Delete", command=lambda task_id=task[0]: self.delete_task(task_id))
            delete_btn.pack(side="right")

    def delete_task(self, task_id):
        self.task_controller.delete_task(task_id)
        self.load_tasks()
