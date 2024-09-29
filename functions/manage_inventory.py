from database.db import save_product, update_stock, delete_product_from_db, load_all_products
from tkinter import messagebox, ttk, Toplevel
import tkinter as tk

def manage_inventory():
    inventory_window = Toplevel()
    inventory_window.title("Inventario")

    # Crear la tabla para mostrar el inventario
    columns = ('ID Producto', 'Nombre', 'Precio', 'Stock', 'Marca', 'Descripción')
    inventory_treeview = ttk.Treeview(inventory_window, columns=columns, show='headings', height=10)

    # Definir encabezados de la grilla
    inventory_treeview.heading('ID Producto', text='ID Producto')
    inventory_treeview.heading('Nombre', text='Nombre')
    inventory_treeview.heading('Precio', text='Precio')
    inventory_treeview.heading('Stock', text='Stock')
    inventory_treeview.heading('Marca', text='Marca')
    inventory_treeview.heading('Descripción', text='Descripción')

    # Empaquetar la tabla
    inventory_treeview.pack(pady=10)

    # Cargar el inventario
    products = load_all_products()
    for product in products:
        inventory_treeview.insert('', 'end', values=(
            product['Product ID'], product['Name'], product['Price'], product['Stock'], product['Brand'], product['Description']
        ))

    # Botón para añadir un nuevo producto
    add_button = tk.Button(inventory_window, text="Añadir Producto", command=lambda: add_product(inventory_treeview))
    add_button.pack(pady=5)

    # Botón para modificar stock
    modify_button = tk.Button(inventory_window, text="Modificar Stock", command=lambda: modify_stock(inventory_treeview))
    modify_button.pack(pady=5)

    # Botón para eliminar producto
    delete_button = tk.Button(inventory_window, text="Eliminar Producto", command=lambda: delete_product(inventory_treeview))
    delete_button.pack(pady=5)

def add_product(inventory_treeview):
    add_window = Toplevel()
    add_window.title("Añadir Producto")

    # Formulario para ingresar los datos del nuevo producto
    product_id_entry = tk.Entry(add_window)
    product_id_entry.pack()

    name_entry = tk.Entry(add_window)
    name_entry.pack()

    # Otros campos: precio, stock, marca, descripción...

    # Botón para guardar el nuevo producto
    save_button = tk.Button(add_window, text="Guardar", command=lambda: save_new_product(
        product_id_entry.get(), name_entry.get(), inventory_treeview, add_window))
    save_button.pack()

def save_new_product(product_id, name, inventory_treeview, add_window):
    product_data = {
        "Product ID": product_id,
        "Name": name,
        # Completar con los otros campos
    }
    save_product(product_data)  # Llamar a manage_inventory.py
    inventory_treeview.insert('', 'end', values=(product_id, name))  # Actualizar la tabla
    add_window.destroy()  # Cerrar la ventana

def modify_stock(inventory_treeview):
    selected_item = inventory_treeview.selection()
    if not selected_item:
        return

    # Obtener el ID del producto seleccionado
    item = inventory_treeview.item(selected_item, 'values')
    product_id = item[0]

    # Ventana para ingresar el nuevo stock
    stock_window = Toplevel()
    stock_window.title("Modificar Stock")

    new_stock_entry = tk.Entry(stock_window)
    new_stock_entry.pack()

    save_button = tk.Button(stock_window, text="Guardar", command=lambda: save_modified_stock(
        product_id, new_stock_entry.get(), inventory_treeview, stock_window))
    save_button.pack()

def save_modified_stock(product_id, new_stock, inventory_treeview, stock_window):
    if int(new_stock) < 0:
        raise ValueError("El stock no puede ser negativo.")
    update_stock(product_id, new_stock)

    # Actualizar el inventario en la vista
    for item in inventory_treeview.get_children():
        values = inventory_treeview.item(item, 'values')
        if values[0] == product_id:
            inventory_treeview.item(item, values=(product_id, values[1], values[2], new_stock))
    stock_window.destroy()

def delete_product(inventory_treeview):
    selected_item = inventory_treeview.selection()
    if not selected_item:
        return

    item = inventory_treeview.item(selected_item, 'values')
    product_id = item[0]

    confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar el producto {product_id}?")
    if confirm:
        delete_product_from_db(product_id)
        inventory_treeview.delete(selected_item)  # Eliminar de la vista
