from models.user_manager import UserManager

class UserController:
    def __init__(self):
        self.user_manager = UserManager()

    def register_user(self, username, password):
        return self.user_manager.register_user(username, password)

    def login_user(self, username, password):
        return self.user_manager.login_user(username, password)

    def get_current_user(self):
        return self.user_manager.get_current_user()
