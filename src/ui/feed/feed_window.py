import tkinter as tk
from tkinter import messagebox
from src.db.db_app import connect, begin_transaction, commit, rollback
from src.services.feed_busqueda_favs.recomendaciones_service import obtener_feed
from src.services.feed_busqueda_favs.favoritos_service import agregar_favorito


def show_feed_view(parent_frame, username="bob"):
    """
    Muestra el feed de recomendaciones en el frame principal.
    
    Funcionalidades futuras (RF3.1, RF3.5):
    - Mostrar productos recomendados según preferencias del usuario
    - Filtrar por categorías preferidas
    - Ordenar por grado de promoción y puntuación del vendedor
    - Barra de búsqueda de productos (fuzzy search)
    - Filtros por categoría y precio
    - Consultar detalles de cada producto
    """
    # Limpiar el frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Título
    tk.Label(
        parent_frame,
        text="📱 Feed de Recomendaciones",
        font=("Arial", 16, "bold")
    ).pack(pady=10)
    
    # Barra de búsqueda
    search_frame = tk.Frame(parent_frame)
    search_frame.pack(pady=10, padx=20, fill=tk.X)
    
    tk.Label(search_frame, text="🔍 Buscar:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    search_entry = tk.Entry(search_frame, width=40)
    search_entry.pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        search_frame,
        text="Buscar",
        state=tk.DISABLED
    ).pack(side=tk.LEFT, padx=5)
    
    tk.Button(
        search_frame,
        text="Filtros ▼",
        state=tk.DISABLED
    ).pack(side=tk.LEFT, padx=5)
    
    # Separador
    tk.Frame(parent_frame, height=2, bg="gray").pack(fill=tk.X, pady=10)
    
    # Lista de productos recomendados (placeholder)
    tk.Label(
        parent_frame,
        text="Productos recomendados para ti:",
        font=("Arial", 12, "bold")
    ).pack(pady=10)
    
    # Frame scrollable para productos
    canvas = tk.Canvas(parent_frame, height=400)
    scrollbar = tk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Obtener productos reales de la BD
    try:
        with connect() as cn:
            productos = obtener_feed(cn, username)
        
        if not productos:
            tk.Label(
                scrollable_frame,
                text="No hay productos disponibles en este momento.",
                font=("Arial", 11),
                fg="gray"
            ).pack(pady=20)
        else:
            for prod in productos:
                prod_frame = tk.Frame(scrollable_frame, relief=tk.RIDGE, borderwidth=2)
                prod_frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Información del producto
                info_frame = tk.Frame(prod_frame)
                info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5, padx=10)
                
                tk.Label(
                    info_frame,
                    text=prod.get('titulo', 'Sin título'),
                    font=("Arial", 11, "bold")
                ).pack(anchor=tk.W)
                
                precio = prod.get('precio', 0)
                categoria = prod.get('nombre_categoria', 'Sin categoría')
                vendedor = prod.get('username_vendedor', 'desconocido')
                promocion = prod.get('promocion', 0)
                
                desc_text = f"€{precio:.2f} • {categoria} • por @{vendedor}"
                if promocion and promocion > 0:
                    desc_text += f" • {promocion}% DESC"
                
                tk.Label(
                    info_frame,
                    text=desc_text,
                    font=("Arial", 9),
                    fg="gray"
                ).pack(anchor=tk.W)
                
                # Botones
                btn_frame = tk.Frame(prod_frame)
                btn_frame.pack(side=tk.RIGHT, padx=10)
                
                tk.Button(
                    btn_frame,
                    text="Ver más",
                    state=tk.DISABLED
                ).pack(side=tk.LEFT, padx=3)
                
                # Handler para agregar a favoritos
                def crear_agregar_favorito_handler(id_prod, user):
                    """Factory para crear handler del botón Agregar Favorito."""
                    def on_agregar_favorito():
                        cn = None
                        try:
                            cn = begin_transaction()
                            agregar_favorito(cn, user, id_prod)
                            commit(cn)
                            messagebox.showinfo("OK", "Producto añadido a favoritos")
                        except Exception as ex:
                            if cn:
                                rollback(cn)
                            messagebox.showerror("Error", str(ex))
                    return on_agregar_favorito
                
                tk.Button(
                    btn_frame,
                    text="♥ Favorito",
                    fg="red",
                    command=crear_agregar_favorito_handler(prod.get('id_producto'), username)
                ).pack(side=tk.LEFT, padx=3)
    
    except Exception as ex:
        messagebox.showerror("Error", f"No se pudo cargar el feed: {str(ex)}")
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
