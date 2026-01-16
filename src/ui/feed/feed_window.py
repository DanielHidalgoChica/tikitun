import tkinter as tk
from tkinter import ttk, messagebox
from src.db.db_app import connect, begin_transaction, commit, rollback
from src.services.feed_busqueda_favs.recomendaciones_service import obtener_feed
from src.services.feed_busqueda_favs.favoritos_service import agregar_favorito
from src.services.feed_busqueda_favs.busqueda_service import buscar_productos, CATEGORIAS_DISPONIBLES


def show_feed_view(parent_frame, username="bob"):
    """
    Muestra el feed de recomendaciones en el frame principal.
    
    Funcionalidades (RF3.1, RF3.5):
    - Mostrar productos recomendados según preferencias del usuario
    - Barra de búsqueda de productos (fuzzy search)
    - Filtros por categoría
    - Ordenación por puntuación o precio
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
    
    # ==================== BARRA DE BÚSQUEDA ====================
    search_frame = tk.Frame(parent_frame)
    search_frame.pack(pady=10, padx=20, fill=tk.X)
    
    # Fila 1: Texto de búsqueda y categoría
    row1 = tk.Frame(search_frame)
    row1.pack(fill=tk.X, pady=2)
    
    tk.Label(row1, text="🔍 Buscar:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    search_var = tk.StringVar()
    search_entry = tk.Entry(row1, width=30, textvariable=search_var)
    search_entry.pack(side=tk.LEFT, padx=5)
    
    tk.Label(row1, text="Categoría:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(15, 5))
    
    categoria_var = tk.StringVar(value="(Todas)")
    categoria_combo = ttk.Combobox(
        row1, 
        textvariable=categoria_var,
        values=["(Todas)"] + CATEGORIAS_DISPONIBLES,
        state="readonly",
        width=15
    )
    categoria_combo.pack(side=tk.LEFT, padx=5)
    
    # Fila 2: Ordenación y botón buscar
    row2 = tk.Frame(search_frame)
    row2.pack(fill=tk.X, pady=5)
    
    tk.Label(row2, text="Ordenar por:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    
    orden_var = tk.StringVar(value="rating")
    
    tk.Radiobutton(row2, text="Puntuación", variable=orden_var, value="rating").pack(side=tk.LEFT, padx=3)
    tk.Radiobutton(row2, text="Precio ↑", variable=orden_var, value="precio_asc").pack(side=tk.LEFT, padx=3)
    tk.Radiobutton(row2, text="Precio ↓", variable=orden_var, value="precio_desc").pack(side=tk.LEFT, padx=3)
    
    buscar_btn = tk.Button(row2, text="🔍 Buscar", state=tk.DISABLED)
    buscar_btn.pack(side=tk.RIGHT, padx=10)
    
    volver_btn = tk.Button(
        row2, 
        text="← Volver a Recomendaciones",
        command=lambda: show_feed_view(parent_frame, username)
    )
    volver_btn.pack(side=tk.RIGHT, padx=5)
    volver_btn.pack_forget()  # Oculto inicialmente
    
    # ==================== ÁREA DE RESULTADOS ====================
    # Separador
    tk.Frame(parent_frame, height=2, bg="gray").pack(fill=tk.X, pady=10)
    
    # Label de contexto (recomendaciones o resultados de búsqueda)
    results_label = tk.Label(
        parent_frame,
        text="Productos recomendados para ti:",
        font=("Arial", 12, "bold")
    )
    results_label.pack(pady=10)
    
    # Frame scrollable para productos
    canvas = tk.Canvas(parent_frame, height=350)
    scrollbar = tk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # ==================== FUNCIONES AUXILIARES ====================
    
    def render_productos(productos):
        """Renderiza la lista de productos en el scrollable_frame."""
        # Limpiar frame
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        if not productos:
            tk.Label(
                scrollable_frame,
                text="No se encontraron productos.",
                font=("Arial", 11),
                fg="gray"
            ).pack(pady=20)
            return
        
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
            rating = prod.get('valoracion_vendedor', 0)
            
            desc_text = f"€{precio:.2f} • {categoria} • por @{vendedor}"
            if promocion and promocion > 0:
                desc_text += f" • {promocion}% DESC"
            if rating:
                desc_text += f" • ⭐{rating:.1f}"
            
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
    
    def actualizar_estado_boton(*args):
        """Habilita/deshabilita el botón Buscar según si hay texto."""
        texto = search_var.get().strip()
        if texto:
            buscar_btn.config(state=tk.NORMAL)
        else:
            buscar_btn.config(state=tk.DISABLED)
    
    def on_buscar():
        """Handler del botón Buscar."""
        texto = search_var.get().strip()
        categoria = categoria_var.get()
        orden = orden_var.get()
        
        try:
            with connect() as cn:
                productos = buscar_productos(cn, texto, categoria, orden)
            
            # Actualizar UI
            results_label.config(text=f"Resultados de búsqueda: \"{texto}\"")
            volver_btn.pack(side=tk.RIGHT, padx=5)  # Mostrar botón volver
            render_productos(productos)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(ex)}")
    
    # ==================== BINDINGS ====================
    
    # Actualizar estado del botón cuando cambia el texto
    search_var.trace_add("write", actualizar_estado_boton)
    
    # Buscar al presionar Enter
    search_entry.bind("<Return>", lambda e: on_buscar() if search_var.get().strip() else None)
    
    # Configurar comando del botón buscar
    buscar_btn.config(command=on_buscar)
    
    # ==================== CARGAR FEED INICIAL ====================
    try:
        with connect() as cn:
            productos = obtener_feed(cn, username)
        render_productos(productos)
    except Exception as ex:
        messagebox.showerror("Error", f"No se pudo cargar el feed: {str(ex)}")
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
