import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from PIL import Image, ImageTk
import sqlite3

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("800x800") # Set window size
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self) # frame == "screen"
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


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class PatientProfile(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Title label (kept at the top)
        label = tk.Label(self, text="Patient Profile", font=controller.title_font)
        label.pack(pady=10)

        # Container frame for label & entry (to be centered)
        form_frame = tk.Frame(self)
        form_frame.place(relx=0.5, y=200, anchor="center")  # Center the frame

        self.entries = {}   # Dictionary to store entry widgets

        # Create input fields
        self.create_labeled_entry(form_frame, "Name", 0)
        self.create_labeled_entry(form_frame, "Surname", 1)
        self.create_labeled_entry(form_frame, "Father Name", 2)
        self.create_labeled_entry(form_frame, "Age", 3)
        self.create_labeled_entry(form_frame, "Address", 4)
        self.create_labeled_entry(form_frame, "AMKA", 5)

        button = tk.Button(form_frame, text="add new entry", font=('Arial',12), command=self.add_entry)
        button.grid(column=0, columnspan=2, pady=10)

        buttonPrint = tk.Button(form_frame, text="Print DB", command=self.print_database)
        buttonPrint.grid(column=0, columnspan=2, pady=10)

        button1 = tk.Button(form_frame, text="Go to New Visit",
                            command=lambda: controller.show_frame("NewVisit"))
        button1.grid(column=0, columnspan=2, pady=10)




    def create_labeled_entry(self, parent, label_text, row):
        """Creates a label and an entry field in the specified parent frame."""
        label = tk.Label(parent, text=label_text, font=('Arial', 12))
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")

        entry = tk.Entry(parent)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")

        # Store the entry in a dictionary for later access
        self.entries[label_text] = entry

    def add_entry(self):
        name = self.entries["Name"].get()  # Get text from the textbox
        surname = self.entries["Surname"].get()
        father = self.entries["Father Name"].get()
        age = self.entries["Age"].get()
        address = self.entries["Address"].get()
        amka = self.entries["AMKA"].get()

        if name and surname and father and age.isdigit():
            conn = sqlite3.connect('test.db')
            curr = conn.cursor()

            curr.execute("INSERT INTO patients (name,surname,father,age,address,amka) "
                        "VALUES (?, ?, ?, ?, ?, ?)", (name,surname,father,age,address,amka))
            conn.commit()
            conn.close()

            #clear field after insert
            for field in self.entries.values():
                field.delete(0, tk.END)
        else:
            print("Please fill out all fields correctly")

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
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="New Visit", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Patient Profile",
                            command=lambda: controller.show_frame("PatientProfile"))
        button1.pack()



if __name__ == "__main__":
    app = App()
    app.mainloop()



# #create database or connect to one
# conn = sqlite3.connect('test.db')

# #create cursor
# curr = conn.cursor()

# add_patients_query = """CREATE TABLE IF NOT EXISTS patients (
#              id INTEGER PRIMARY KEY AUTOINCREMENT,
#              name VARCHAR(45),
#              surname VARCHAR(45),
#              father VARCHAR(45),
#              age INTEGER,
#              address TEXT,
#              amka TEXT
#              )"""


# #create table
# curr.execute(add_patients_query)

# #commit changes
# conn.commit()

# # return all from patients
# # curr.execute("SELECT * FROM patients")
# # print(curr.fetchone())

# def add_entry():
#     name = name_entry.get() # get text form the textbox
#     surname = surname_entry.get()
#     father = father_entry.get()
#     age = age_entry.get()
#     address = address_entry.get()
#     amka = amka_entry.get()

#     if name and surname and father and age.isdigit():
#         conn = sqlite3.connect('test.db')
#         curr = conn.cursor()

#         curr.execute("INSERT INTO patients (name,surname,father,age,address,amka) "
#                      "VALUES (?, ?, ?, ?, ?, ?)", (name,surname,father,age,address,amka))
#         conn.commit()
#         conn.close()

#         name_entry.delete(0, END) #clear field after insert
#         surname_entry.delete(0, END) #clear field after insert
#         father_entry.delete(0, END) #clear field after insert
#         age_entry.delete(0, END) #clear field after insert
#         address_entry.delete(0, END) #clear field after insert
#         amka_entry.delete(0, END) #clear field after insert
#     else:
#         print("Please fill out all fields correctly")

# def search_entry():
#     amka = search.get() # get text from textbox

#     if amka:
#         conn = sqlite3.connect("test.db")
#         curr = conn.cursor()

#         curr.execute("SELECT * FROM patients WHERE amka = ?",(amka,))
#         result = curr.fetchone() # fetch one row
#         conn.close()
#         if result:  
#             label.config(text=f"Result: {result}")  # Update label with the fetched data
#         else:
#             label.config(text="No data found")  

# def print_database():
#     conn = sqlite3.connect('test.db')
#     curr = conn.cursor()
#     curr.execute("SELECT * FROM patients")
#     rows = curr.fetchall()

#     if rows:
#         print("\n--- Patient Records ---")
#         for row in rows:
#             print(row)
#     else:
#         print("\nNo records found in the database.")

# # def get_field():
# #     conn = sqlite3.connect("test.db")
# #     curr = conn.cursor()

# #     curr.execute("SELECT * FROM patients WHERE id = 1")
# #     result = curr.fetchone() # fetch one row

# #     conn.close()

# #     if result:  
# #         label.config(text=f"Name: {result[1]}")  # Update label with the fetched data
# #     else:
# #         label.config(text="No data found")  


# label = Label(root, text="Type AMKA of patient", font=("Arial", 12))
# label.pack(pady=20)

# search = Entry(root) #entry to search
# search.pack()

# button = Button(root, text="Search for entry", font=('Arial',12), command=search_entry)
# button.pack(padx=5, pady=5)

# button = Button(root, text="Add patient entry", font=('Arial',12), command=add_entry)
# button.pack(padx=5, pady=5)

# button = Button(root, text="Print DB", font=('Arial',12), command=print_database)
# button.pack(padx=5, pady=5)

