"""
Vista de "Productos comprados" - Lista los productos comprados por el usuario actual.
Permite confirmar la recepción de productos y puntuar las ventas.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.services.ventas.ventas_service import obtener_productos_comprados, obtener_ventas_usuario
from src.db.db_app import connect


def show_productos_comprados_view(parent, username: str):
    """Muestra la vista de productos comprados del usuario en el área de contenido.
    
    Args:
        parent: Frame contenedor (content_frame)
        username: Usuario actual
    """
    # Limpiar contenido anterior
    for widget in parent.winfo_children():
        widget.destroy()
    
    # Frame principal
    frame = tk.Frame(parent, bg="white", padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Título
    header = tk.Frame(frame, bg="white")
    header.pack(fill=tk.X, pady=(0, 20))
    
    tk.Label(
        header,
        text="📦 Productos comprados",
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(side=tk.LEFT)
    
    # Botón refrescar
    def refrescar():
        show_productos_comprados_view(parent, username)
    
    tk.Button(
        header,
        text="🔄 Refrescar",
        command=refrescar
    ).pack(side=tk.RIGHT)
    
    # Cargar productos del usuario
    productos = []
    try:
        with connect() as cn:
            productos = obtener_productos_comprados(cn, username)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}")
    
    if not productos:
        tk.Label(
            frame,
            text="No tienes productos comprados.",
            font=("Arial", 12),
            bg="white",
            fg="gray"
        ).pack(pady=50)
        return
    
    # Lista de productos
    tk.Label(
        frame,
        text=f"{len(productos)} producto(s)",
        font=("Arial", 10),
        bg="white",
        fg="gray"
    ).pack(anchor="w", pady=(0, 10))
    
    # Contenedor con scroll
    canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Mostrar cada producto como una tarjeta
    for producto in productos:
        crear_tarjeta_producto(scrollable_frame, producto, username, parent)




def crear_tarjeta_producto(parent, producto: dict, username: str, content_frame):
    """Crea una tarjeta visual para un producto.
    
    Args:
        parent: Frame padre
        producto: Dict con datos del producto
        username: Usuario actual
        content_frame: Frame de contenido principal (para refrescar)
    """
    venta = None

    try:
        with connect() as cn:
            ventas = obtener_ventas_usuario(cn, username)
            id_producto = producto["id_producto"]
            venta = next((v for v in ventas if v["id_producto"] == id_producto), None)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}")
    
    if not venta:
        messagebox.showerror(
            "Error",
            f"No se encontró información de la venta para el producto {id_producto}"
        )
        return

    completada = venta["recepcion_confirmada"]
    # Frame de la tarjeta
    card = tk.Frame(
        parent,
        bg="#f9f9f9" if completada==0 else "#ffebee",
        relief=tk.RAISED,
        borderwidth=1,
        padx=15,
        pady=10
    )
    card.pack(fill=tk.X, pady=5, padx=5)
    
    # Contenido izquierdo
    left = tk.Frame(card, bg=card.cget("bg"))
    left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Título
    titulo_frame = tk.Frame(left, bg=card.cget("bg"))
    titulo_frame.pack(anchor="w")
    
    tk.Label(
        titulo_frame,
        text=producto.get("titulo", "Sin título"),
        font=("Arial", 12, "bold"),
        bg=card.cget("bg"),
        fg="#333" if completada==0 else "#999"
    ).pack(side=tk.LEFT)
    
    # Badge de no disponible
    if completada==1:
        tk.Label(
            titulo_frame,
            text=" (Venta completada)",
            font=("Arial", 9),
            bg=card.cget("bg"),
            fg="red"
        ).pack(side=tk.LEFT, padx=5)
    
    # Precio y categoría
    info_frame = tk.Frame(left, bg=card.cget("bg"))
    info_frame.pack(anchor="w", pady=5)
    
    precio = venta['precio_final']
    tk.Label(
        info_frame,
        text=f"{precio:.2f}€",
        font=("Arial", 11, "bold"),
        bg=card.cget("bg"),
        fg="#4CAF50" if completada==0 else "#999"
    ).pack(side=tk.LEFT)
    
    tk.Label(
        info_frame,
        text=f"  •  {producto.get('nombre_categoria', 'Sin categoría')}",
        font=("Arial", 10),
        bg=card.cget("bg"),
        fg="gray"
    ).pack(side=tk.LEFT)
    
    tk.Label(
        info_frame,
        text=f"  •  ID: {producto.get('id_producto')}",
        font=("Arial", 9),
        bg=card.cget("bg"),
        fg="gray"
    ).pack(side=tk.LEFT)
    
    # Botones (solo si disponible)
    if completada==0:
        btn_frame = tk.Frame(card, bg=card.cget("bg"))
        btn_frame.pack(side=tk.RIGHT)
        
        id_producto = producto.get("id_producto")
        
        def on_confirmar_venta():
            from src.ui.productos.confirmar_venta_window import show_confirmar_venta_view
            show_confirmar_venta_view(content_frame, id_producto, username)
        
        tk.Button(btn_frame, text="👁", command=on_confirmar_venta, width=3).pack(side=tk.LEFT, padx=2)
