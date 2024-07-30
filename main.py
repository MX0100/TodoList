import tkinter as tk
from views.main_view import ToDoApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("750x500")
    root.title('Secure TodoList')
    app = ToDoApp(root)
    root.mainloop()

