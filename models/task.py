from datetime import datetime

class Task:
    def __init__(self, task_id, description, timestamp, start_date, end_date, repeat, completed, user_id):
        self.task_id = task_id
        self.description = description
        self.timestamp = timestamp
        self.start_date = start_date
        self.end_date = end_date
        self.repeat = repeat
        self.completed = completed
        self.user_id = user_id

    def get_task_id(self):
        return self.task_id

    def get_description(self):
        return self.description

    def get_timestamp(self):
        return self.timestamp

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_repeat(self):
        return self.repeat

    def is_completed(self):
        return self.completed

    def get_user_id(self):
        return self.user_id
