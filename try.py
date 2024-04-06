import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("505x500")
        self.root.resizable(False, False)
        
        self.conn = sqlite3.connect('todo.db')
        self.create_table()

        # Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('Treeview', font=('Arial', 12))

        # Entry widget for entering tasks
        self.task_entry = ttk.Entry(root, width=40)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky='ew')

        # Add Task button
        self.add_button = ttk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky='e')

        # Delete Task button
        self.delete_button = ttk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=0, column=3, padx=(0, 10), pady=10, sticky='e')

        # Treeview widget to display tasks
        self.task_tree = ttk.Treeview(root, columns=('ID', 'Task'), show='headings', height=15)
        self.task_tree.heading('ID', text='ID')
        self.task_tree.heading('Task', text='Task')
        self.task_tree.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky='ew')

        # Load tasks initially
        self.load_tasks()

        # Exit button
        self.exit_button = ttk.Button(root, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=2, column=0, columnspan=4, padx=10, pady=(10, 0), sticky='ew')

        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    task TEXT NOT NULL
                    )'''
        self.conn.execute(query)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            query = "INSERT INTO tasks (task) VALUES (?)"
            self.conn.execute(query, (task,))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.load_tasks()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def load_tasks(self):
        self.task_tree.delete(*self.task_tree.get_children())
        query = "SELECT * FROM tasks"
        cursor = self.conn.execute(query)
        for row in cursor.fetchall():
            self.task_tree.insert('', 'end', values=row)

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task_id = self.task_tree.item(selected_item, 'values')[0]
            query = "DELETE FROM tasks WHERE id = ?"
            self.conn.execute(query, (task_id,))
            self.conn.commit()
            self.load_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
