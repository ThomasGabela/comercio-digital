from database.db import load_all_products, save_sale, update_stock

def add_to_cart(barcode, quantity, cart, cart_treeview, total_label):
    quantity = int(quantity)  # Leer la cantidad ingresada
    product = load_all_products(barcode)
    if product is None:
        return

    if quantity <= 0 or product["stock"] < quantity:
        return

    # Si el producto ya está en el carrito, incrementar la cantidad
    for item in cart:
        if item["id"] == product["id"]:
            item["quantity"] += quantity
            update_cart_display(cart, cart_treeview, total_label)
            return

    # Añadir nuevo producto al carrito con la cantidad correcta
    product["quantity"] = quantity
    cart.append(product)
    update_cart_display(cart, cart_treeview, total_label)

def update_cart_display(cart, cart_treeview, total_label):
    # Limpiar la tabla de la grilla
    for item in cart_treeview.get_children():
        cart_treeview.delete(item)

    # Insertar los productos en la tabla
    total_price = 0
    for item in cart:
        total_price += item['price'] * item['quantity']
        cart_treeview.insert('', 'end', values=(item['name'], item['quantity'], f"${item['price'] * item['quantity']:.2f}","X"))

    # Actualizar el total
    total_label.config(text=f"Total: ${total_price:.2f}")

def finalize_purchase(cart, cart_treeview, total_label):
    if not cart:
        return

    for item in cart:
        save_sale(item["id"], item["quantity"], item["price"])  # Registrar la venta
        update_stock(item["id"], item["quantity"])  # Reducir el stock
    cart.clear()  # Vaciar el carrito después de la compra
    update_cart_display(cart, cart_treeview, total_label)

def remove_from_cart(cart, cart_treeview, total_label): #boton no usable: general para eliminar multiples items
    selected_item = cart_treeview.selection()
    if not selected_item:
        return

    # Obtener el nombre del producto seleccionado
    item_values = cart_treeview.item(selected_item, 'values')
    product_name = item_values[0]

    # Buscar el producto en el carrito por nombre y eliminarlo
    for item in cart:
        if item['name'] == product_name:
            cart.remove(item)
            break

    # Actualizar la tabla y el total
    update_cart_display(cart, cart_treeview, total_label)

def remove_one_unit(cart, product_name, cart_treeview, total_label):
    # Buscar el producto en el carrito por nombre
    for item in cart:
        if item['name'] == product_name:
            if item['quantity'] > 1:
                item['quantity'] -= 1  # Reducir en 1 la cantidad
            else:
                cart.remove(item)  # Eliminar del carrito si la cantidad es 1
            break

    # Actualizar la tabla y el total
    update_cart_display(cart, cart_treeview, total_label)
