from app import App
from utils.populate import populate_database
from tkinter import ttk

if __name__ == "__main__":
    populate_database(100)  # For testing purposes
    app = App()
    label = ttk.Style()
    label.configure('.', font=('Helvetica', 12))
    app.mainloop()