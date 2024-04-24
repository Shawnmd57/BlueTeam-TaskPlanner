import sqlite3
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.db_file = 'taskplanner.db'
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_file)

    def create_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                due_date TEXT,
                notes TEXT,
                completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)) DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def get_tasks(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, description, due_date, notes, completed FROM tasks')
        result = cursor.fetchall()
        tasks = [{'id': row[0], 'description': row[1], 'due_date': row[2],
                'notes': row[3], 'completed': bool(row[4])} for row in result]
        conn.close()
        return tasks

    def add_task(self, description, due_date, notes):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO tasks (description, due_date, notes) VALUES (?, ?, ?)''', (description, due_date, notes))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
        finally:
            conn.close()

    def update_task(self, task_id, **kwargs):
        updates = ', '.join([f"{k} = ?" for k in kwargs])
        values = tuple(kwargs.values())
        
        cursor = self.conn.cursor()
        cursor.execute(f'''
            UPDATE tasks SET {updates} WHERE id = ?
        ''', values + (task_id,))
        self.conn.commit()

    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()