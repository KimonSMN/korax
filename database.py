import tkinter as tk                # python 3
from tkinter import ttk
from tkinter import *
import sqlite3
import customtkinter
from datetime import date
from faker import Faker
import random

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
        for F in (PatientProfile, Patients):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Patients")

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
                    amka INTEGER,
                    allergies TEXT(1000),
                    medications TEXT(1000)
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
        form_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

        self.entries = {}   # Dictionary to store entry widgets

        # Create input fields
        self.create_labeled_entry(form_frame, "Name", 0, 30)
        self.create_labeled_entry(form_frame, "Surname", 1, 30)
        self.create_labeled_entry(form_frame, "Father Name", 2, 30)
        self.create_labeled_entry(form_frame, "Age", 3, 30)
        self.create_labeled_entry(form_frame, "Address", 4, 30)
        self.create_labeled_entry(form_frame, "AMKA", 5, 30)
        self.allergies = self.create_textbox(form_frame, 200, 30, 6, "Enter Allergies...")


        button = ttk.Button(form_frame, padding=(10, 9, 10, 7), text="Add new entry", style="Accent.TButton", command=self.add_entry) #padding aligns text in the center of button
        button.grid(column=0, columnspan=2, pady=10)

        buttonPrint = ttk.Button(form_frame, text="Print DB", command=self.print_database)
        buttonPrint.grid(column=0, columnspan=2, pady=10)

        self.allergies_visible = False  # Track visibility
        ttk.Button(form_frame, text="Toggle Allergies", command=lambda: self.toggle_text(self.allergies, 6)).grid(column=0, columnspan=2, pady=10)
        self.allergies.grid_remove() # Placed after the creation of the button because it didn't dynamically if placed before

        button1 = ttk.Button(form_frame, text="Go to Patients",
                            command=lambda: controller.show_frame("Patients"))
        button1.grid(column=0, columnspan=2, pady=10)

    def create_labeled_entry(self, parent, label_text, row, width):
        """Creates a label and an entry field in the specified parent frame."""
        # label = ttk.Label(parent, text=label_text)
        # label.configure(font=('Helvetica', 12)) # font size 12
        # label.grid(row=row, column=0, padx=10, pady=5, sticky="e")

        placeholder = tk.StringVar()
        placeholder.set(label_text)  # Default placeholder text

        entry = ttk.Entry(parent, textvariable=placeholder, width=width)
        entry.grid(row=row, column=1, pady=5, sticky="nsew")

        entry.bind("<FocusIn>", lambda event, w=entry, d=label_text: self.clear_placeholder(w, d))
        entry.bind("<FocusOut>", lambda event, w=entry, d=label_text: self.restore_placeholder(w, d))

        entry.configure(foreground="gray", font=('Helvatica', 10))  # Placeholder text color
        
        # Store the entry in a dictionary for later access
        self.entries[label_text] = (entry, placeholder)
        
    def create_textbox(self, parent: Frame, height: int, width: int, row: int, label_text: str):
        text = customtkinter.CTkTextbox(parent, height = height, width = width, 
                                        fg_color="white", border_width=1 ,border_color="lightgray", text_color="gray", font=('Helvetica', 12))
        text.insert("1.0", label_text)
        text.grid(row=row, column=0, columnspan=2, pady=5, sticky="nsew")

        placeholder = tk.StringVar()
        placeholder.set(label_text)  # Default placeholder text

        text.bind("<FocusIn>", lambda event, w=text, d=label_text: self.clear_placeholder(w, d))
        text.bind("<FocusOut>", lambda event, w=text, d=label_text: self.restore_placeholder(w, d))
    
        self.entries[label_text] = (text, None)
        return text
    
    def clear_placeholder(self, widget, default_text: str) -> None:
        """Clears the placeholder text in a ttk.Entry or customtkinter.CTkTextbox when clicked."""
        if isinstance(widget, ttk.Entry):  # Handling ttk.Entry
            if widget.get() == default_text:
                widget.delete(0, tk.END)
                widget.config(foreground="black")  # Normal text color
        elif isinstance(widget, customtkinter.CTkTextbox):  # Handling customtkinter.CTkTextbox
            if widget.get("1.0", "end-1c") == default_text:
                widget.delete("1.0", "end")
                widget.configure(text_color="black")  # Normal text color

    def restore_placeholder(self, widget, default_text: str) -> None:
        """Restores the placeholder text if the ttk.Entry or customtkinter.CTkTextbox is empty."""
        if isinstance(widget, ttk.Entry):  # Handling ttk.Entry
            if not widget.get().strip():
                widget.insert(0, default_text)
                widget.config(foreground="gray")  # Placeholder color
        elif isinstance(widget, customtkinter.CTkTextbox):  # Handling customtkinter.CTkTextbox
            if not widget.get("1.0", "end-1c").strip():
                widget.insert("1.0", default_text)
                widget.configure(text_color="gray")  # Placeholder color

    def add_entry(self) -> None:

        # Retrieve values dynamically from both ttk.Entry and customtkinter.CTkTextbox
        def get_widget_value(widget):
            """Returns the value from an Entry or Text widget dynamically."""
            if isinstance(widget, ttk.Entry):  # ttk.Entry
                return widget.get().strip()
            elif isinstance(widget, customtkinter.CTkTextbox):  # customtkinter.CTkTextbox
                return widget.get("1.0", "end-1c").strip()
            return ""
        
        # Extract input values
        name: str = get_widget_value(self.entries["Name"][0])  
        surname: str = get_widget_value(self.entries["Surname"][0])
        father: str = get_widget_value(self.entries["Father Name"][0])
        age_input: str = get_widget_value(self.entries["Age"][0])
        address: str = get_widget_value(self.entries["Address"][0])
        amka: str = get_widget_value(self.entries["AMKA"][0])
        allergies: str = get_widget_value(self.entries["Enter Allergies..."][0])

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
        amka = amka.replace(" ", "")  # Remove accidental spaces
        if not amka.isdigit() or len(amka) != 11:
            print("Error: AMKA must be an 11-digit number.")
            return

        conn = sqlite3.connect('test.db')
        curr = conn.cursor()

        curr.execute("INSERT INTO patients (name,surname,father,age,address,amka,allergies)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?)", (name,surname,father,age,address,amka,allergies))
        conn.commit()
        conn.close()

        # Clear fields after insertion and restore placeholders
        for label_text, (widget, placeholder) in self.entries.items():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, customtkinter.CTkTextbox):
                widget.delete("1.0", "end")
            self.restore_placeholder(widget, label_text)

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

    def toggle_text(self, widget, row):
        """Show/hide the allergies textbox """
        if self.allergies_visible:
            widget.grid_remove()
        else:
            widget.grid(row=row, column=0, columnspan=2, pady=5, sticky="nsew")

        self.allergies_visible = not self.allergies_visible

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
        conn = sqlite3.connect('test.db')
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


def populate_database(num_entries=1000):
    """Populates the database with random patients if it's empty."""
    fake = Faker()
    conn = sqlite3.connect("test.db")
    curr = conn.cursor()

    # 🛠️ **Ensure the table exists BEFORE querying**
    curr.execute("""CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    surname TEXT,
                    father TEXT,
                    age INTEGER,
                    address TEXT,
                    amka TEXT,
                    allergies TEXT,
                    medications TEXT
                );""")
    conn.commit()  # ✅ Commit the table creation to avoid errors

    # ✅ Now check if the table has records
    curr.execute("SELECT COUNT(*) FROM patients")
    count = curr.fetchone()[0]

    if count >= num_entries:
        print(f"✅ Database already contains {count} patients. Skipping population.")
        conn.close()
        return

    print(f"⚡ Populating database with {num_entries} random patients...")
    for _ in range(num_entries):
        name = fake.first_name()
        surname = fake.last_name()
        father = fake.first_name_male()
        age = random.randint(1, 100)
        address = fake.address().replace("\n", ", ")
        amka = "".join([str(random.randint(0, 9)) for _ in range(11)])
        allergies = fake.sentence(nb_words=5) if random.random() > 0.5 else ""
        medications = fake.sentence(nb_words=5) if random.random() > 0.5 else ""

        curr.execute("INSERT INTO patients (name, surname, father, age, address, amka, allergies, medications) "
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     (name, surname, father, age, address, amka, allergies, medications))

    conn.commit()
    conn.close()
    print(f"✅ Successfully inserted {num_entries} random patients!")


if __name__ == "__main__":
    
    populate_database(100)

    app = App()
    label = ttk.Style()
    label.configure('.', font=('Helvetica', 12))
    app.mainloop()


