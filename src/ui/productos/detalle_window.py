"""
Ventana de detalle de producto (RF2.4).
Muestra información completa del producto y permite acciones según el usuario.
"""
import tkinter as tk
from tkinter import messagebox
from src.db.db_app import connect
from io import BytesIO

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def show_detalle_producto(parent, id_producto: int, username_actual: str):
    """Abre una ventana con el detalle completo de un producto.
    
    Args:
        parent: Ventana padre
        id_producto: ID del producto a mostrar
        username_actual: Usuario que está viendo el producto
    """
    from src.services.productos.productos_service import consultar_producto
    
    win = tk.Toplevel(parent)
    win.title("Detalle de Producto")
    win.geometry("600x650")
    win.resizable(False, False)
    
    # Cargar datos del producto
    producto = None
    try:
        with connect() as cn:
            producto = consultar_producto(cn, id_producto)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        win.destroy()
        return
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el producto: {e}")
        win.destroy()
        return
    
    if not producto:
        messagebox.showerror("Error", "Producto no encontrado.")
        win.destroy()
        return
    
    # Verificar si el usuario actual es el vendedor
    es_vendedor = producto.get("username_vendedor") == username_actual
    
    # --- Contenido ---
    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Imagen del producto (si existe)
    imagen_data = producto.get("imagen")
    if imagen_data and PIL_AVAILABLE:
        try:
            # Convertir bytes a imagen
            image = Image.open(BytesIO(imagen_data))
            # Redimensionar manteniendo aspecto
            image.thumbnail((250, 250))
            photo = ImageTk.PhotoImage(image)
            
            img_label = tk.Label(frame, image=photo)
            img_label.image = photo  # Mantener referencia
            img_label.pack(anchor="center", pady=(0, 15))
        except Exception as e:
            # Si hay error con la imagen, mostrar placeholder
            tk.Label(
                frame,
                text="🖼️ Imagen no disponible",
                font=("Arial", 10),
                fg="gray",
                bg="#f0f0f0",
                width=30,
                height=5
            ).pack(anchor="center", pady=(0, 15))
    elif imagen_data and not PIL_AVAILABLE:
        tk.Label(
            frame,
            text="📷 Imagen disponible\n(instala Pillow para verla)",
            font=("Arial", 9),
            fg="gray",
            bg="#f0f0f0",
            width=30,
            height=3
        ).pack(anchor="center", pady=(0, 15))
    
    # Título
    tk.Label(
        frame, 
        text=producto.get("titulo", "Sin título"),
        font=("Arial", 16, "bold"),
        wraplength=500
    ).pack(anchor="w", pady=(0, 10))
    
    # Precio
    precio = producto.get("precio", 0)
    tk.Label(
        frame,
        text=f"{precio:.2f} €",
        font=("Arial", 20, "bold"),
        fg="#4CAF50"
    ).pack(anchor="w", pady=(0, 10))
    
    # Categoría
    categoria_frame = tk.Frame(frame)
    categoria_frame.pack(anchor="w", pady=(0, 10))
    tk.Label(categoria_frame, text="Categoría:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
    tk.Label(
        categoria_frame, 
        text=producto.get("nombre_categoria", "Sin categoría"),
        font=("Arial", 10),
        fg="gray"
    ).pack(side=tk.LEFT, padx=5)
    
    # Descripción
    tk.Label(frame, text="Descripción", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
    descripcion = producto.get("descripcion", "Sin descripción")
    if not descripcion.strip():
        descripcion = "Sin descripción"
    
    desc_text = tk.Text(frame, height=4, width=60, wrap=tk.WORD, state=tk.NORMAL)
    desc_text.insert("1.0", descripcion)
    desc_text.config(state=tk.DISABLED, bg="#f5f5f5")
    desc_text.pack(anchor="w", pady=(0, 10))
    
    # Información del vendedor
    vendedor_frame = tk.Frame(frame, bg="#f0f0f0", padx=10, pady=10)
    vendedor_frame.pack(fill=tk.X, pady=10)
    
    tk.Label(
        vendedor_frame, 
        text="Vendedor",
        font=("Arial", 10, "bold"),
        bg="#f0f0f0"
    ).pack(anchor="w")
    
    vendedor_info = tk.Frame(vendedor_frame, bg="#f0f0f0")
    vendedor_info.pack(anchor="w")
    
    tk.Label(
        vendedor_info,
        text=f"@{producto.get('username_vendedor', 'desconocido')}",
        font=("Arial", 11),
        fg="blue",
        bg="#f0f0f0"
    ).pack(side=tk.LEFT)
    
    valoracion = producto.get("valoracion_vendedor")
    if valoracion is not None and valoracion > 0:
        tk.Label(
            vendedor_info,
            text=f"  ⭐ {valoracion:.1f}",
            font=("Arial", 10),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT)
    
    # Promoción (si tiene)
    promocion = producto.get("promocion", 0)
    if promocion and promocion > 0:
        tk.Label(
            frame,
            text=f"🔥 Promocionado ({promocion:.0%})",
            font=("Arial", 10),
            fg="orange"
        ).pack(anchor="w", pady=(5, 0))
    
    # --- Botones de acción ---
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=20)
    
    if es_vendedor:
        # El vendedor puede editar, eliminar, promocionar o ver las contraofertas disponibles
        def on_editar():
            from src.ui.productos.editar_window import open_editar_producto
            win.destroy()
            open_editar_producto(parent, id_producto, username_actual)
        
        def on_eliminar():
            from src.services.productos.productos_service import eliminar_producto
            from src.db.db_app import begin_transaction, commit, rollback
            
            if not messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar este producto?"):
                return
            
            cn = begin_transaction()
            try:
                eliminar_producto(cn, id_producto, username_actual)
                commit(cn)
                messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")
                win.destroy()
            except ValueError as e:
                rollback(cn)
                messagebox.showerror("Error", str(e))
            except Exception as e:
                rollback(cn)
                messagebox.showerror("Error", f"Error al eliminar: {e}")
        
        def on_promocionar():
            from src.ui.productos.promocionar_window import open_promocionar_producto
            open_promocionar_producto(win, id_producto, username_actual)
        
        def on_mostrar_contraofertas():
            from src.ui.productos.contraofertas_window import open_gestionar_contraofertas
            open_gestionar_contraofertas(win, id_producto)
        
        tk.Button(
            btn_frame,
            text="✏️ Editar",
            command=on_editar,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Eliminar",
            command=on_eliminar,
            width=12,
            fg="red"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="🚀 Promocionar",
            command=on_promocionar,
            width=12,
            fg="orange"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            text="📨 Ver contraofertas",
            command=lambda: on_mostrar_contraofertas(),
            width=18,
            font=("Arial", 10, "bold")
        ).pack(pady=5)

    else:
        # El comprador puede comprar, hacer contraoferta o añadir a favoritos
        def on_comprar():
            from src.services.ventas.ventas_service import realizar_compra_directa
            from src.db.db_app import begin_transaction, commit, rollback
            cn = begin_transaction()

            try:
                realizar_compra_directa(cn, id_producto, username_actual)
                commit(cn)
                messagebox.showinfo("Compra producto", "Producto comprado.")
            except Exception as e:
                rollback(cn)
                messagebox.showerror("Error", f"Error al comprar producto: {e}")
        
        def on_contraoferta():
            from src.ui.productos.realizar_contraoferta_window import open_realizar_contraoferta
            open_realizar_contraoferta(id_producto, username_actual)
        
        def on_favorito():
            from src.services.feed_busqueda_favs.favoritos_service import add_favorito
            from src.db.db_app import begin_transaction, commit, rollback
            
            cn = begin_transaction()
            try:
                add_favorito(cn, username_actual, id_producto)
                commit(cn)
                messagebox.showinfo("Favorito", "Producto añadido a favoritos.")
            except Exception as e:
                rollback(cn)
                messagebox.showerror("Error", f"Error al añadir a favoritos: {e}")
        
        tk.Button(
            btn_frame,
            text="🛒 Comprar",
            command=on_comprar,
            bg="#4CAF50",
            fg="white",
            width=12,
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="💬 Contraoferta",
            command=on_contraoferta,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="❤️ Favorito",
            command=on_favorito,
            width=12
        ).pack(side=tk.LEFT, padx=5)
    
    # Botón cerrar
    tk.Button(
        btn_frame,
        text="Cerrar",
        command=win.destroy,
        width=10
    ).pack(side=tk.LEFT, padx=5)


def show_detalle_view(parent, id_producto: int, username_actual: str, origen: str = "mis_productos"):
    """Muestra el detalle de un producto en el content_frame (vista embebida).
    
    Args:
        parent: Frame contenedor (content_frame)
        id_producto: ID del producto a mostrar
        username_actual: Usuario que está viendo el producto
        origen: De dónde se llamó ("mis_productos", "feed", "favoritos")
    """
    from src.services.productos.productos_service import consultar_producto
    
    # Helper para volver según origen
    def volver_segun_origen():
        if origen == "feed":
            from src.ui.feed.feed_window import show_feed_view
            show_feed_view(parent, username_actual)
        elif origen == "favoritos":
            from src.ui.favoritos.favoritos_window import show_favoritos_view
            show_favoritos_view(parent, username_actual)
        else:  # mis_productos o default
            from src.ui.productos.mis_productos_window import show_mis_productos_view
            show_mis_productos_view(parent, username_actual)
    
    # Limpiar contenido anterior
    for widget in parent.winfo_children():
        widget.destroy()
    
    # Cargar datos del producto
    producto = None
    try:
        with connect() as cn:
            producto = consultar_producto(cn, id_producto)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        volver_segun_origen()
        return
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el producto: {e}")
        volver_segun_origen()
        return
    
    if not producto:
        messagebox.showerror("Error", "Producto no encontrado.")
        volver_segun_origen()
        return
    
    es_vendedor = producto.get("username_vendedor") == username_actual
    
    # Frame principal
    main_frame = tk.Frame(parent, bg="white", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Header con botón volver
    header = tk.Frame(main_frame, bg="white")
    header.pack(fill=tk.X, pady=(0, 15))
    
    tk.Button(
        header,
        text="← Volver",
        command=volver_segun_origen,
        relief=tk.FLAT,
        font=("Arial", 10)
    ).pack(side=tk.LEFT)
    
    tk.Label(
        header,
        text="📋 Detalle de Producto",
        font=("Arial", 16, "bold"),
        bg="white"
    ).pack(side=tk.LEFT, padx=20)
    
    # Contenedor con scroll
    canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    content = tk.Frame(canvas, bg="white")
    
    content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=content, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Imagen del producto
    imagen_data = producto.get("imagen")
    if imagen_data and PIL_AVAILABLE:
        try:
            image = Image.open(BytesIO(imagen_data))
            image.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(image)
            
            img_label = tk.Label(content, image=photo, bg="white")
            img_label.image = photo
            img_label.pack(anchor="w", pady=(0, 15))
        except:
            pass
    
    # Título
    tk.Label(
        content, 
        text=producto.get("titulo", "Sin título"),
        font=("Arial", 18, "bold"),
        bg="white",
        wraplength=500
    ).pack(anchor="w", pady=(0, 10))
    
    # Precio
    precio = producto.get("precio", 0)
    tk.Label(
        content,
        text=f"{precio:.2f} €",
        font=("Arial", 22, "bold"),
        fg="#4CAF50",
        bg="white"
    ).pack(anchor="w", pady=(0, 10))
    
    # Categoría y promoción
    info_row = tk.Frame(content, bg="white")
    info_row.pack(anchor="w", pady=(0, 10))
    
    tk.Label(
        info_row,
        text=f"📁 {producto.get('nombre_categoria', 'Sin categoría')}",
        font=("Arial", 10),
        bg="white",
        fg="gray"
    ).pack(side=tk.LEFT, padx=(0, 20))
    
    promocion = producto.get("promocion", 0)
    if promocion and promocion > 0:
        tk.Label(
            info_row,
            text=f"🔥 Promoción: {promocion:.0%}",
            font=("Arial", 10),
            bg="white",
            fg="orange"
        ).pack(side=tk.LEFT)
    
    # Descripción
    tk.Label(content, text="Descripción", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(15, 5))
    descripcion = producto.get("descripcion", "Sin descripción") or "Sin descripción"
    
    desc_text = tk.Text(content, height=4, width=60, wrap=tk.WORD)
    desc_text.insert("1.0", descripcion)
    desc_text.config(state=tk.DISABLED, bg="#f5f5f5")
    desc_text.pack(anchor="w", pady=(0, 15))
    
    # Vendedor
    vendedor_frame = tk.Frame(content, bg="#f0f0f0", padx=15, pady=10)
    vendedor_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(vendedor_frame, text="Vendedor:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(side=tk.LEFT)
    tk.Label(
        vendedor_frame,
        text=f"@{producto.get('username_vendedor', 'desconocido')}",
        font=("Arial", 11),
        fg="blue",
        bg="#f0f0f0"
    ).pack(side=tk.LEFT, padx=10)
    
    valoracion = producto.get("valoracion_vendedor")
    if valoracion and valoracion > 0:
        tk.Label(vendedor_frame, text=f"⭐ {valoracion:.1f}", font=("Arial", 10), bg="#f0f0f0").pack(side=tk.LEFT)
    
    # Botones de acción
    btn_frame = tk.Frame(content, bg="white")
    btn_frame.pack(pady=20)
    
    if es_vendedor:
        def on_editar():
            from src.ui.productos.editar_window import show_editar_view
            show_editar_view(parent, id_producto, username_actual)
        
        def on_promocionar():
            from src.ui.productos.promocionar_window import show_promocionar_view
            show_promocionar_view(parent, id_producto, username_actual)
        
        def on_eliminar():
            from src.services.productos.productos_service import eliminar_producto
            from src.db.db_app import begin_transaction, commit, rollback
            
            if not messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
                return
            
            cn = begin_transaction()
            try:
                eliminar_producto(cn, id_producto, username_actual)
                commit(cn)
                messagebox.showinfo("Eliminado", "Producto eliminado.")
                from src.ui.productos.mis_productos_window import show_mis_productos_view
                show_mis_productos_view(parent, username_actual)
            except ValueError as e:
                rollback(cn)
                messagebox.showerror("Error", str(e))
            except Exception as e:
                rollback(cn)
                messagebox.showerror("Error", f"Error: {e}")
        
        def on_mostrar_contraofertas():
            from src.ui.productos.contraofertas_window import open_gestionar_contraofertas
            open_gestionar_contraofertas(parent, id_producto)

        tk.Button(btn_frame, text="✏️ Editar", command=on_editar, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🚀 Promocionar", command=on_promocionar, width=12, fg="orange").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", command=on_eliminar, width=12, fg="red").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📨 Ver contraofertas", command=on_mostrar_contraofertas, width=14, fg="black").pack(side=tk.LEFT, padx=5)
    else:
        def on_comprar():
            from src.services.ventas.ventas_service import realizar_compra_directa
            from src.db.db_app import begin_transaction, commit, rollback
            cn = begin_transaction()

            try:
                realizar_compra_directa(cn, id_producto, username_actual)
                commit(cn)
                messagebox.showinfo("Compra producto", "Producto comprado.")
            except Exception as e:
                rollback(cn)
                messagebox.showerror("Error", f"Error al comprar producto: {e}")
        
        def on_contraoferta():
            from src.ui.productos.realizar_contraoferta_window import open_realizar_contraoferta
            open_realizar_contraoferta(id_producto, username_actual)
        
        def on_favorito():
            from src.services.feed_busqueda_favs.favoritos_service import add_favorito
            from src.db.db_app import begin_transaction, commit, rollback
            
            cn = begin_transaction()
            try:
                add_favorito(cn, username_actual, id_producto)
                commit(cn)
                messagebox.showinfo("Favorito", "Añadido a favoritos.")
            except Exception as e:
                rollback(cn)
                messagebox.showerror("Error", str(e))
        
        tk.Button(btn_frame, text="🛒 Comprar", command=on_comprar, bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="💬 Contraoferta", command=on_contraoferta, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❤️ Favorito", command=on_favorito, width=12).pack(side=tk.LEFT, padx=5)
