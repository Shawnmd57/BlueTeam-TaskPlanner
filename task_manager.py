import json
from contextlib import contextmanager
import datetime
import os

class TaskManager:
    def __init__(self):
        self.json_file_path = 'tasks.json'
        self.ensure_data_file()

    def ensure_data_file(self):
        """Ensure the JSON file exists and is properly initialized."""
        if not os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'w') as file:
                json.dump({'tasks': []}, file)
    
    def read_tasks(self):
        with open(self.json_file_path, 'r') as file:
            return json.load(file)['tasks']

    def write_tasks(self, tasks):
        with open(self.json_file_path, 'w') as file:
            json.dump({'tasks': tasks}, file)
    
    def get_tasks(self):
        """Retrieve all tasks from the JSON data file."""
        return self.read_tasks()

    def add_task(self, description, notes, due_date):
        tasks = self.read_tasks()
        new_id = 1
        if tasks:
            new_id = max(task['id'] for task in tasks) + 1
        tasks.append({
            'id': new_id,
            'description': description,
            'due_date': due_date,
            'notes': notes,
            'completed': False
        })
        self.write_tasks(tasks)
        print(f"Task added: {description} on {due_date} with notes {notes}")

    def delete_task(self, task_id):
        tasks = self.read_tasks()
        tasks = [task for task in tasks if task['id'] != task_id]
        self.write_tasks(tasks)

    def update_task(self, task_id, **kwargs):
        tasks = self.read_tasks()
        updated = False
        for task in tasks:
            if task['id'] == task_id:
                for key, value in kwargs.items():
                    task[key] = value
                updated = True
        self.write_tasks(tasks)
        if updated:
            print("Task updated:", task_id)
        else:
            print("Task not found:", task_id)


    def complete_task(self, task_id):
        self.update_task(task_id, completed=True)