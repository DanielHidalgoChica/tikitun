"""
Vista de productos de otro usuario - Lista los productos de un usuario que no es el actual.
Permite ver el detalle de productos y comprarlos, pero no editarlos.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.services.productos.productos_service import get_productos_usuario
from src.db.db_app import connect, begin_transaction, commit, rollback
from src.services.feed_busqueda_favs.favoritos_service import agregar_favorito

from io import BytesIO

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def show_productos_usuario_view(parent, current_user: str, profile_user: str):
    """Muestra la vista de productos de otro usuario (solo lectura).
    
    Args:
        parent: Frame contenedor (content_frame)
        current_user: Usuario actualmente logueado
        profile_user: Usuario del que se muestran los productos
    """
    # Limpiar contenido anterior
    for widget in parent.winfo_children():
        widget.destroy()
    
    # Frame principal
    frame = tk.Frame(parent, bg="white", padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Header con botón volver
    header = tk.Frame(frame, bg="white")
    header.pack(fill=tk.X, pady=(0, 20))
    
    def volver_a_perfil():
        from src.ui.perfil.perfil_window import show_perfil_view
        show_perfil_view(parent, current_user, profile_user)
    
    tk.Button(
        header,
        text="← Volver al perfil",
        command=volver_a_perfil,
        bg="#9E9E9E",
        fg="white",
        font=("Arial", 10),
        padx=10,
        pady=5
    ).pack(side=tk.LEFT)
    
    tk.Label(
        header,
        text=f"📦 Productos de @{profile_user}",
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(side=tk.LEFT, padx=20)
    
    # Botón refrescar
    def refrescar():
        show_productos_usuario_view(parent, current_user, profile_user)
    
    tk.Button(
        header,
        text="🔄 Refrescar",
        command=refrescar
    ).pack(side=tk.RIGHT)
    
    # Cargar productos del usuario
    productos = []
    try:
        with connect() as cn:
            productos = get_productos_usuario(cn, profile_user)
            # Filtrar solo productos disponibles
            productos = [p for p in productos if p.get("disponible", 0)]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}")
    
    if not productos:
        tk.Label(
            frame,
            text=f"@{profile_user} no tiene productos disponibles.",
            font=("Arial", 12),
            bg="white",
            fg="gray"
        ).pack(pady=50)
        return
    
    # Contador de productos
    tk.Label(
        frame,
        text=f"{len(productos)} producto(s) disponible(s)",
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
        crear_tarjeta_producto_readonly(scrollable_frame, producto, current_user, parent)


def crear_tarjeta_producto_readonly(parent, producto: dict, current_user: str, content_frame):
    """Crea una tarjeta visual para un producto (solo lectura, con opción de ver/comprar).
    
    Args:
        parent: Frame padre
        producto: Dict con datos del producto
        current_user: Usuario actualmente logueado
        content_frame: Frame de contenido principal
    """
    # Frame de la tarjeta
    card = tk.Frame(
        parent,
        bg="#f9f9f9",
        relief=tk.RAISED,
        borderwidth=1,
        padx=15,
        pady=10
    )
    card.pack(fill=tk.X, pady=5, padx=5)
    
    # Imagen del producto (si existe)
    imagen_data = producto.get('imagen')
    if imagen_data and PIL_AVAILABLE:
        try:
            image = Image.open(BytesIO(imagen_data))
            image.thumbnail((80, 80))
            photo = ImageTk.PhotoImage(image)
            
            img_label = tk.Label(card, image=photo, bg=card.cget("bg"))
            img_label.image = photo
            img_label.pack(side=tk.LEFT, padx=(0, 10))
        except Exception:
            tk.Label(
                card,
                text="🖼️",
                font=("Arial", 24),
                fg="gray",
                bg=card.cget("bg"),
                width=3,
                height=2
            ).pack(side=tk.LEFT, padx=(0, 10))
    else:
        tk.Label(
            card,
            text="🖼️",
            font=("Arial", 24),
            fg="gray",
            bg=card.cget("bg"),
            width=3,
            height=2
        ).pack(side=tk.LEFT, padx=(0, 10))
    
    # Contenido central
    center = tk.Frame(card, bg=card.cget("bg"))
    center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Título
    titulo_frame = tk.Frame(center, bg=card.cget("bg"))
    titulo_frame.pack(anchor="w")
    
    tk.Label(
        titulo_frame,
        text=producto.get("titulo", "Sin título"),
        font=("Arial", 12, "bold"),
        bg=card.cget("bg"),
        fg="#333"
    ).pack(side=tk.LEFT)
    
    # Badge de promoción
    promocion = producto.get("promocion", 0)
    if promocion and promocion > 0:
        tk.Label(
            titulo_frame,
            text=f" 🔥 {promocion:.0%} OFF",
            font=("Arial", 9),
            bg=card.cget("bg"),
            fg="orange"
        ).pack(side=tk.LEFT, padx=5)
    
    # Precio y categoría
    info_frame = tk.Frame(center, bg=card.cget("bg"))
    info_frame.pack(anchor="w", pady=5)
    
    precio = producto.get("precio", 0)
    tk.Label(
        info_frame,
        text=f"{precio:.2f}€",
        font=("Arial", 11, "bold"),
        bg=card.cget("bg"),
        fg="#4CAF50"
    ).pack(side=tk.LEFT)
    
    tk.Label(
        info_frame,
        text=f"  •  {producto.get('nombre_categoria', 'Sin categoría')}",
        font=("Arial", 10),
        bg=card.cget("bg"),
        fg="gray"
    ).pack(side=tk.LEFT)
    
    # Valoración del vendedor
    rating = producto.get('valoracion_vendedor', 0)
    if rating:
        tk.Label(
            info_frame,
            text=f"  •  ⭐{rating:.1f}",
            font=("Arial", 10),
            bg=card.cget("bg"),
            fg="gray"
        ).pack(side=tk.LEFT)
    
    # Botones
    btn_frame = tk.Frame(card, bg=card.cget("bg"))
    btn_frame.pack(side=tk.RIGHT, padx=10)
    
    id_producto = producto.get("id_producto")
    profile_user = producto.get("username")
    
    def on_ver_mas():
        from src.ui.productos.detalle_window import show_detalle_view
        show_detalle_view(content_frame, id_producto, current_user, origen="perfil_usuario", profile_user=profile_user)
    
    tk.Button(
        btn_frame,
        text="Ver más",
        command=on_ver_mas,
        bg="#2196F3",
        fg="white",
        font=("Arial", 10),
        padx=10
    ).pack(side=tk.LEFT, padx=3, pady=2)
    
    # Botón agregar a favoritos
    def on_agregar_favorito():
        cn = None
        try:
            cn = begin_transaction()
            agregar_favorito(cn, current_user, id_producto)
            commit(cn)
            messagebox.showinfo("OK", "Producto añadido a favoritos")
        except Exception as ex:
            if cn:
                rollback(cn)
            messagebox.showerror("Error", str(ex))
    
    tk.Button(
        btn_frame,
        text="♥ Favorito",
        command=on_agregar_favorito,
        fg="red",
        font=("Arial", 10),
        padx=10
    ).pack(side=tk.LEFT, padx=3, pady=2)
