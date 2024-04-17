import tkinter as tk
from tkinter import simpledialog, messagebox
from task_manager import TaskManager

class TaskPlannerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskPlanner Application Dashboard")
        self.setup_dashboard()

    def setup_dashboard(self):
        #Creates a main frame to hold dashboard widgets
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        #Planner Button
        self.planner_button = tk.Button(self.main_frame, text="Planner", command=self.open_planner)
        self.planner_button.pack(fill=tk.X, padx=5, pady=2)

        #Placeholder buttons
        self.other_widget_button_1 = tk.Button(self.main_frame, text="Other Widget 1", command=self.open_other_widget_1)
        self.other_widget_button_1.pack(fill=tk.X, padx=5, pady=2)

        self.other_widget_button_2 = tk.Button(self.main_frame, text="Other Widget 2", command=self.open_other_widget_2)
        self.other_widget_button_2.pack(fill=tk.X, padx=5, pady=2)


    def open_planner(self):
        #Logic to open the TaskPlanner widget
        planner_win = tk.Toplevel(self.root)
        planner_win.title("Task Planner")
        task_manager = TaskManager()
        planner_ui = PlannerWidget(planner_win, task_manager)
        planner_ui.setup_ui()


    def open_other_widget_1(self):
        #Logic to open Other Widget 1
        print("Opening Other Widget 1...")

    def open_other_widget_2(self):
        #Logic to open Other Widget 2
        print("Opening Other Widget 2...")

class PlannerWidget:
    def __init__(self, root, task_manager):
        self.root = root
        self.task_manager = task_manager
        self.root.title("Task Planner")
        self.setup_ui()

    def setup_ui(self):
        #Task List
        label = tk.Label(self.root, text="Task Planner window")
        label.pack()
        self.task_listbox = tk.Listbox(self.root, width=50, height=15)
        self.task_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        #Scrollbar for Task List
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.task_listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill='y')
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        #Button Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        #Add Task Button
        self.add_button = tk.Button(button_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(fill=tk.X, padx=5, pady=2)

        #Delete Task Button
        self.delete_button = tk.Button(button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(fill=tk.X, padx=5, pady=2)

        #Update Task Button
        self.update_button = tk.Button(button_frame, text="Update Task", command=self.update_task)
        self.update_button.pack(fill=tk.X, padx=5, pady=2)

        #Refresh Task List at UI initialization
        self.refresh_task_list()

    def add_task(self):
        description = simpledialog.askstring("Add Task", "Task Description:")
        if description:
            self.task_manager.add_task(description)
            self.refresh_task_list()

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.task_manager.delete_task(selected_index)
            self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def update_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            new_description = simpledialog.askstring("Update Task", "New Task Description:")
            if new_description:
                self.task_manager.update_task(selected_index, new_description)
                self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to update.")

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.get_tasks():
            self.task_listbox.insert(tk.END, task['description'])

if __name__ == "__main__":
    root = tk.Tk()
    app_ui = TaskPlannerUI(root)
    root.mainloop()

