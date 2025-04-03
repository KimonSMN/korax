import tkinter as tk
from tkinter import ttk
import sqlite3

from screens.profile import PatientProfile
from screens.patients import Patients
from screens.edit import EditPatient

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x800")
        self.option_add("*tearOff", False)

        self.selected_patient = None  # Store selected patient data

        style = ttk.Style(self)
        self.tk.call("source", "forest-light.tcl")
        style.theme_use("forest-light")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PatientProfile, Patients, EditPatient):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Patients")

        conn = sqlite3.connect('database.db')
        curr = conn.cursor()
        curr.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                amka INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT,
                father TEXT,
                age INTEGER,
                address TEXT,
                allergies TEXT,
                medications TEXT
            );
        """)
        conn.commit()
        conn.close()

    def show_frame(self, page_name, data=None):
        frame = self.frames[page_name]
        
        if data:
            self.selected_patient = data
            if hasattr(frame, "set_data"):
                frame.set_data(data)

        if hasattr(frame, "refresh"):
            frame.refresh()
            
        frame.tkraise()
