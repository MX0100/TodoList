from models.user_manager import UserManager

class TaskController:
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
