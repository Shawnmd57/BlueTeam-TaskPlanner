import tkinter as tk
from PIL import Image, ImageTk
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

        # Load and display the image
        self.load_dashboard_image()

        self.planner_button = tk.Button(self.main_frame, text="Planner", command=self.open_planner)
        self.planner_button.pack(fill=tk.X, padx=5, pady=2)

    def load_dashboard_image(self):
        try:
            image = Image.open("TaskManager.png")
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(self.main_frame, image=photo)
            image_label.image = photo  # keep a reference!
            image_label.pack(padx=10, pady=10)
        except IOError as e:
            print(f"Error loading the image: {e}")

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
        self.no_task_image = None
        self.pack(fill=tk.BOTH, expand=True)
        self.current_year, self.current_month = datetime.datetime.now().year, datetime.datetime.now().month
        self.create_ui()

    def create_ui(self):
        self.sidebar = tk.Frame(self, width=300, bg='white', highlightbackground="darkgray", highlightthickness=1)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.calendar_area = tk.Frame(self, height=400)
        self.calendar_area.pack(side=tk.TOP, fill=tk.X, expand=False, padx=5, pady=5)

        self.render_calendar()
        self.update_sidebar()

    def render_calendar(self):
        year, month = self.current_year, self.current_month
        cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
        month_days = cal.monthdayscalendar(year, month)

        # Clear widgets
        for widget in self.calendar_area.winfo_children():
            widget.destroy()

        # Month control with navigation
        control_frame = tk.Frame(self.calendar_area)
        control_frame.grid(row=0, column=0, columnspan=7, sticky="ew")

        left_button = tk.Button(control_frame, text="<", command=self.previous_month)
        left_button.pack(side=tk.LEFT)

        month_label = tk.Label(control_frame, text=f'{calendar.month_name[month]} {year}', font=('Arial', 14, 'bold'))
        month_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

        right_button = tk.Button(control_frame, text=">", command=self.next_month)
        right_button.pack(side=tk.LEFT)

        # Day headers
        weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        for i, day in enumerate(weekdays):
            lbl = tk.Label(self.calendar_area, text=day[:3], font=('Arial', 10, 'bold'), bg='lightgrey')
            lbl.grid(row=1, column=i, sticky="ew")

        # Day buttons
        for i, week in enumerate(month_days):
            for j, day in enumerate(week):
                if day != 0:
                    day_btn = tk.Button(self.calendar_area, text=f'{day}', font=('Arial', 10),
                                        command=lambda d=day: self.day_button_clicked(d))
                    if day == datetime.datetime.now().day and month == datetime.datetime.now().month:
                        day_btn['bg'] = 'lightgreen'
                    day_btn.grid(row=i + 2, column=j, sticky="nsew", padx=1, pady=1)

        self.configure_grid()

    def configure_grid(self):
        for col in range(7):
            self.calendar_area.grid_columnconfigure(col, weight=1)
        self.calendar_area.grid_rowconfigure(0, weight=1)    # For extra controls
        for row in range(1, 8):
            self.calendar_area.grid_rowconfigure(row, weight=1)

    def previous_month(self):
        """Go to the previous month."""
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.render_calendar()

    def next_month(self):
        """Go to the next month."""
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.render_calendar()

    def day_button_clicked(self, day):
        year, month = self.current_year, self.current_month
        date_str = datetime.date(year, month, day).strftime('%Y-%m-%d')
        self.open_task_detail(date_str)

    def open_task_detail(self, date_str, task_id=None):
        detail_win = tk.Toplevel(self.parent)
        detail_win.title("Task Details for " + date_str)
        detail_win.geometry("400x500")

        # Fetch task details if editing
        task = None
        if task_id:
            tasks = self.task_manager.get_tasks()
            task = next((t for t in tasks if t['id'] == task_id), None)

        # Setup widgets with existing task details if present
        tk.Label(detail_win, text="Title:").pack()
        description_entry = tk.Entry(detail_win)
        description_entry.pack()
        description_entry.insert(0, task['description'] if task else '')

        tk.Label(detail_win, text="Description:").pack()
        notes_entry = tk.Entry(detail_win)
        notes_entry.pack()
        notes_entry.insert(0, task['notes'] if task else '')

        # Time label and entry
        tk.Label(detail_win, text="Time:").pack()
        time_frame = tk.Frame(detail_win)
        time_frame.pack(pady=5)

        # Preset the time if editing
        due_date_time = datetime.datetime.strptime(task['due_date'], '%Y-%m-%d %H:%M') if task else datetime.datetime.now()
        hour = due_date_time.strftime('%I')
        minute = due_date_time.strftime('%M')
        am_pm = due_date_time.strftime('%p')

        hour_spin = tk.Spinbox(time_frame, from_=1, to=12, width=5, format='%02.0f')
        hour_spin.pack(side=tk.LEFT, padx=5)
        hour_spin.delete(0, tk.END)
        hour_spin.insert(0, hour)

        minute_spin = tk.Spinbox(time_frame, from_=0, to=59, width=5, format='%02.0f')
        minute_spin.pack(side=tk.LEFT, padx=5)
        minute_spin.delete(0, tk.END)
        minute_spin.insert(0, minute)

        am_pm_var = tk.StringVar(value=am_pm)
        am_pm_selector = tk.OptionMenu(time_frame, am_pm_var, "AM", "PM")
        am_pm_selector.pack(side=tk.LEFT, padx=5)

        done_button = tk.Button(detail_win, text="Done", command=lambda: self.on_done_click(description_entry, notes_entry, hour_spin, minute_spin, am_pm_var, date_str, detail_win, task_id))
        done_button.pack(pady=10)

    def on_done_click(self, description_entry, notes_entry, hour_spin, minute_spin, am_pm_var, date_str, detail_win, task_id=None):
        description = description_entry.get()
        notes = notes_entry.get()
        hour = hour_spin.get()
        minute = minute_spin.get()
        am_pm = am_pm_var.get()
        formatted_time = self.format_time(hour, minute, am_pm)

        # Splitting date_str to ensure it contains only the date part
        date_only = date_str.split()[0]
        due_date = f"{date_only} {formatted_time}"

        try:
            datetime.datetime.strptime(due_date, '%Y-%m-%d %H:%M')
            if task_id:
                # Update existing task
                self.task_manager.update_task(task_id, description=description, notes=notes, due_date=due_date, completed=False)
            else:
                # Add new task if no ID is provided
                self.task_manager.add_task(description, notes, due_date)
            detail_win.destroy()
            self.update_sidebar()
        except ValueError:
            print(f"Error: Invalid date format for {due_date}. Expected format is 'YYYY-MM-DD HH:MM'")

    def save_task(self, description, notes, due_date):
        self.task_manager.add_task(description, due_date, notes)
        self.update_sidebar()  # Updates the sidebar afterward

    def update_sidebar(self):
        # Clears existing task cards
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        # Creates new task cards or shows an image if no tasks
        tasks = self.task_manager.get_tasks()
        if tasks:
            # Sort tasks by due date
            sorted_tasks = sorted(tasks, key=lambda x: datetime.datetime.strptime(x['due_date'], '%Y-%m-%d %H:%M'))
            for task in sorted_tasks:
                self.create_task_card(task)
        else:
            self.display_no_task_image()

    def display_no_task_image(self):
        if not self.no_task_image:
            try:
                self.no_task_image = ImageTk.PhotoImage(Image.open("Tasks.png"))
            except Exception as e:
                print(f"Failed to load image: {e}")
                return  # Exit if the image cannot be loaded

        # Display the image
        image_label = tk.Label(self.sidebar, image=self.no_task_image)
        image_label.image = self.no_task_image  # Keep a reference!
        image_label.pack(pady=20)

    def format_time(self, hour, minute, am_pm):
        hour = int(hour)
        minute = int(minute)
        if am_pm == 'PM' and hour != 12:
            hour += 12
        elif am_pm == 'AM' and hour == 12:
            hour = 0
        return f"{hour:02}:{minute:02}"

    def create_task_card(self, task):
        # Parsing the due_date string to a datetime object
        try:
            due_date = datetime.datetime.strptime(task['due_date'], '%Y-%m-%d %H:%M')
            display_due_date = due_date.strftime('%Y-%m-%d %I:%M %p')  # Format for display in AM/PM
        except ValueError as ve:
            print("Error parsing date for task:", task)
            return  # Optionally handle or return if the date format is invalid

        task_frame = tk.Frame(self.sidebar, bg='white', relief=tk.RIDGE, bd=1)
        task_frame.pack(fill=tk.X, padx=5, pady=5, expand=True)

        # Bind click event to the entire task frame
        task_frame.bind("<Button-1>", lambda e, t=task: self.show_task_options(t))

        day_month_frame = tk.Frame(task_frame)
        day_month_frame.pack(side=tk.LEFT, padx=10)
        day_month_frame.bind("<Button-1>", lambda e, t=task: self.show_task_options(t))  # Bind here too if needed

        day_label = tk.Label(day_month_frame, text=due_date.strftime('%d'), font=('Arial', 16, 'bold'), bg='white')
        day_label.pack()
        month_label = tk.Label(day_month_frame, text=due_date.strftime('%b'), font=('Arial', 12), bg='white')
        month_label.pack()

        text_frame = tk.Frame(task_frame, bg='white')
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        text_frame.bind("<Button-1>", lambda e, t=task: self.show_task_options(t))  # Bind here too if needed

        title_label = tk.Label(text_frame, text=task['description'], font=('Arial', 12, 'bold'), bg='white', anchor='w')
        title_label.pack(fill=tk.X)
        title_label.bind("<Button-1>", lambda e, t=task: self.show_task_options(t))  # Ensure all components propagate the click event

        if 'notes' in task:
            notes_label = tk.Label(text_frame, text=task['notes'], font=('Arial', 10), fg='gray', bg='white', anchor='w')
            notes_label.pack(fill=tk.X)
            notes_label.bind("<Button-1>", lambda e, t=task: self.show_task_options(t))  # Bind here too if needed

        time_label = tk.Label(task_frame, text=due_date.strftime('%I:%M %p'), font=('Arial', 12), bg='white', anchor='e')
        time_label.pack(side=tk.RIGHT, padx=10)
        time_label.bind("<Button-1>", lambda e, t=task: self.show_task_options(t))  # Bind here too if needed

    def show_task_options(self, task):
        options_win = tk.Toplevel(self.parent)
        options_win.title("Reminder Options")
        options_win.geometry("250x150")

        back_button = tk.Button(options_win, text="Back", command=options_win.destroy)
        back_button.pack(fill=tk.X, padx=20, pady=5)

        edit_button = tk.Button(options_win, text="Edit", command=lambda: [options_win.destroy(), self.open_task_detail(task['due_date'], task['id'])])
        edit_button.pack(fill=tk.X, padx=20, pady=5)

        delete_button = tk.Button(options_win, text="Delete", command=lambda: [options_win.destroy(), self.confirm_delete(task)])
        delete_button.pack(fill=tk.X, padx=20, pady=5)

    def confirm_delete(self, task):
        confirm_win = tk.Toplevel(self.parent)
        confirm_win.title("Confirm Deletion")
        confirm_win.geometry("250x100")
        confirm_label = tk.Label(confirm_win, text="Are you sure you want to delete this reminder?")
        confirm_label.pack(padx=20, pady=10)
        yes_button = tk.Button(confirm_win, text="Yes", command=lambda: [self.task_manager.delete_task(task['id']), confirm_win.destroy(), self.update_sidebar()])
        yes_button.pack(side=tk.LEFT, padx=10, pady=10)
        no_button = tk.Button(confirm_win, text="No", command=confirm_win.destroy)
        no_button.pack(side=tk.RIGHT, padx=10, pady=10)
