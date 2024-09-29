# Comercio Digital - Prototipo Open Source

Este es un **prototipo de digitalización de comercio** desarrollado en Python. El objetivo de este proyecto es ofrecer una solución simple y escalable para gestionar productos, inventarios y ventas en un comercio minorista. Está diseñado como un sistema local que utiliza archivos CSV como base de datos, y una interfaz gráfica sencilla con **Tkinter**.

## Características del Prototipo

1. **Gestión de Inventario**:
   - Ver todos los productos disponibles en el inventario.
   - Añadir nuevos productos con campos como nombre, precio, stock, marca y descripción.
   - Modificar el stock de productos existentes.
   - Eliminar productos del inventario.

2. **Sistema de Ventas**:
   - Registrar ventas con productos del inventario.
   - Actualización automática del stock después de cada venta.
   - Historial de ventas accesible para revisión.

3. **Interfaz Gráfica (Tkinter)**:
   - Interfaz simple para usuarios no técnicos.
   - Formulario para agregar, modificar o eliminar productos.

4. **Estructura Modular**:
   - Código segmentado en diferentes archivos para facilitar el mantenimiento y futuras mejoras.
   - Soporte para la gestión de productos a través de archivos CSV, con la posibilidad de migrar a una base de datos más compleja en el futuro.

## Archivos del Proyecto

- **main.py**: Archivo principal que ejecuta la aplicación.
- **/database**: Carpeta que contiene los archivos CSV (productos.csv, ventas.csv).
- **/functions**: Lógica relacionada con el carrito de compras y la interfaz gráfica.
- **/manage_inventory.py**: Funciones para agregar, modificar y eliminar productos en el inventario.
- **/db.py**: Archivo intermedio que maneja la interacción con los archivos CSV.

## Próximos Pasos para Convertirlo en un Producto Completo

Este proyecto aún es un **prototipo** y aquí hay algunas mejoras que podrían implementarse para convertirlo en una solución más robusta:

1. **Migración a una Base de Datos Real**:
   - Migrar los archivos CSV a una base de datos como SQLite, MySQL o PostgreSQL para mejor escalabilidad y seguridad.

2. **Mejoras en la Interfaz de Usuario**:
   - Mejorar el diseño de la interfaz gráfica para hacerlo más intuitivo y fácil de usar.
   - Añadir soporte para múltiples idiomas.
   - Incluir más opciones visuales y reportes gráficos en la sección de ventas e inventarios.

3. **Soporte para Facturación**:
   - Implementar un sistema de impresión de facturas al completar una venta.
   - Añadir opciones de pago (efectivo, tarjeta, etc.).

4. **Manejo de Usuarios**:
   - Añadir soporte para múltiples usuarios y roles (administrador, vendedor, etc.).
   - Control de acceso basado en permisos.

5. **Sistema de Notificaciones**:
   - Notificaciones automáticas para alertar sobre bajo stock o productos agotados.
   - Reportes automáticos de ventas por correo electrónico.

## Requisitos

- **Python 3.x**
- Bibliotecas estándar de Python como `csv`, `tkinter`.