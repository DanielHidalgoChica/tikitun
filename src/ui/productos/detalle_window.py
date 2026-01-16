"""
Ventana de detalle de producto (RF2.4).
Muestra información completa del producto y permite acciones según el usuario.
"""
import tkinter as tk
from tkinter import messagebox
from src.db.db_app import connect


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
    win.geometry("550x500")
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
    
    desc_text = tk.Text(frame, height=6, width=60, wrap=tk.WORD, state=tk.NORMAL)
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
        # El vendedor puede editar o eliminar
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
    else:
        # El comprador puede comprar, hacer contraoferta o añadir a favoritos
        def on_comprar():
            messagebox.showinfo("Comprar", "Funcionalidad de compra (RF4.1) pendiente de implementar.")
        
        def on_contraoferta():
            messagebox.showinfo("Contraoferta", "Funcionalidad de contraoferta (RF4.2) pendiente de implementar.")
        
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
