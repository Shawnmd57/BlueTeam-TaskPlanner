import tkinter as tk
from ui import TaskPlannerUI
from task_manager import TaskManager
from notification_manager import NotificationManager

def main():
    root = tk.Tk()
    app_ui = TaskPlannerUI(root)
    task_manager = TaskManager() 
    notification_manager = NotificationManager(task_manager) 
    notification_manager.start_notification_service()
    
    root.mainloop()

if __name__ == "__main__":
    main()