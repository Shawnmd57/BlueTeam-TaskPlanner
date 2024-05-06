import tkinter as tk
from ui import TaskPlannerUI
from task_manager import TaskManager
from notification_manager import NotificationManager

def main():
    #Creates main window
    root = tk.Tk()
    root.title("Task Planner")

    #Initializes task manager
    task_manager = TaskManager()

    #Initializes / starts notification manager
    notification_manager = NotificationManager(task_manager, root)
    notification_manager.start_notification_service()

    #Creates/shows UI
    app_ui = TaskPlannerUI(root, task_manager)
    
    #Starts Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()