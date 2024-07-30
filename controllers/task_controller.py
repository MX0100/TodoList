# controllers/task_controller.py
from db.database import Database
from datetime import datetime
from models.task import Task  # 确保 Task 类放在 models/task.py 文件中


class TaskController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TaskController, cls).__new__(cls, *args, **kwargs)
            cls._instance.db = Database()
        return cls._instance

    def add_task(self, description, user_id, start_date, end_date, repeat_value, password):
        self.db.add_task_with_dates(description, user_id, start_date, end_date, repeat_value, password)

    def update_task(self, task_id, new_description, password):
        self.db.update_task_with_description(task_id, new_description, password)

    def get_tasks(self, user_id, password):
        tasks_data = self.db.get_tasks(user_id, password)
        tasks = [self._create_task_from_data(task) for task in tasks_data]
        return tasks

    def get_tasks_by_date(self, user_id, date, password):
        tasks_data = self.db.get_tasks_by_date(user_id, date, password)
        filtered_tasks = []
        for task_data in tasks_data:
            task = self._create_task_from_data(task_data)
            if self._should_display_task(task, date):
                filtered_tasks.append(task)
        return filtered_tasks

    def delete_task(self, task_id):
        self.db.delete_task(task_id)

    def _create_task_from_data(self, task_data):
        return Task(
            task_id=task_data[0],
            description=task_data[1],
            timestamp=str(task_data[2]) if task_data[2] else None,
            start_date=str(task_data[3]) if task_data[3] else None,
            end_date=str(task_data[4]) if task_data[4] else None,
            repeat=task_data[5],
            completed=task_data[6],
            user_id=task_data[7]
        )

    def _should_display_task(self, task, date):
        if not task.get_start_date() or not task.get_end_date():
            return False

        start_date = datetime.strptime(task.get_start_date(), '%Y-%m-%d')
        end_date = datetime.strptime(task.get_end_date(), '%Y-%m-%d')
        current_date = datetime.strptime(date, '%Y-%m-%d')

        print(
            f"Checking task: {task.get_description()} (Start: {task.get_start_date()}, End: {task.get_end_date()}, Repeat: {task.get_repeat()}) for date: {date}")

        if task.get_repeat() == 0:  # None
            return start_date <= current_date <= end_date
        elif task.get_repeat() == 1:  # Daily
            return start_date <= current_date <= end_date
        elif task.get_repeat() == 2:  # Weekly
            delta = (current_date - start_date).days
            return start_date <= current_date <= end_date and delta % 7 == 0
        elif task.get_repeat() == 3:  # Monthly
            return start_date <= current_date <= end_date and start_date.day == current_date.day
        elif task.get_repeat() == 4:  # Yearly
            return start_date <= current_date <= end_date and start_date.month == current_date.month and start_date.day == current_date.day
        return False

    def get_general_tasks(self, user_id, password):
        tasks_data = self.db.get_general_tasks(user_id, password)
        tasks = [self._create_task_from_data(task) for task in tasks_data]
        return tasks

    def get_scheduled_tasks(self, user_id, password):
        tasks_data = self.db.get_scheduled_tasks(user_id, password)
        tasks = [self._create_task_from_data(task) for task in tasks_data]
        return tasks


    def toggle_task_completion(self, task_id, completed):
        self.db.toggle_task_completion(task_id, completed)


    def register_observer(self, observer):
        self.db.add_observer(observer)

    def unregister_observer(self, observer):
        self.db.remove_observer(observer)
