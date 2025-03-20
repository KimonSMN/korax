import tkinter as tk                # python 3
from tkinter import ttk
from tkinter import *
import sqlite3
from datetime import date

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("800x800") # Set window size
        self.option_add("*tearOff", False) # This is always a good idea

        style = ttk.Style(self)
        self.tk.call("source", "forest-light.tcl")
        style.theme_use("forest-light")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = ttk.Frame(self) # frame == "screen"
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {} # create dictionary of screens
        for F in (PatientProfile, NewVisit):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("PatientProfile")

        conn = sqlite3.connect('test.db')
        curr = conn.cursor()
 
        # Creating table
        patients = """ CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name CHAR(25) NOT NULL,
                    surname CHAR(25),
                    father INTEGER,
                    age INTEGER,
                    address VARCHAR(255),
                    amka INTEGER
                ); """
        
        curr.execute(patients)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class PatientProfile(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # Title label (kept at the top)
        label = ttk.Label(self, text="Patient Profile")
        label.config(font=('Helvetica', 18)) # font size 18
        label.pack(pady=20)

        # Container frame for label & entry (to be centered)
        form_frame = ttk.Frame(self)
        form_frame.place(relx=0.5, y=280, anchor="center")  # Center the frame

        self.entries = {}   # Dictionary to store entry widgets

        # Create input fields
        self.create_labeled_entry(form_frame, "Name", 0)
        self.create_labeled_entry(form_frame, "Surname", 1)
        self.create_labeled_entry(form_frame, "Father Name", 2)
        self.create_labeled_entry(form_frame, "Age", 3)
        self.create_labeled_entry(form_frame, "Address", 4)
        self.create_labeled_entry(form_frame, "AMKA", 5)

        button = ttk.Button(form_frame, padding=(10, 9, 10, 7), text="Add new entry", style="Accent.TButton", command=self.add_entry) #padding aligns text in the center of button
        button.grid(column=0, columnspan=2, pady=10)#, sticky='nswe'

        buttonPrint = ttk.Button(form_frame, text="Print DB", command=self.print_database)
        buttonPrint.grid(column=0, columnspan=2, pady=10)

        button1 = ttk.Button(form_frame, text="Go to New Visit",
                            command=lambda: controller.show_frame("NewVisit"))
        button1.grid(column=0, columnspan=2, pady=10)

    def create_labeled_entry(self, parent, label_text, row):
        """Creates a label and an entry field in the specified parent frame."""
        label = ttk.Label(parent, text=label_text)
        label.config(font=('Helvetica', 12)) # font size 12
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")

        placeholder = tk.StringVar()
        placeholder.set(label_text)  # Default placeholder text

        entry = ttk.Entry(parent, textvariable=placeholder)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")

        entry.bind("<FocusIn>", lambda event, e=entry, v=placeholder, default=label_text: self.clearBox(e, v, default))
        entry.bind("<FocusOut>", lambda event, e=entry, v=placeholder, default=label_text: self.restore_placeholder(e, v, default))
        
        # Store the entry in a dictionary for later access
        self.entries[label_text] = (entry, placeholder)

    def clearBox(self, entry, placeholder, default_text):
        """Clears the text inside the entry field only if it's the default placeholder."""
        if placeholder.get() == default_text:
            placeholder.set("")  # Clear placeholder text

    def restore_placeholder(self, entry, placeholder, default_text):
        """Restores placeholder text if the field is left empty."""
        if not placeholder.get().strip():
            placeholder.set(default_text)  # Restore placeholder text

    def add_entry(self) -> None:
        name: str = self.entries["Name"][1].get()  # Get text from the textbox
        surname: str = self.entries["Surname"][1].get()
        father: str = self.entries["Father Name"][1].get()
        age_input: str = self.entries["Age"][1].get()
        address: str = self.entries["Address"][1].get()
        amka: str = self.entries["AMKA"][1].get()

        # Validate non-empty fields
        if not name or not surname or not father or not address:
            print("ERROR: Name, Surname, Father Name and Address can't be empty!")
            return

        # Validate Age
        try:
            age: int = int(age_input)
            if(age) <= 0 or age > 120: # Age sanity check
                print("Error: Invalid age entered.")
                return
        except ValueError:
            print("Error: Age must be a valid integer.")
            return

        # Validate AMKA 
        if not amka.isdigit() or len(amka) != 11:
            print("Error: AMKA must be an 11-digit number.")
            return

        conn = sqlite3.connect('test.db')
        curr = conn.cursor()

        curr.execute("INSERT INTO patients (name,surname,father,age,address,amka)"
                    "VALUES (?, ?, ?, ?, ?, ?)", (name,surname,father,age,address,amka))
        conn.commit()
        conn.close()

        #clear field after insert
        for label_text, (entry, placeholder) in self.entries.items():
            entry.delete(0, tk.END)
            self.restore_placeholder(entry, placeholder, label_text)
        

    def print_database(self):
        conn = sqlite3.connect('test.db')
        curr = conn.cursor()
        curr.execute("SELECT * FROM patients")
        rows = curr.fetchall()

        if rows:
            print("\n--- Patient Records ---")
            for row in rows:
                print(row)
        else:
            print("\nNo records found in the database.")



class NewVisit(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="New Visit")
        label.pack(side="top", fill="x", pady=10)

        button1 = ttk.Button(self, text="Go to Patient Profile",
                            command=lambda: controller.show_frame("PatientProfile"))
        button1.pack()



if __name__ == "__main__":
    app = App()
    # button = ttk.Style()
    # button.configure('.', font=('Helvetica', 12))
    label = ttk.Style()
    label.configure('.', font=('Helvetica', 12))
    app.mainloop()


