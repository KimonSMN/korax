import tkinter as tk
from tkinter import ttk
import sqlite3

class Patients(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title Label
        label = ttk.Label(self, text="Patients", font=('Helvetica', 18))
        label.pack(pady=10)

        # Treeview Frame
        treeFrame = ttk.Frame(self)
        treeFrame.pack(fill="y", padx=5, pady=5, side="left")

        # Scrollbar
        treeScroll = ttk.Scrollbar(treeFrame)
        treeScroll.pack(side="right", fill="y")

        # Treeview
        self.tree = ttk.Treeview(treeFrame,
                                 selectmode="extended",
                                 yscrollcommand=treeScroll.set,
                                 columns=("AMKA", "Name", "Surname", "Age"),
                                 show="headings",
                                 height=12)
        self.tree.pack(expand=True, fill="both")

        treeScroll.config(command=self.tree.yview)

        # Setup Treeview headings
        self.tree.heading("AMKA", text=" AMKA", anchor="w")
        self.tree.heading("Name", text=" Name", anchor="w")
        self.tree.heading("Surname", text="Surname", anchor="w")
        self.tree.heading("Age", text="Age", anchor="center")

        self.tree.column("AMKA", anchor="w", width=120)
        self.tree.column("Name", anchor="w", width=120)
        self.tree.column("Surname", anchor="w", width=120)
        self.tree.column("Age", anchor="center", width=30)

        # Example data
        for i in range(40):
            self.tree.insert("", "end", values=(f"Patient {i}", 20 + i % 50, f"AMKA{i:05}"))

        self.tree.bind("<Double-1>", self.openProfile)

        # Navigation Buttons
        button1 = ttk.Button(self, text="Go to Add Entry",
                             command=lambda: controller.show_frame("PatientProfile"))
        button1.pack(pady=5)

        button2 = ttk.Button(self, text="Go to Edit",
                             command=lambda: controller.show_frame("EditPatient"))
        button2.pack(pady=5)



    def populate_treeview(self, frame):
        """Uses a Treeview instead of labels for better performance."""
        columns = ("amka", "name", "surname", "age")
        
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        
        tree.heading("amka", text=" AMKA", anchor="w")
        tree.heading("name", text=" Name", anchor="w")
        tree.heading("surname", text="Surname", anchor="w")
        tree.heading("age", text="Age", anchor="center")

        tree.column("amka", width=120, anchor="w")
        tree.column("name", width=150, anchor="w")
        tree.column("surname", width=200, anchor="w")
        tree.column("age", width=30, anchor="center")

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


    def refresh(self):
        # Clear existing entries in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch updated data
        data = self.fetch_patient_data()

        # Re-insert data into the treeview
        for row in data:
            self.tree.insert("", "end", values=row)