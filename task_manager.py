import json
from contextlib import contextmanager
import datetime
import os

class TaskManager:
    def __init__(self):
        # Set the path to the JSON file
        self.json_file_path = 'tasks.json'
        # Ensure that the data file exists and is properly initialized
        self.ensure_data_file()

    def ensure_data_file(self):
        """Ensure the JSON file exists and is properly initialized."""
        # If the JSON file doesn't exist, create it and initialize it with an empty list of tasks
        if not os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'w') as file:
                json.dump({'tasks': []}, file)
    
    def read_tasks(self):
        # Read the tasks from the JSON file and return them
        with open(self.json_file_path, 'r') as file:
            return json.load(file)['tasks']

    def write_tasks(self, tasks):
        # Write the tasks to the JSON file
        with open(self.json_file_path, 'w') as file:
            json.dump({'tasks': tasks}, file)
    
    def get_tasks(self):
        """Retrieve all tasks from the JSON data file."""
        # Return all tasks from the JSON file
        return self.read_tasks()

    def add_task(self, description, notes, due_date):
        # Read the existing tasks from the JSON file
        tasks = self.read_tasks()
        # Generate a new ID for the task
        new_id = 1
        if tasks:
            new_id = max(task['id'] for task in tasks) + 1
        # Create a new task with the provided information
        new_task = {
            'id': new_id,
            'description': description,
            'due_date': due_date,
            'notes': notes,
            'completed': False
        }
        # Add the new task to the list of tasks
        tasks.append(new_task)
        # Write the updated list of tasks to the JSON file
        self.write_tasks(tasks)
        # Print a message confirming that the task has been added
        print(f"Task added: {description} on {due_date} with notes {notes}")

    def delete_task(self, task_id):
        # Read the existing tasks from the JSON file
        tasks = self.read_tasks()
        # Remove the task with the specified ID from the list of tasks
        tasks = [task for task in tasks if task['id'] != task_id]
        # Write the updated list of tasks to the JSON file
        self.write_tasks(tasks)

    def update_task(self, task_id, **kwargs):
        # Read the existing tasks from the JSON file
        tasks = self.read_tasks()
        updated = False
        for task in tasks:
            if task['id'] == task_id:
                # Update the specified task with the provided key-value pairs
                for key, value in kwargs.items():
                    task[key] = value
                updated = True
        # Write the updated list of tasks to the JSON file
        self.write_tasks(tasks)
        if updated:
            # Print a message confirming that the task has been updated
            print("Task updated:", task_id)
        else:
            # Print a message indicating that the task was not found
            print("Task not found:", task_id)

    def complete_task(self, task_id):
        # Mark the task with the specified ID as completed
        self.update_task(task_id, completed=True)