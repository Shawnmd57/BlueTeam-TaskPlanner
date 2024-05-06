import datetime
from threading import Thread
import time
import tkinter as tk
from tkinter import messagebox

class NotificationManager:
    def __init__(self, task_manager, root):
        self.task_manager = task_manager
        self.root = root
        self.check_interval = 30  #checks every 30 seconds

    def start_notification_service(self):
        notification_thread = Thread(target=self.run_notification_check, daemon=True)
        notification_thread.start()

    def _get_time_now(self):
        return datetime.datetime.now().replace(second=0, microsecond=0)  #Removes seconds/microseconds for matching
    
    def run_notification_check(self):
        while True:
            current_time = self._get_time_now()
            tasks = self.task_manager.get_tasks()
            for task in tasks:
                task_time = self._parse_datetime(task['due_date'])
                if task_time and task_time == current_time and not task['completed']:
                    self._notify(task)
            time.sleep(self.check_interval)

    def _parse_datetime(self, datetime_str):
        if datetime_str is None:
            return None
        #Trys different formats
        date_formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %I:%M %p']
        for fmt in date_formats:
            try:
                return datetime.datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue  #Trys next format
        #If no format succeeds
        print(f"Warning: Failed to parse date '{datetime_str}'")
        return None

    def _notify(self, task):
        #Ensures notifications appear on main thread
        tk.messagebox.showwarning("Reminder", f"Reminder! It's time for: {task['description']}", master=self.root)

    def complete_task(self, task_id):
        self.task_manager.complete_task(task_id)