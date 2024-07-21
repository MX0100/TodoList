import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import datetime
class CalendarWindow:
    def __init__(self, root,user_controller,task_controller):
        self.root = root
        self.task_controller = task_controller
        self.user_controller = user_controller

    def show_calendar(self):
        self.calendar_window = tk.Toplevel(self.root)
        self.calendar_window.title("Calendar")
        self.calendar_window.geometry("800x600")

        self.calendar = Calendar(self.calendar_window, selectmode='day', year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        self.calendar.pack(pady=20, fill="both", expand=True)

        self.calendar.bind("<<CalendarSelected>>", self.show_tasks)

        self.task_listbox = tk.Listbox(self.calendar_window)
        self.task_listbox.pack(pady=10, fill="both", expand=True)

        add_task_btn = tk.Button(self.calendar_window, text="Add Task", command=self.open_add_task_dialog)
        add_task_btn.pack(pady=20, anchor="ne")

        close_btn = tk.Button(self.calendar_window, text="Close", command=self.calendar_window.destroy)
        close_btn.pack(pady=20)

        # 加载当天的任务
        self.show_tasks()

    def show_tasks(self, event=None):
        selected_date = self.calendar.get_date()
        selected_date=datetime.datetime.strptime(selected_date, "%m/%d/%y").strftime("%Y-%m-%d") #转化
        print(selected_date)
        current_user_id = self.user_controller.get_current_user_id()
        tasks = self.task_controller.get_tasks_by_date(current_user_id, selected_date)

        self.task_listbox.delete(0, tk.END)
        for task in tasks:
            self.task_listbox.insert(tk.END, f"{task.get_description()} (Start: {task.get_start_date()}, End: {task.get_end_date()})")

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

        # 将 repeat 字符值转换为整数值
        repeat_value = {"None": 0, "Daily": 1, "Weekly": 2, "Monthly": 3, "Yearly": 4}.get(repeat, 0)

        if task_description:
            current_user_id = self.user_controller.get_current_user_id()
            self.task_controller.add_task(task_description, current_user_id, start_date, end_date, repeat_value)
            self.add_task_dialog.destroy()
            self.show_tasks()  # Refresh tasks
        else:
            messagebox.showwarning("Warning", "Task description cannot be empty")

