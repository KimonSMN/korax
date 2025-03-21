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
        button1 = ttk.Button(self, text="Go to Add Entry",
                             command=lambda: controller.show_frame("PatientProfile"))
        button1.pack(pady=10)
        
        button2 = ttk.Button(self, text="Go to Edit",
                             command=lambda: controller.show_frame("EditPatient"))
        button2.pack(pady=10)



    def populate_treeview(self, frame):
        """Uses a Treeview instead of labels for better performance."""
        columns = ("amka", "name", "surname", "age")
        
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        
        tree.heading("amka", text="AMKA")
        tree.heading("name", text="Name")
        tree.heading("surname", text="Surname")
        tree.heading("age", text="Age")

        tree.column("amka", width=150, anchor="w")
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
        curr.execute("SELECT amka, name, surname, age FROM patients")
        rows = curr.fetchall()
        conn.close()
        return rows

    def openProfile(self, event):
        curItem = self.tree.focus()
        values = self.tree.item(curItem, "values")

        amka = values[0]

        conn = sqlite3.connect('database.db')
        curr = conn.cursor()
        curr.execute("SELECT * FROM patients WHERE amka = ?", (amka,))
        row = curr.fetchone()
        conn.close()

        if values:
            patient_data = {
                "amka": row[0],
                "name": row[1],
                "surname": row[2],
                "father": row[3],
                "age": row[4],
                "address": row[5],
                "allergies": row[6],
                "medications": row[7]
            }
        print(row)
        self.controller.show_frame("EditPatient", patient_data)

