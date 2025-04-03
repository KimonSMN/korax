import tkinter as tk
from tkinter import ttk
import sqlite3
import customtkinter

class EditPatient(tk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Edit Patient", font=('Helvetica', 18))
        label.pack(pady=10)

        # Force UI update to fix scrolling
        self.update_idletasks()

        self.old_amka = None

        form_frame = ttk.Frame(self)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

        self.entries = {}   # Dictionary to store entry widgets
#test
        # Create input fields
        self.name_entry = self.create_labeled_entry(form_frame, "Name", 0, 30)
        self.surname_entry = self.create_labeled_entry(form_frame, "Surname", 1, 30)
        self.father_entry = self.create_labeled_entry(form_frame, "Father Name", 2, 30)
        self.age_entry = self.create_labeled_entry(form_frame, "Age", 3, 30)
        self.address_entry = self.create_labeled_entry(form_frame, "Address", 4, 30)
        self.amka_entry = self.create_labeled_entry(form_frame, "AMKA", 5, 30)
        self.allergies_entry = self.create_textbox(form_frame, 200, 30, 6, "Enter Allergies...")
        # self.medication_entry = self.create_textbox(form_frame, 200, 30, 7, "Enter Medication...")

        editButton = ttk.Button(form_frame, padding=(10, 9, 10, 7), style="Accent.TButton", text="Update Patient Info",
                             command=self.update_entry)
        editButton.grid(column=0, columnspan=2, pady=10)

        # Navigation button
        button1 = ttk.Button(form_frame, text="Go to Patient List",
                             command=lambda: controller.show_frame("Patients"))
        button1.grid(column=0, columnspan=2, pady=10)


    def set_data(self, data):
        """ Update the form with patient data. """

        self.old_amka = data.get("amka")

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

        if "allergies" in data:
            print(data["allergies"])
            self.allergies_entry.delete('1.0', tk.END)
            self.allergies_entry.insert('1.0', data["allergies"])
            self.allergies_entry.configure(text_color="black")

    def update_entry(self) -> None:
        def get_widget_value(widget):
            if isinstance(widget, ttk.Entry):
                return widget.get().strip()
            elif isinstance(widget, customtkinter.CTkTextbox):
                return widget.get("1.0", "end-1c").strip()
            return ""

        amka = get_widget_value(self.entries["AMKA"][0])
        name = get_widget_value(self.entries["Name"][0])
        surname = get_widget_value(self.entries["Surname"][0])
        father = get_widget_value(self.entries["Father Name"][0])
        age = get_widget_value(self.entries["Age"][0])
        address = get_widget_value(self.entries["Address"][0])
        allergies = get_widget_value(self.entries["Enter Allergies..."][0])

        if not self.old_amka:
            print("Error: old_amka is not set. Cannot update.")
            return

        conn = sqlite3.connect("database.db")
        curr = conn.cursor()
        curr.execute("""
            UPDATE patients 
            SET name = ?, surname = ?, father = ?, age = ?, amka = ?, address = ?, allergies = ? 
            WHERE amka = ?
        """, (name, surname, father, age, amka, address, allergies, self.old_amka))
        conn.commit()
        conn.close()

        print(f"✅ Patient with AMKA {self.old_amka} updated.")


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


    def create_textbox(self, parent: tk.Frame, height: int, width: int, row: int, label_text: str):
        text = customtkinter.CTkTextbox(parent, height = height, width = width, 
                                        fg_color="white", border_width=1 ,border_color="lightgray", text_color="gray", font=('Helvetica', 12))
        text.insert("1.0", label_text)
        text.grid(row=row, column=1, columnspan=2, pady=5, sticky="nsew")

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