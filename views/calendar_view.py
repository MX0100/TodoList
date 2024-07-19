import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
from datetime import datetime
from controllers.task_controller import TaskController
from controllers.user_controller import UserController

class CalendarWindow:
    def __init__(self, root):
        self.root = root
        self.task_controller = TaskController()
        self.user_controller = UserController()

    def show_calendar(self):
        self.calendar_window = tk.Toplevel(self.root)
        self.calendar_window.title("Calendar")
        self.calendar_window.geometry("800x600")

        self.calendar = Calendar(self.calendar_window, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.pack(pady=20, fill="both", expand=True)

        self.calendar.bind("<<CalendarSelected>>", self.show_tasks)

        self.task_listbox = tk.Listbox(self.calendar_window)
        self.task_listbox.pack(pady=10, fill="both", expand=True)

        add_task_btn = tk.Button(self.calendar_window, text="Add Task", command=self.open_add_task_dialog)
        add_task_btn.pack(pady=20, anchor="ne")

        close_btn = tk.Button(self.calendar_window, text="Close", command=self.calendar_window.destroy)
        close_btn.pack(pady=20)

        # 加载当天的任务
        self.show_tasks(None)

    def show_tasks(self, event):
        selected_date = self.calendar.get_date()
        current_user = self.user_controller.get_current_user()
        tasks = self.task_controller.get_tasks_by_date(current_user, selected_date)

        self.task_listbox.delete(0, tk.END)
        for task in tasks:
            self.task_listbox.insert(tk.END, f"{task[1]} (Start: {task[3]}, End: {task[4]})")

    def open_add_task_dialog(self):
        self.add_task_dialog = tk.Toplevel(self.calendar_window)
        self.add_task_dialog.title("Add Task")
        self.add_task_dialog.geometry("400x400")

        tk.Label(self.add_task_dialog, text="Task Description:").pack(pady=5)
        self.task_description_entry = tk.Entry(self.add_task_dialog, width=50)
        self.task_description_entry.pack(pady=5)

        tk.Label(self.add_task_dialog, text="Start Date:").pack(pady=5)
        self.start_date_entry = DateEntry(self.add_task_dialog)
        self.start_date_entry.pack(pady=5)

        tk.Label(self.add_task_dialog, text="End Date:").pack(pady=5)
        self.end_date_entry = DateEntry(self.add_task_dialog)
        self.end_date_entry.pack(pady=5)

        tk.Label(self.add_task_dialog, text="Repeat:").pack(pady=5)
        self.repeat_combobox = ttk.Combobox(self.add_task_dialog, values=["None", "Daily", "Weekly", "Monthly", "Yearly"])
        self.repeat_combobox.pack(pady=5)

        save_btn = tk.Button(self.add_task_dialog, text="Save", command=self.save_task)
        save_btn.pack(pady=20)

        close_btn = tk.Button(self.add_task_dialog, text="Close", command=self.add_task_dialog.destroy)
        close_btn.pack(pady=20)

    def save_task(self):
        task_description = self.task_description_entry.get()
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        repeat = self.repeat_combobox.get()

        if task_description:
            current_user = self.user_controller.get_current_user()
            self.task_controller.add_task(task_description, current_user, start_date, end_date, repeat)
            self.add_task_dialog.destroy()
            self.show_tasks(None)  # Refresh tasks
        else:
            messagebox.showwarning("Warning", "Task description cannot be empty")
