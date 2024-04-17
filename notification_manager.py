import datetime
from threading import Thread
import time

class NotificationManager:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.check_interval = 60  # Check every 60 seconds

    def start_notification_service(self):
        notification_thread = Thread(target=self._run_notification_check, daemon=True)
        notification_thread.start()

    def _run_notification_check(self):
        while True:
            self._check_for_upcoming_deadlines()
            time.sleep(self.check_interval)

    def _check_for_upcoming_deadlines(self):
        now = datetime.datetime.now()
        for task in self.task_manager.get_tasks():
            if 'due_date' in task and isinstance(task['due_date'], datetime.datetime):
                time_until_deadline = task['due_date'] - now
                # Check if a deadline is within the next 24 hours but not past
                if 0 < time_until_deadline.total_seconds() <= 86400:  # 86400 seconds = 24 hours
                    self._notify(task)

    def _notify(self, task):
        print(f"Reminder! The task '{task['description']}' is nearing its deadline.")