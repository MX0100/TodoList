from models.user_manager import UserManager


class UserController:
    def __init__(self):
        self.user_manager=UserManager()
        print(id(self.user_manager))
        self.current_user=None

    def register_user(self, username, password):
        return self.user_manager.register_user(username, password)

    def login_user(self, username, password):
        self.current_user = self.user_manager.login_user(username, password)
        if self.current_user:
            return True, "Login successful"
        return False, "Invalid username or password"

    def get_current_user(self):
        return self.current_user

    def get_current_user_id(self):
        return self.current_user['id']
