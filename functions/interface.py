import tkinter as tk
import csv
from tkinter import messagebox, ttk, Toplevel
from database.db import load_all_products, save_product, update_stock
from functions.operations import (
    add_to_cart,
    finalize_purchase,
    update_cart_display,
    remove_one_unit,
)
from functions.manage_inventory import manage_inventory

def create_interface(root, cart):
    # Crear la interfaz gráfica
    root.title("Sistema de Ventas")

    # Botón para gestionar el inventario
    inventory_button = tk.Button(root, text="Gestionar Inventario", command=manage_inventory)
    inventory_button.pack(pady=5)

    # Etiqueta y campo de entrada para el código de barras
    tk.Label(root, text="Escanear Código de Barras:").pack(pady=5)
    barcode_entry = tk.Entry(root, width=40)
    barcode_entry.pack(pady=5)
    barcode_entry.bind("<Return>", lambda event: add_to_cart(barcode_entry.get(), quantity_entry.get(), cart, cart_treeview, total_label))

    # Etiqueta y campo de entrada para la cantidad
    tk.Label(root, text="Cantidad:").pack(pady=5)
    quantity_entry = tk.Entry(root, width=10)
    quantity_entry.insert(0, "1")  # Valor por defecto de cantidad 1
    quantity_entry.pack(pady=5)

    # Botón para añadir el producto manualmente
    add_button = tk.Button(root, text="Añadir al Carrito", command=lambda: add_to_cart(barcode_entry.get(), quantity_entry.get(), cart, cart_treeview, total_label))
    add_button.pack(pady=5)

    # Botón para mostrar el historial de ventas
    sales_history_button = tk.Button(root, text="Historial de Ventas", command=lambda: show_sales_history())
    sales_history_button.pack(pady=5)

    # Crear la tabla para mostrar los productos en el carrito
    columns = ('Nombre', 'Cantidad', 'Precio', 'Eliminar')
    cart_treeview = ttk.Treeview(root, columns=columns, show='headings', height=10)

    # Definir encabezados de la grilla
    cart_treeview.heading('Nombre', text='Nombre')
    cart_treeview.heading('Cantidad', text='Cantidad')
    cart_treeview.heading('Precio', text='Precio')
    cart_treeview.heading('Eliminar', text='X')  # Nueva columna para eliminar

    # Definir tamaño de columnas
    cart_treeview.column('Nombre', width=200)
    cart_treeview.column('Cantidad', width=80)
    cart_treeview.column('Precio', width=100)
    cart_treeview.column('Eliminar', width=12)

    # Empaquetar la grilla en la interfaz
    cart_treeview.pack(pady=10)

    # Evento para manejar la eliminación de una unidad al hacer clic en la columna "Eliminar"
    cart_treeview.bind('<ButtonRelease-1>', lambda event: handle_remove_click(event, cart, cart_treeview, total_label))

    # # Botón para eliminar el producto seleccionado
    # remove_button = tk.Button(root, text="Eliminar Producto", command=lambda: remove_from_cart(cart, cart_treeview, total_label))
    # remove_button.pack(pady=5)

    # Etiqueta para mostrar el total
    total_label = tk.Label(root, text="Total: $0.00", font=("Arial", 14))
    total_label.pack(pady=10)

    # Botón para finalizar la compra
    finalize_button = tk.Button(root, text="Finalizar Compra", command=lambda: finalize_purchase(cart, cart_treeview, total_label))
    finalize_button.pack(pady=10)

def handle_remove_click(event, cart, cart_treeview, total_label):
    selected_item = cart_treeview.selection()
    column = cart_treeview.identify_column(event.x)
    if not selected_item or column != '#4':  # #4 es la columna "Eliminar"
        return

    # Obtener el nombre del producto seleccionado
    item_values = cart_treeview.item(selected_item, 'values')
    product_name = item_values[0]

    # Eliminar una unidad del producto
    remove_one_unit(cart, product_name, cart_treeview, total_label)

def show_sales_history():
    # Crear una nueva ventana (popup)
    sales_window = Toplevel()
    sales_window.title("Historial de Ventas")

    # Crear la tabla para mostrar las ventas
    columns = ('ID Venta', 'ID Producto', 'Nombre', 'Fecha', 'Precio Unitario', 'Cantidad', 'Precio Total')
    sales_treeview = ttk.Treeview(sales_window, columns=columns, show='headings', height=10)

# Definir encabezados de la grilla
    sales_treeview.heading('ID Venta', text='ID Venta')
    sales_treeview.heading('ID Producto', text='ID Producto')
    sales_treeview.heading('Nombre', text='Nombre')
    sales_treeview.heading('Fecha', text='Fecha')
    sales_treeview.heading('Precio Unitario', text='Precio Unitario')
    sales_treeview.heading('Cantidad', text='Cantidad')
    sales_treeview.heading('Precio Total', text='Precio Total')

    # Definir tamaño de columnas
    sales_treeview.column('ID Venta', width=80)
    sales_treeview.column('ID Producto', width=100)
    sales_treeview.column('Nombre', width=200)
    sales_treeview.column('Fecha', width=150)
    sales_treeview.column('Precio Unitario', width=100)
    sales_treeview.column('Cantidad', width=80)
    sales_treeview.column('Precio Total', width=100)

    # Empaquetar la tabla
    sales_treeview.pack(pady=10)

    # Cargar las ventas desde el archivo CSV y hacer merge con productos.csv
    try:
        with open('database/ventas.csv', mode='r') as ventas_file, open('database/productos.csv', mode='r') as productos_file:
            ventas_reader = csv.DictReader(ventas_file)
            productos_reader = csv.DictReader(productos_file)
            productos = {row["Product ID"]: row["Name"] for row in productos_reader}

            for row in ventas_reader:
                nombre = productos.get(row['id_producto'], 'Desconocido')
                sales_treeview.insert('', 'end', values=(
                    row['id_venta'],
                    row['id_producto'],
                    nombre,
                    row['fecha'],
                    f"${float(row['precio_unidad']):.2f}",
                    row['cantidad'],
                    f"${float(row['price_total']):.2f}"
                ))
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de ventas o productos no encontrado.")

    # Botón para eliminar ventas seleccionadas
    delete_button = tk.Button(sales_window, text="Eliminar Seleccionadas", command=lambda: delete_selected_sales(sales_treeview, sales_window))
    delete_button.pack(pady=5)

def delete_selected_sales(sales_treeview, sales_window):
    selected_items = sales_treeview.selection()
    if not selected_items:
        messagebox.showinfo("Info", "No hay ventas seleccionadas para eliminar.")
        return

    # Contar cuántas ventas serán eliminadas
    count = len(selected_items)
    confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar {count} venta(s) del historial?")

    if not confirm:
        return

    # Lista para almacenar los IDs de ventas a eliminar
    sales_to_delete = []
    for item in selected_items:
        sale = sales_treeview.item(item, 'values')
        sales_to_delete.append(sale)

    # Eliminar las ventas del archivo CSV y reincorporar el stock
    from database.db import update_stock
    updated_sales = []

    try:
        with open('database/ventas.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Si la venta no está en sales_to_delete, la mantenemos
                if not any(row['id_venta'] == sale[0] for sale in sales_to_delete):
                    updated_sales.append(row)
                else:
                    # Reincorporar el stock
                    update_stock(row['id_producto'], -int(row['cantidad']))
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de ventas no encontrado.")
        return

    # Escribir las ventas actualizadas en el CSV
    with open('database/ventas.csv', mode='w', newline='') as file:
        fieldnames = ['id_venta', 'id_producto', 'fecha', 'precio_unidad', 'cantidad', 'price_total']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_sales)

    # Actualizar la interfaz
    for item in selected_items:
        sales_treeview.delete(item)

    messagebox.showinfo("Info", f"{count} venta(s) eliminada(s) exitosamente.")
