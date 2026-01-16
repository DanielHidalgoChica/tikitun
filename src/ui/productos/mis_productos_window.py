"""
Vista de "Mis Productos" - Lista los productos del usuario actual.
Permite acceder a consultar, editar, eliminar y promocionar.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.services.productos.productos_service import get_productos_usuario
from src.db.db_app import connect


def show_mis_productos_view(parent, username: str):
    """Muestra la vista de productos del usuario en el área de contenido.
    
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
        text="📦 Mis Productos",
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(side=tk.LEFT)
    
    # Botón refrescar
    def refrescar():
        show_mis_productos_view(parent, username)
    
    tk.Button(
        header,
        text="🔄 Refrescar",
        command=refrescar
    ).pack(side=tk.RIGHT)
    
    # Cargar productos del usuario
    productos = []
    try:
        with connect() as cn:
            productos = get_productos_usuario(cn, username)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}")
    
    if not productos:
        tk.Label(
            frame,
            text="No tienes productos publicados.\n\nUsa el botón 'Publicar' para crear tu primer producto.",
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
    disponible = producto.get("disponible", 0)
    
    # Frame de la tarjeta
    card = tk.Frame(
        parent,
        bg="#f9f9f9" if disponible else "#ffebee",
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
        fg="#333" if disponible else "#999"
    ).pack(side=tk.LEFT)
    
    # Badge de promoción
    promocion = producto.get("promocion", 0)
    if promocion and promocion > 0:
        tk.Label(
            titulo_frame,
            text=f" 🔥 {promocion:.0%}",
            font=("Arial", 9),
            bg=card.cget("bg"),
            fg="orange"
        ).pack(side=tk.LEFT, padx=5)
    
    # Badge de no disponible
    if not disponible:
        tk.Label(
            titulo_frame,
            text=" (Eliminado)",
            font=("Arial", 9),
            bg=card.cget("bg"),
            fg="red"
        ).pack(side=tk.LEFT, padx=5)
    
    # Precio y categoría
    info_frame = tk.Frame(left, bg=card.cget("bg"))
    info_frame.pack(anchor="w", pady=5)
    
    precio = producto.get("precio", 0)
    tk.Label(
        info_frame,
        text=f"{precio:.2f}€",
        font=("Arial", 11, "bold"),
        bg=card.cget("bg"),
        fg="#4CAF50" if disponible else "#999"
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
    if disponible:
        btn_frame = tk.Frame(card, bg=card.cget("bg"))
        btn_frame.pack(side=tk.RIGHT)
        
        id_producto = producto.get("id_producto")
        
        def on_ver():
            from src.ui.productos.detalle_window import show_detalle_view
            show_detalle_view(content_frame, id_producto, username)
        
        def on_editar():
            from src.ui.productos.editar_window import show_editar_view
            show_editar_view(content_frame, id_producto, username)
        
        def on_promocionar():
            from src.ui.productos.promocionar_window import show_promocionar_view
            show_promocionar_view(content_frame, id_producto, username)
        
        def on_eliminar():
            from src.services.productos.productos_service import eliminar_producto
            from src.db.db_app import begin_transaction, commit, rollback
            
            if not messagebox.askyesno(
                "Confirmar",
                f"¿Eliminar '{producto.get('titulo')}'?\n\nEsta acción no se puede deshacer."
            ):
                return
            
            cn = begin_transaction()
            try:
                eliminar_producto(cn, id_producto, username)
                commit(cn)
                messagebox.showinfo("Eliminado", "Producto eliminado.")
                # Refrescar vista
                show_mis_productos_view(content_frame, username)
            except ValueError as e:
                rollback(cn)
                messagebox.showerror("Error", str(e))
            except Exception as e:
                rollback(cn)
                messagebox.showerror("Error", f"Error: {e}")
        
        tk.Button(btn_frame, text="👁", command=on_ver, width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="✏️", command=on_editar, width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🚀", command=on_promocionar, width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🗑️", command=on_eliminar, width=3, fg="red").pack(side=tk.LEFT, padx=2)
