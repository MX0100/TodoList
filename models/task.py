from datetime import datetime

class Task:
    def __init__(self, description):
        self.description = description
        self.timestamp = datetime.now()
        self.completed = False
