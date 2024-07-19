from db.database import Database

class UserManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
            cls._instance.users = {}  # 使用字典保存用户信息
            cls._instance.current_user = None
            cls._instance.db = Database()
        return cls._instance

    def register_user(self, username, password):
        if not username or not password:
            return False, "Username and password cannot be empty"
        if self.db.get_user_by_username(username):
            return False, "Username already exists"
        self.db.add_user(username, password)
        return True, "User registered successfully"

    def login_user(self, username, password):
        if not username or not password:
            return False, "Username and password cannot be empty"
        user = self.db.get_user(username, password)
        if user:
            self.current_user = user[0]
            return True, "Login successful"
        return False, "Invalid username or password"

    def get_current_user(self):
        return self.current_user
