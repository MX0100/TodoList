import tkinter as _tk
from tkinter import ttk as tk
from tkinter import messagebox
from controllers.task_controller import TaskController
from controllers.user_controller import UserController
from views.login_register_view import LoginRegisterWindow
from interceptors.auth_interceptor import auth_required
import sys

OS = sys.platform


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.user_controller = UserController()
        self.task_controller = TaskController()
        self.login_register_window = LoginRegisterWindow(root, self, self.user_controller)
        self.tasks = []
        self.scheduled_tasks = []
        self.calendar_window = None

    def show_main_window(self):
        from views.calendar_view import CalendarWindow  # 延迟导入以避免循环依赖
        self.calendar_window = CalendarWindow(self.root, self.user_controller, self.task_controller, self)

        self.login_register_window.login_frame.pack_forget()
        self.frame = _tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.task_entry = _tk.Entry(self.frame, width=50)
        self.task_entry.grid(row=0, column=0)
        self.task_entry.bind('<Return>', self.add_task)

        self.add_task_btn = _tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_task_btn.grid(row=0, column=1)

        self.show_calendar_btn = _tk.Button(self.frame, text="Show Calendar", command=self.calendar_window.show_calendar)
        self.show_calendar_btn.grid(row=0, column=2)

        self.main_frame = _tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # General tasks frame
        self.general_tasks_frame = _tk.Frame(self.main_frame)
        self.general_tasks_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.general_tasks_label = _tk.Label(self.general_tasks_frame, text="General Tasks")
        self.general_tasks_label.pack()

        self.general_tasks_canvas = _tk.Canvas(self.general_tasks_frame, highlightthickness=0)
        self.general_tasks_canvas.pack(side="left", fill="both", expand=True)

        self.general_tasks_scrollbar = tk.Scrollbar(self.general_tasks_frame, orient="vertical", command=self.general_tasks_canvas.yview)
        self.general_tasks_canvas.configure(yscrollcommand=self.general_tasks_scrollbar.set)
        self.general_tasks_scrollbar.pack(side="right", fill="y")

        self.general_tasks_inner_frame = _tk.Frame(self.general_tasks_canvas)
        self.general_tasks_canvas.create_window((0, 0), window=self.general_tasks_inner_frame, anchor="nw")
        self.general_tasks_inner_frame.bind(
            "<Configure>",
            lambda e: self.general_tasks_canvas.configure(scrollregion=self.general_tasks_canvas.bbox("all"))
        )

        if OS in ('win32', 'darwin'):
            # https://apple.stackexchange.com/q/392936
            self.general_tasks_canvas.bind('<MouseWheel>', self._on_mouse_wheel_general)
        if OS == 'linux':
            # https://stackoverflow.com/a/17452217/13629335
            self.general_tasks_canvas.bind('<Button-4>', self._on_mouse_wheel_general)
            self.general_tasks_canvas.bind('<Button-5>', self._on_mouse_wheel_general)

        # Separator
        self.separator = _tk.ttk.Separator(self.main_frame, orient='vertical')
        self.separator.pack(side="left", fill="y", padx=5)

        # Scheduled tasks frame
        self.scheduled_tasks_frame = _tk.Frame(self.main_frame)
        self.scheduled_tasks_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.scheduled_tasks_label = _tk.Label(self.scheduled_tasks_frame, text="Scheduled Tasks")
        self.scheduled_tasks_label.pack()

        self.scheduled_tasks_canvas = _tk.Canvas(self.scheduled_tasks_frame, highlightthickness=0)
        self.scheduled_tasks_canvas.pack(side="left", fill="both", expand=True)

        self.scheduled_tasks_scrollbar = _tk.Scrollbar(self.scheduled_tasks_frame, orient="vertical", command=self.scheduled_tasks_canvas.yview)
        self.scheduled_tasks_canvas.configure(yscrollcommand=self.scheduled_tasks_scrollbar.set)
        self.scheduled_tasks_scrollbar.pack(side="right", fill="y")

        self.scheduled_tasks_inner_frame = _tk.Frame(self.scheduled_tasks_canvas)
        self.scheduled_tasks_canvas.create_window((0, 0), window=self.scheduled_tasks_inner_frame, anchor="nw")
        self.scheduled_tasks_inner_frame.bind(
            "<Configure>",
            lambda e: self.scheduled_tasks_canvas.configure(scrollregion=self.scheduled_tasks_canvas.bbox("all"))
        )

        if OS in ('win32', 'darwin'):
            # https://apple.stackexchange.com/q/392936
            self.scheduled_tasks_canvas.bind('<MouseWheel>', self._on_mouse_wheel_scheduled)
        if OS == 'linux':
            # https://stackoverflow.com/a/17452217/13629335
            self.scheduled_tasks_canvas.bind('<Button-4>', self._on_mouse_wheel_scheduled)
            self.scheduled_tasks_canvas.bind('<Button-5>', self._on_mouse_wheel_scheduled)

        self.load_tasks()

    def _on_mouse_wheel_general(self, event):
        self.general_tasks_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mouse_wheel_scheduled(self, event):
        self.scheduled_tasks_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    @auth_required
    def add_task(self):
        task_description = self.task_entry.get()
        if task_description.strip():
            current_user_id = self.user_controller.get_current_user_id()
            self.task_controller.add_task(task_description, current_user_id, None, None, 0)
            self.task_entry.delete(0, _tk.END)
            self.load_tasks()
        else:
            messagebox.showwarning("Warning", "Task description cannot be empty")

    def load_tasks(self):
        current_user_id = self.user_controller.get_current_user_id()
        self.tasks = self.task_controller.get_general_tasks(current_user_id)
        self.scheduled_tasks = self.task_controller.get_scheduled_tasks(current_user_id)
        self.update_tasks()

    def update_tasks(self):
        self.update_general_tasks()
        self.update_scheduled_tasks()

    def update_general_tasks(self):
        for widget in self.general_tasks_inner_frame.winfo_children():
            widget.destroy()

        for task in self.tasks:
            task_frame = _tk.Frame(self.general_tasks_inner_frame)
            task_frame.pack(fill="x")

            task_var = _tk.IntVar(value=task.is_completed())
            task_check = _tk.Checkbutton(task_frame, variable=task_var, command=lambda task_id=task.get_task_id(), var=task_var: self.toggle_task_completion(task_id, var.get()))
            task_check.pack(side="left")

            task_entry = _tk.Entry(task_frame, width=20, bg='#ebebeb', borderwidth = 0, highlightthickness=0)
            task_entry.insert(0, task.get_description())
            task_entry.bind("<Return>", lambda event, task_id=task.get_task_id(), entry=task_entry: self.update_task(task_id, entry.get()))
            task_entry.pack(side="left", fill="x", expand=True)

            delete_btn = tk.Button(task_frame, text="Delete", command=lambda task_id=task.get_task_id(): self.delete_task(task_id))
            delete_btn.pack(side="right")

    def update_scheduled_tasks(self):
        for widget in self.scheduled_tasks_inner_frame.winfo_children():
            widget.destroy()

        for task in self.scheduled_tasks:
            task_frame = _tk.Frame(self.scheduled_tasks_inner_frame)
            task_frame.pack(fill="x")

            task_var = _tk.IntVar(value=task.is_completed())
            task_check = _tk.Checkbutton(task_frame, variable=task_var, command=lambda task_id=task.get_task_id(), var=task_var: self.toggle_task_completion(task_id, var.get()))
            task_check.pack(side="left")

            task_text = f"{task.get_start_date()} {task.get_description()}"
            task_entry = _tk.Entry(task_frame, width=20, bg='#ebebeb', borderwidth = 0, highlightthickness=0)
            task_entry.insert(0, task_text)
            task_entry.bind("<Return>", lambda event, task_id=task.get_task_id(), entry=task_entry: self.update_task(task_id, entry.get()))
            task_entry.pack(side="left", fill="x", expand=True)

            delete_btn = tk.Button(task_frame, text="Delete", command=lambda task_id=task.get_task_id(): self.delete_task(task_id))
            delete_btn.pack(side="right")

    def update_task(self, task_id, new_description):
        self.task_controller.update_task(task_id, new_description)
        self.load_tasks()

    def toggle_task_completion(self, task_id, completed):
        self.task_controller.toggle_task_completion(task_id, completed)
        self.load_tasks()

    def delete_task(self, task_id):
        self.task_controller.delete_task(task_id)
        self.load_tasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
