单例模式 (Singleton Pattern)
class UserManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
            cls._instance.users = {}
            cls._instance.current_user = None
            cls._instance.db = Database()
        return cls._instance
工厂模式 (Factory Pattern)
class Database:
    def __init__(self, db_name="todo_app.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()
命令模式 (Command Pattern)
add_task_btn = tk.Button(self.frame, text="Add Task", command=self.add_task)
观察者模式 (Observer Pattern
self.calendar.bind("<<CalendarSelected>>", self.show_tasks)
策略模式 (Strategy Pattern)
def register_user(self, username, password):
    if not username or not password:
        return False, "Username and password cannot be empty"
    if self.db.get_user_by_username(username):
        return False, "Username already exists"
    self.db.add_user(username, password)
    return True, "User registered successfully"
模板方法模式 (Template Method Pattern)
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
                repeat TEXT,
                completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)),
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
    装饰器模式 (Decorator Pattern)
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
MVC 模式 (Model-View-Controller Pattern)
描述: 模型-视图-控制器模式将应用程序分为三个主要部分：模型、视图和控制器。
实现: 我们的项目结构包含模型（models 文件夹）、视图（views 文件夹）和控制器（controllers 文件夹）。
代码示例:
模型: Database 类和 UserManager 类
视图: LoginRegisterWindow 和 CalendarWindow
控制器: TaskController 和 UserController
