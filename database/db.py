import csv
from tkinter import messagebox
from datetime import datetime

def load_all_products(id_product = None):
    products = []
    try:
        with open('database/productos.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if id_product == row["Product ID"]:
                    products = {
                        "id":   int(row["Product ID"]),
                        "name": row["Name"],
                        "price": float(row["Price"]),
                        "stock": int(row["Stock"]),
                        "brand": row["Brand"],        # Añadir brand
                        "description": row["Description"],  # Añadir description
                        "quantity": 1  # Mantener la cantidad por defecto
                    }
                if id_product is None:
                    products.append(row)


    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de productos no encontrado")
        return None

    if len(products) == 0:
        return None
    return products

def save_sale(id_producto, cantidad, precio_unidad):
    price_total = precio_unidad * cantidad  # Calcular el precio total
    last_id = get_last_sale_id()
    new_id = last_id + 1  # Incrementar el ID de venta

    with open('database/ventas.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_id, id_producto, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), precio_unidad, cantidad, price_total])

def update_stock(id_producto, nuevo_stock):
    products_list = load_all_products(id_producto)
    for product in products_list:
        if product["Product ID"] == str(id_producto):
            product["Stock"] = str(nuevo_stock)

    # Guardar el stock actualizado
    with open('database/productos.csv', mode='w', newline='') as file:
        fieldnames = ["Product ID", "Name", "Price", "Stock", "Brand", "Description"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products_list)

def get_last_sale_id():
    try:
        with open('database/ventas.csv', mode='r') as file:
            reader = csv.DictReader(file)
            sales = list(reader)
            if not sales:
                return 0
            return int(sales[-1]['id_venta'])
    except FileNotFoundError:
        return 0

def save_product(product_data):
    with open('database/productos.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Product ID", "Name", "Price", "Stock", "Brand", "Description"])
        writer.writerow(product_data)

def delete_product_from_db(id_producto):
    products_list = load_all_products(id_producto)
    products_list = [product for product in products_list if product["Product ID"] != str(id_producto)]

    with open('database/productos.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Product ID", "Name", "Price", "Stock", "Brand", "Description"])
        writer.writeheader()
        writer.writerows(products_list)