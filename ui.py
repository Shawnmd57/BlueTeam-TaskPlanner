import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import calendar
import datetime

class TaskPlannerUI:
    def __init__(self, root, task_manager):
        self.root = root
        self.root.title("TaskPlanner Application Dashboard")
        self.task_manager = task_manager
        self.setup_dashboard()

    def setup_dashboard(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)
        self.planner_button = tk.Button(self.main_frame, text="Planner", command=self.open_planner)
        self.planner_button.pack(fill=tk.X, padx=5, pady=2)

    def open_planner(self):
        planner_win = tk.Toplevel(self.root)
        planner_win.title("Task Planner")
        planner_win.geometry("700x400")
        PlannerWidget(planner_win, self.task_manager)

class PlannerWidget(tk.Frame):
    def __init__(self, parent, task_manager):
        super().__init__(parent)
        self.parent = parent
        self.task_manager = task_manager
        self.pack(fill=tk.BOTH, expand=True)
        self.create_ui()

    def create_ui(self):
        self.sidebar = tk.Frame(self, width=300, bg='white', highlightbackground="darkgray", highlightthickness=1)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.calendar_area = tk.Frame(self, height=400)
        self.calendar_area.pack(side=tk.TOP, fill=tk.X, expand=False, padx=5, pady=5)

        self.render_calendar()
        self.update_sidebar()

    def render_calendar(self):
        now = datetime.datetime.now()
        year, month = now.year, now.month
        cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
        month_days = cal.monthdayscalendar(year, month)

        month_label = tk.Label(self.calendar_area, text=f'{calendar.month_name[month]} {year}', font=('Arial', 14, 'bold'), bg='lightblue')
        month_label.grid(row=0, column=0, columnspan=7, sticky="ew")

        weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for i, day in enumerate(weekdays):
            lbl = tk.Label(self.calendar_area, text=day[:3], font=('Arial', 10, 'bold'), bg='lightgrey')
            lbl.grid(row=1, column=i, sticky="ew")

        for i, week in enumerate(month_days):
            for j, day in enumerate(week):
                if day != 0:
                    btn_text = f'{day}'
                    day_btn = tk.Button(self.calendar_area, text=btn_text, font=('Arial', 10), command=lambda d=day: self.day_button_clicked(d))
                    if day == now.day:
                        day_btn['bg'] = 'lightgreen'
                    day_btn.grid(row=i + 2, column=j, sticky="nsew", padx=1, pady=1)

        for col in range(7):
            self.calendar_area.grid_columnconfigure(col, weight=1)
        for row in range(len(month_days) + 2):
            self.calendar_area.grid_rowconfigure(row, weight=1)

    def day_button_clicked(self, day):
        year, month = datetime.datetime.now().year, datetime.datetime.now().month
        date_str = datetime.date(year, month, day).strftime('%Y-%m-%d')
        self.open_task_detail(date_str)

    def open_task_detail(self, date_str):
        detail_win = tk.Toplevel(self.parent)
        detail_win.title("Task Details for " + date_str)
        detail_win.geometry("400x500")

        tk.Label(detail_win, text="Description:").pack()
        description_entry = tk.Entry(detail_win)
        description_entry.pack()

        tk.Label(detail_win, text="Notes:").pack()
        notes_entry = tk.Entry(detail_win)
        notes_entry.pack()

        # Time entry
        tk.Label(detail_win, text="Time:").pack()

        # Hour entry
        hour_spin = tk.Spinbox(detail_win, from_=1, to=12, width=5, format='%02.0f')
        hour_spin.pack(side=tk.LEFT, padx=5)

        # Minute entry
        minute_spin = tk.Spinbox(detail_win, from_=0, to=59, width=5, format='%02.0f')
        minute_spin.pack(side=tk.LEFT, padx=5)

        # AM/PM selection
        am_pm_var = tk.StringVar(value="AM")
        am_pm_selector = tk.OptionMenu(detail_win, am_pm_var, "AM", "PM")
        am_pm_selector.pack(side=tk.LEFT, padx=5)

        # time converted to format to the on_done_click method
        formatted_time = self.format_time(hour_spin.get(), minute_spin.get(), am_pm_var.get())

        # Done button configuration
        done_button = tk.Button(detail_win, text="Done", command=lambda: self.on_done_click(description_entry, notes_entry, formatted_time, date_str, detail_win))
        done_button.pack(pady=10)

    def on_done_click(self, description_entry, notes_entry, formatted_time, date_str, detail_win):
        due_date = f"{date_str} {formatted_time}"
        self.save_task(description_entry.get(), notes_entry.get(), due_date)
        detail_win.destroy()

    def save_task(self, description, notes, due_date):
        self.task_manager.add_task(description, due_date, notes)
        self.update_sidebar()  # Updates the sidebar afterward

    def update_sidebar(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            self.create_task_card(task)

    def format_time(self, hour, minute, am_pm):
        return f"{hour}:{minute:02} {am_pm}"

    def create_task_card(self, task):
        try:
            due_date = datetime.datetime.strptime(task['due_date'], '%Y-%m-%d %I:%M %p')  # Note %I for 12-hour and %p for AM/PM
        except ValueError as ve:
            print(f"Error parsing date: {task['due_date']}. Error: {ve}")
            due_date = datetime.datetime.now()  # Fallback to current time on error
        
        # Creates a main frame for each task with a border
        task_frame = tk.Frame(self.sidebar, bg='white', relief=tk.RIDGE, width=300, bd=1)
        task_frame.pack(fill=tk.X, padx=5, pady=5, expand=True)

        # Date and Month extracted from the due_date
        due_date = datetime.datetime.strptime(task['due_date'], '%Y-%m-%d %I:%M %p')
        day_month_frame = tk.Frame(task_frame)
        day_month_frame.pack(side=tk.LEFT, padx=10)

        day_label = tk.Label(day_month_frame, text=due_date.strftime('%d'), font=('Arial', 16, 'bold'), bg='white')
        day_label.pack()

        month_label = tk.Label(day_month_frame, text=due_date.strftime('%b'), font=('Arial', 12), bg='white')
        month_label.pack()

        # Task Title and Notes
        text_frame = tk.Frame(task_frame, bg='white')
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        title_label = tk.Label(text_frame, text=task['description'], font=('Arial', 12, 'bold'), bg='white', anchor='w')
        title_label.pack(fill=tk.X)

        if 'notes' in task:
            notes_label = tk.Label(text_frame, text=task['notes'], font=('Arial', 10), fg='gray', bg='white', anchor='w')
            notes_label.pack(fill=tk.X)

        # Reminder time to the far right
        time_label = tk.Label(task_frame, text=due_date.strftime('%I:%M %p'), font=('Arial', 12), bg='white', anchor='e')
        time_label.pack(side=tk.RIGHT, padx=10)