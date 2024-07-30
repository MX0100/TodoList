from models.user_manager import UserManager


class UserController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserController, cls).__new__(cls, *args, **kwargs)
            cls._instance.user_manager = UserManager()
            cls._instance.current_user = None
        return cls._instance

    def register_user(self, username, password):
        return self.user_manager.register_user(username, password)

    def login_user(self, username, password):
        if not username or not password:
            return False, "Username and password cannot be empty"

        self.current_user = self.user_manager.login_user(username, password)
        if self.current_user:
            return True, "Login successful"
        else:
            return False, "Invalid username or password"

    def get_current_user(self):
        return self.current_user

    def get_current_user_id(self):
        return self.current_user['id']

    def get_current_user_password(self):
        return self.current_user['password']
