import tkinter as tk
from tkinter import ttk
import sqlite3

class Patients(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Patients", font=('Helvetica', 18))
        label.pack(pady=10)

        # Scrollable Canvas Frame
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create a window inside the canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # self.populate_labels(self.scrollable_frame, data)
        self.tree = self.populate_treeview(canvas)

        # Force UI update to fix scrolling
        self.update_idletasks()

        self.tree.bind("<Double 1>",self.openProfile)

        # Navigation button
        button1 = ttk.Button(self, text="Go to Patient Profile",
                             command=lambda: controller.show_frame("PatientProfile"))
        button1.pack(pady=10)
        
    def populate_treeview(self, frame):
        """Uses a Treeview instead of labels for better performance."""
        columns = ("name", "surname", "age")
        
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        
        tree.heading("name", text="Name")
        tree.heading("surname", text="Surname")
        tree.heading("age", text="Age")

        tree.column("name", width=150, anchor="w")
        tree.column("surname", width=150, anchor="w")
        tree.column("age", width=50, anchor="center")

        # Insert data into treeview
        data = self.fetch_patient_data()
        for row in data:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)
        return tree

    def fetch_patient_data(self):
        """Fetches data from SQLite and returns it as a list of tuples."""
        conn = sqlite3.connect('database.db')
        curr = conn.cursor()
        curr.execute("SELECT name, surname, age FROM patients")
        rows = curr.fetchall()
        conn.close()
        return rows

    def openProfile(self, event):
        print("Selected Entry")
        curItem = self.tree.focus()
        print (self.tree.item(curItem, "values"))
        self.controller.show_frame("PatientProfile")