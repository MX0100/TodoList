import tkinter as tk
from views.main_view import ToDoApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x500")
    app = ToDoApp(root)
    root.mainloop()

