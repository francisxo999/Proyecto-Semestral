import tkinter as tk
from mascota.gui import Frame

def main():
    root = tk.Tk()
    root.title('VETTsafe')
    root.resizable(False, False)
    app = Frame(root)
    app.mainloop()

if __name__ == '__main__':
    main()
