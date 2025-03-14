from tkinter import *
from PIL import Image, ImageTk
import sqlite3

root = Tk()
root.title("Test")
root.geometry("400x400")

frame = Frame(root)
frame.pack(pady=20, anchor="w")



# First Name
name_label = Label(frame, text="Name", font=('Arial', 12))
name_label.grid(padx=5, pady=5, row=0, column=0)

name_entry = Entry(frame)
name_entry.grid(padx=5, pady=5, row=0, column=1)

# Surname Name
surname_label = Label(frame, text="Surname", font=('Arial', 12))
surname_label.grid(padx=5, pady=5, row=1, column=0)

surname_entry = Entry(frame)
surname_entry.grid(padx=5, pady=5, row=1, column=1)

# Father Name
father_label = Label(frame, text="Father Name", font=('Arial', 12))
father_label.grid(padx=5, pady=5, row=2, column=0)

father_entry = Entry(frame)
father_entry.grid(padx=5, pady=5, row=2, column=1)

# Age
age_label = Label(frame, text="Age", font=('Arial', 12))
age_label.grid(padx=5, pady=5, row=3, column=0)

age_entry = Entry(frame)
age_entry.grid(padx=5, pady=5, row=3, column=1)

# Address
address_label = Label(frame, text="Address", font=('Arial', 12))
address_label.grid(padx=5, pady=5, row=4, column=0)

address_entry = Entry(frame)
address_entry.grid(padx=5, pady=5, row=4, column=1)

# AMKA
amka_label = Label(frame, text="AMKA", font=('Arial', 12))
amka_label.grid(padx=5, pady=5, row=5, column=0)

amka_entry = Entry(frame)
amka_entry.grid(padx=5, pady=5, row=5, column=1)

#create database or connect to one
conn = sqlite3.connect('test.db')

#create cursor
curr = conn.cursor()

add_patients_query = """CREATE TABLE IF NOT EXISTS patients (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name VARCHAR(45),
             surname VARCHAR(45),
             father VARCHAR(45),
             age INTEGER,
             address TEXT,
             amka TEXT
             )"""


#create table
curr.execute(add_patients_query)

#commit changes
conn.commit()

# return all from patients
# curr.execute("SELECT * FROM patients")
# print(curr.fetchone())

def add_entry():
    name = name_entry.get() # get text form the textbox
    surname = surname_entry.get()
    father = father_entry.get()
    age = age_entry.get()
    address = address_entry.get()
    amka = amka_entry.get()

    if name and surname and father and age.isdigit():
        conn = sqlite3.connect('test.db')
        curr = conn.cursor()

        curr.execute("INSERT INTO patients (name,surname,father,age,address,amka) "
                     "VALUES (?, ?, ?, ?, ?, ?)", (name,surname,father,age,address,amka))
        conn.commit()
        conn.close()

        name_entry.delete(0, END) #clear field after insert
        surname_entry.delete(0, END) #clear field after insert
        father_entry.delete(0, END) #clear field after insert
        age_entry.delete(0, END) #clear field after insert
        address_entry.delete(0, END) #clear field after insert
        amka_entry.delete(0, END) #clear field after insert
    else:
        print("Please fill out all fields correctly")

def search_entry():
    name = search.get() # get text from textbox

    if name:
        conn = sqlite3.connect("test.db")
        curr = conn.cursor()

        curr.execute("SELECT * FROM patients WHERE name = ?",(name,))
        result = curr.fetchone() # fetch one row
        conn.close()
        if result:  
            label.config(text=f"Name: {result}")  # Update label with the fetched data
        else:
            label.config(text="No data found")  

def print_database():
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

# def get_field():
#     conn = sqlite3.connect("test.db")
#     curr = conn.cursor()

#     curr.execute("SELECT * FROM patients WHERE id = 1")
#     result = curr.fetchone() # fetch one row

#     conn.close()

#     if result:  
#         label.config(text=f"Name: {result[1]}")  # Update label with the fetched data
#     else:
#         label.config(text="No data found")  


label = Label(root, text="Type name of patient", font=("Arial", 12))
label.pack(pady=20)

search = Entry(root)
search.pack()

button = Button(root, text="Search for entry", font=('Arial',12), command=search_entry)
button.pack(padx=5, pady=5)

button = Button(root, text="Add patient entry", font=('Arial',12), command=add_entry)
button.pack(padx=5, pady=5)

button = Button(root, text="Print DB", font=('Arial',12), command=print_database)
button.pack(padx=5, pady=5)

root.mainloop()
