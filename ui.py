import tkinter as tk
from tkinter import simpledialog
from task_manager import TaskManager

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.task_manager = TaskManager()
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        self.add_task_button = tk.Button(self.main_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack()

        self.list_tasks_button = tk.Button(self.main_frame, text="List Tasks", command=self.list_tasks)
        self.list_tasks_button.pack()

    def add_task(self):
        task_name = simpledialog.askstring("Input", "What is the task?")
        if task_name:
            self.task_manager.add_task(task_name)

    def list_tasks(self):
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            tk.Label(self.main_frame, text=task).pack()

def main():
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()