class TaskManager:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks
    
    # For simplicity, an in-memory list is being used to store tasks. 
    # We can replace this with a database if need be.