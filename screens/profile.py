import tkinter as tk
from tkinter import ttk
import customtkinter
import sqlite3
from tkinter import Frame

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

        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

        self.entries = {}   # Dictionary to store entry widgets

        # Create input fields
        self.create_labeled_entry(form_frame, "AMKA", "Enter AMKA number", 0, 30)
        self.create_labeled_entry(form_frame, "Name", "Enter patient name", 2, 30, inline=True, col=0)
        self.create_labeled_entry(form_frame, "Surname", "Enter patient surname", 2, 30, inline=True, col=1)
        self.create_labeled_entry(form_frame, "Father's Name", "Enter father's name", 4, 30)
        self.create_labeled_entry(form_frame, "Age", " ", 6, 30)
        self.create_labeled_entry(form_frame, "Address", "Enter patient's address", 8, 30)


        self.allergies = self.create_textbox(form_frame, 200, 30, 6, "Enter Allergies...")

        button = ttk.Button(form_frame, padding=(10, 9, 10, 7), text="Add new entry", style="Accent.TButton", command=self.add_entry) #padding aligns text in the center of button
        button.grid(column=0, columnspan=2, pady=10)

        buttonPrint = ttk.Button(form_frame, text="Print DB", command=self.print_database)
        buttonPrint.grid(column=0, columnspan=2, pady=10)

        self.allergies_visible = False  # Track visibility
        ttk.Button(form_frame, text="Toggle Allergies", command=lambda: self.toggle_text(self.allergies, 6)).grid(column=0, columnspan=2, pady=10)
        self.allergies.grid_remove() # Placed after the creation of the button because it didn't dynamically if placed before

        button1 = ttk.Button(form_frame, text="Go to Patient List",
                            command=lambda: controller.show_frame("Patients"))
        button1.grid(column=0, columnspan=2, pady=10)

    def create_labeled_entry(self, parent, label_text, placeholder_text, row, width, inline=False, col=0):
        """Creates a label and entry field. Inline fields go side by side. Non-inline fields span both columns."""
        
        # Label
        label = ttk.Label(parent, text=label_text, padding=(0, 12, 0, 0))
        label.configure(font=('Helvetica', 11))
        if inline:
            label.grid(row=row, column=col, sticky="w", padx=((15,0) if label_text == "Surname" else (0,0)))
        else:
            label.grid(row=row, column=0, columnspan=2, sticky="w")

        # Placeholder
        placeholder = tk.StringVar()
        placeholder.set(placeholder_text)

        entry = ttk.Entry(parent, textvariable=placeholder, width=width)
        if inline:
            entry.grid(row=row+1, column=col, pady=5, padx=((15,0) if col == 1 else 0), sticky="ew")
        else:
            entry.grid(row=row+1, column=0, columnspan=2, pady=5, sticky="ew")

        entry.bind("<FocusIn>", lambda event, w=entry, d=placeholder_text: self.clear_placeholder(w, d))
        entry.bind("<FocusOut>", lambda event, w=entry, d=placeholder_text: self.restore_placeholder(w, d))

        entry.configure(foreground="gray", font=('Helvetica', 10))

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
        amka: str = get_widget_value(self.entries["AMKA"][0])
        name: str = get_widget_value(self.entries["Name"][0])  
        surname: str = get_widget_value(self.entries["Surname"][0])
        father: str = get_widget_value(self.entries["Father Name"][0])
        age_input: str = get_widget_value(self.entries["Age"][0])
        address: str = get_widget_value(self.entries["Address"][0])
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

        conn = sqlite3.connect('database.db')
        curr = conn.cursor()

        curr.execute("INSERT INTO patients (amka,name,surname,father,age,address,allergies)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?)", (amka,name,surname,father,age,address,allergies))
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
        conn = sqlite3.connect('database.db')
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