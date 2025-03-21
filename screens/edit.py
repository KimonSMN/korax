import tkinter as tk
from tkinter import ttk
import sqlite3

class EditPatient(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Edit Patient", font=('Helvetica', 18))
        label.pack(pady=10)

        # Force UI update to fix scrolling
        self.update_idletasks()

        # Navigation button
        button1 = ttk.Button(self, text="Go to Patient List",
                             command=lambda: controller.show_frame("Patients"))
        button1.pack(pady=10)

        button2 = ttk.Button(self, text="Go to Add entry",
                             command=lambda: controller.show_frame("PatientProfile"))
        button2.pack(pady=10)

        form_frame = ttk.Frame(self)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

        self.entries = {}   # Dictionary to store entry widgets

        # Create input fields
        self.name_entry = self.create_labeled_entry(form_frame, "Name", 0, 30)
        self.surname_entry = self.create_labeled_entry(form_frame, "Surname", 1, 30)
        self.father_entry = self.create_labeled_entry(form_frame, "Father Name", 2, 30)
        self.age_entry = self.create_labeled_entry(form_frame, "Age", 3, 30)
        self.address_entry = self.create_labeled_entry(form_frame, "Address", 4, 30)
        self.amka_entry = self.create_labeled_entry(form_frame, "AMKA", 5, 30)
        # self.allergies = self.create_textbox(form_frame, 200, 30, 6, "Enter Allergies...")

    def set_data(self, data):
        """ Update the form with patient data. """

        if "name" in data:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, data["name"])
            self.name_entry.configure(foreground="black")

        if "surname" in data:
            self.surname_entry.delete(0, tk.END)
            self.surname_entry.insert(0, data["surname"])
            self.surname_entry.configure(foreground="black")

        if "age" in data:
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, str(data["age"]))
            self.age_entry.configure(foreground="black")

        if "amka" in data:
            self.amka_entry.delete(0, tk.END)
            self.amka_entry.insert(0, data["amka"])
            self.amka_entry.configure(foreground="black")

        if "father" in data:
            self.father_entry.delete(0, tk.END)
            self.father_entry.insert(0, data["father"])
            self.father_entry.configure(foreground="black")

        if "address" in data:
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, data["address"])
            self.address_entry.configure(foreground="black")


    def reset_form(self):
        for entry, placeholder in self.entries.values():
            entry.delete(0, tk.END)

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
        return entry

    def clear_placeholder(self, widget, default_text: str) -> None:
        """Clears the placeholder text in a ttk.Entry or customtkinter.CTkTextbox when clicked."""
        if isinstance(widget, ttk.Entry):  # Handling ttk.Entry
            if widget.get() == default_text:
                widget.delete(0, tk.END)
                widget.config(foreground="black")  # Normal text color
        # elif isinstance(widget, customtkinter.CTkTextbox):  # Handling customtkinter.CTkTextbox
        #     if widget.get("1.0", "end-1c") == default_text:
        #         widget.delete("1.0", "end")
        #         widget.configure(text_color="black")  # Normal text color

    def restore_placeholder(self, widget, default_text: str) -> None:
        """Restores the placeholder text if the ttk.Entry or customtkinter.CTkTextbox is empty."""
        if isinstance(widget, ttk.Entry):  # Handling ttk.Entry
            if not widget.get().strip():
                widget.insert(0, default_text)
                widget.config(foreground="gray")  # Placeholder color
        # elif isinstance(widget, customtkinter.CTkTextbox):  # Handling customtkinter.CTkTextbox
        #     if not widget.get("1.0", "end-1c").strip():
        #         widget.insert("1.0", default_text)
        #         widget.configure(text_color="gray")  # Placeholder color