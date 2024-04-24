import tkinter as tk
from ui import TaskPlannerUI
from task_manager import TaskManager
from notification_manager import NotificationManager

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Task Planner")

    # Initialize the task manager
    task_manager = TaskManager()

    # Initialize and start the notification manager
    notification_manager = NotificationManager(task_manager, root)
    notification_manager.start_notification_service()

    # Create and show the UI
    app_ui = TaskPlannerUI(root, task_manager)
    
    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()