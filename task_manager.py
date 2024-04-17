class TaskManager:
    def __init__(self):
        # Initialize task list
        self.tasks = []

    def add_task(self, description):
        task = {"description": description, "completed": False}
        self.tasks.append(task)

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def update_task(self, index, description):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["description"] = description

    def toggle_task_completion(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]

    def get_tasks(self):
        return self.tasks