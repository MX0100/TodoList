

class User:
    def __repr__(self):
        return f"<User(username={self.username})>"

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
