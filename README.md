# TodoList

Course Project

## 设计模式

### 单例模式 (Singleton Pattern)
确保一个类只有一个实例，并提供全局访问点。

**代码示例**:
```python
# models/user_manager.py
class UserManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
            cls._instance.users = {}
            cls._instance.current_user = None
            cls._instance.db = Database()
        return cls._instance
```

### 工厂模式 (Factory Pattern)
提供一个创建对象的接口，而无需指定具体类。

**代码示例**:
```python
# db/database.py
class Database:
    def __init__(self, db_name="todo_app.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()
```
### 命令模式 (Command Pattern)
将请求封装为对象，从而使我们可用不同的请求对客户进行参数化。

**代码示例**:
```python
# views/main_view.py
self.add_task_btn = tk.Button(self.frame, text="Add Task", command=self.add_task)
```
### 观察者模式 (Observer Pattern)
定义对象间的一对多依赖，当一个对象改变状态时，所有依赖对象都会收到通知并自动更新。

**代码示例**:
```python
# views/calendar_view.py
self.calendar.bind("<<CalendarSelected>>", self.show_tasks)
```
### 策略模式 (Strategy Pattern)
定义一系列算法，将每个算法封装起来，使它们可以相互替换。

**代码示例**:
```python
# models/user_manager.py
def register_user(self, username, password):
    if not username or not password:
        return False, "Username and password cannot be empty"
    if self.db.get_user_by_username(username):
        return False, "Username already exists"
    self.db.add_user(username, password)
    return True, "User registered successfully"
```
### 模板方法模式 (Template Method Pattern)
定义一个操作中的算法骨架，将一些步骤延迟到子类中。

**代码示例**:
```python
# db/database.py
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
```
### 装饰器模式 (Decorator Pattern)
动态地将责任附加到对象上，装饰器提供了比子类更灵活的扩展功能。

**代码示例**:
```python
# interceptors/auth_interceptor.py
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
```
### MVC 模式 (Model-View-Controller Pattern)
模型-视图-控制器模式将应用程序分为三个主要部分：模型、视图和控制器。

**代码示例**:
```python
# controllers/task_controller_interface.py
from abc import ABC, abstractmethod

class TaskControllerInterface(ABC):
    @abstractmethod
    def add_task(self, description, user_id, start_date=None, end_date=None, repeat=None):
        pass

    @abstractmethod
    def get_tasks(self, user_id):
        pass

    @abstractmethod
    def get_tasks_by_date(self, user_id, date):
        pass

    @abstractmethod
    def delete_task(self, task_id):
        pass
```
```python
# controllers/task_controller.py
from models.user_manager import UserManager
from controllers.task_controller_interface import TaskControllerInterface

class TaskController(TaskControllerInterface):
    def __init__(self):
        self.user_manager = UserManager()

    def add_task(self, description, user_id, start_date=None, end_date=None, repeat=None):
        if start_date and end_date:
            self.user_manager.db.add_task_with_dates(description, user_id, start_date, end_date, repeat)
        else:
            self.user_manager.db.add_task(description, user_id)

    def get_tasks(self, user_id):
        return self.user_manager.db.get_tasks(user_id)

    def get_tasks_by_date(self, user_id, date):
        return self.user_manager.db.get_tasks_by_date(user_id, date)

    def delete_task(self, task_id):
        self.user_manager.db.delete_task(task_id)
```



