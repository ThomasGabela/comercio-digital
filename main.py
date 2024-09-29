import tkinter as tk
from functions.interface import create_interface

def main():
    cart = []  # Lista temporal para guardar productos seleccionados en la compra actual
    root = tk.Tk()
    create_interface(root, cart)
    root.mainloop()

if __name__ == "__main__":
    main()

