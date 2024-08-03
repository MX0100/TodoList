# TodoList

Course Project

## Simplified Implementation
In Python, you can directly define a base class that includes the necessary methods, and the concrete strategy classes only need to implement these methods. This implementation is more concise and can fully meet the requirements in many cases.
## Dynamic Language Characteristics
Python is a dynamic language and does not enforce the use of abstract base classes to define interfaces. You can use duck typing to implement interfaces, meaning that as long as a class implements the required methods, it can be considered as implementing the interface.

## 设计模式

### 单例模式 (Singleton Pattern)
The TaskController class is designed using the Singleton pattern, ensuring that only one instance of this class exists throughout the application. This is achieved by overriding the __new__ method to check if an instance already exists and, if not, creating it. The class is responsible for managing tasks, including adding, updating, retrieving, and deleting tasks from the database. It interacts with the Database class and uses methods to handle tasks based on user input, ensuring consistent task management across the application.

**代码示例**:
```python
# class TaskController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TaskController, cls).__new__(cls, *args, **kwargs)
            cls._instance.db = Database()
        return cls._instance
```
The class is responsible for managing user operations, including registering, logging in, retrieving current user information, and handling user sessions. It interacts with the UserManager class and uses methods to handle user operations based on input, ensuring consistent user management across the application.
```python
# from models.user_manager import UserManager
class UserController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserController, cls).__new__(cls, *args, **kwargs)
            cls._instance.user_manager = UserManager()
            cls._instance.current_user = None
        return cls._instance

```
The UserManager class is designed using the Singleton pattern, ensuring that only one instance of this class exists throughout the application. This is achieved by overriding the __new__ method to check if an instance already exists and, if not, creating it. The class is responsible for user management tasks, such as registering and logging in users, and maintaining the current user's state.
```python
class UserManager:
    _instance = None
    def __init__(self):
        self.current_user = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
            cls._instance.current_user = None
            cls._instance.db = Database()
        return cls._instance
```
In Python, cls is a conventionally used parameter name in class methods that refer to the class itself. This is similar to how self refers to the instance of the class in instance methods. Here’s a brief explanation:

### 工厂模式 (Factory Pattern)
It initializes an SQLite database, creates necessary tables for users and tasks, and includes methods for adding, updating, retrieving, and deleting tasks and users. The class ensures security by using PBKDF2HMAC for password hashing and AES for encrypting task descriptions.

**代码示例**:
```python
class Database:
    def __init__(self, uri_or_path="todo_app.db"):
        self.connection = sqlite3.connect(uri_or_path)

        self.create_tables()
        self.observers = []

    def create_tables(self):
        with self.connection:
```
### 观察者模式 (Observer Pattern)
db.py also implements the observer pattern to notify registered observers of any changes in the database, ensuring consistent task management and real-time updates across the application.
```python
 def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()

``

```python
class Observer(ABC):
    @abstractmethod
    def update(self):
        pass
```
```python
# views/calendar_view.py
self.calendar.bind("<<CalendarSelected>>", self.show_tasks)
```
### 策略模式 (Strategy Pattern)
The Strategy Pattern is a behavioral design pattern that defines a family of algorithms, encapsulates each one, and makes them interchangeable. This pattern allows the algorithm to vary independently from its clients.

定义一系列算法，将每个算法封装起来，使它们可以相互替换。

**代码示例**:
```python
# models/user_manager.py
class RegistrationStrategy:
    def validate(self, db, username, password):
        raise NotImplementedError("You should implement this method.")

class EmptyFieldStrategy(RegistrationStrategy):
    def validate(self, db, username, password):
        if not username or not password:
            return False, "Username and password cannot be empty"
        return True, None

class UsernameExistsStrategy(RegistrationStrategy):
    def validate(self, db, username, password):
        if db.get_user_by_username(username):
            return False, "Username already exists"
        return True, None
```
### 模板方法模式 (Template Method Pattern)
1.	Abstract Class:
    •	Contains the template method which defines the algorithm’s structure.
	•	The template method consists of a series of method calls, some of which are implemented in the abstract class, and some are abstract (or hooks) meant to be implemented by subclasses.
2.	Concrete Classes:
	•	Implement the abstract methods (or hooks) defined in the abstract class.
	•	These implementations provide the specific behavior for the steps defined as abstract in the template method.

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
The auth_required decorator is designed to ensure that a user is authenticated before allowing access to certain methods. Here’s how it works:

    Decorator Definition: The auth_required function is defined as a decorator. It takes a function func as an argument.

    Wrapper Function: Inside auth_required, a wrapper function is defined. This wrapper function adds additional behavior before and after the original function func is called.

    Authentication Check:
        The wrapper function retrieves the current user ID by calling self.user_controller.get_current_user_id().
        If no user is logged in (user is None), a warning message is displayed using messagebox.showwarning, informing the user that they must be logged in to perform the action.
        If a user is logged in, the original function func is called with its arguments (*args and **kwargs).

    Using the Decorator: By applying the @auth_required decorator to a method, you ensure that this authentication check is performed every time the method is called.
```python
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
```
### MVC 模式 (Model-View-Controller Pattern)
1.	Model:
•	Represents the application’s data and business logic.
•	Notifies observers (typically the controller or view) of changes.
•	Directly manages the data, logic, and rules of the application.
2.	View:
•	Represents the UI (user interface) of the application.
•	Displays the data from the model to the user.
•	Sends user commands to the controller.
•	Observes the model and updates the display when the model changes.
3.	Controller:
•	Acts as an intermediary between Model and View.
•	Responds to user input from the View.
•	Updates the Model based on user actions.
•	May also update the View in response to model changes.

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



