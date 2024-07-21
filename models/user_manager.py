from db.database import Database


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

    def register_user(self, username, password):
        if not username or not password:
            return False, "Username and password cannot be empty"
        if self.db.get_user_by_username(username):
            return False, "Username already exists"
        self.db.add_user(username, password)
        return True, "User registered successfully"

    def login_user(self, username, password):
        user = self.db.get_user(username, password)
        if user:
            self.current_user = {
                "id": user[0],
                "username": user[1],
                "password": user[2]  # 如果需要，可以包括密码
            }
            return self.current_user

    def get_current_user_id(self):
        if self.current_user:
            return self.current_user["id"]
        return None

    def get_current_user(self):
        return self.current_user
