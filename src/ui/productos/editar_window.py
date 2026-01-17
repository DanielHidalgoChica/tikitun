"""
Ventana para editar un producto existente (RF2.2).
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.db.db_app import begin_transaction, commit, rollback, connect
from src.services.productos.productos_service import (
    consultar_producto, 
    modificar_producto, 
    get_categorias
)


def open_editar_producto(parent, id_producto: int, username: str):
    """Abre la ventana de edición de producto.
    
    Args:
        parent: Ventana padre
        id_producto: ID del producto a editar
        username: Usuario que edita (debe ser el vendedor)
    """
    win = tk.Toplevel(parent)
    win.title("Editar Producto")
    win.geometry("500x480")
    win.resizable(False, False)
    
    # Cargar datos actuales del producto y categorías
    producto = None
    categorias = []
    try:
        with connect() as cn:
            producto = consultar_producto(cn, id_producto)
            categorias = get_categorias(cn)
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
    
    # Verificar permisos
    if producto.get("username_vendedor") != username:
        messagebox.showerror("Error", "No tienes permiso para editar este producto.")
        win.destroy()
        return
    
    # Variable para guardar la imagen seleccionada
    imagen_bytes = {"data": None, "changed": False}
    
    # --- Formulario ---
    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # ID (solo lectura)
    tk.Label(frame, text=f"ID: {id_producto}", font=("Arial", 10), fg="gray").grid(
        row=0, column=0, sticky="w", pady=(0, 10)
    )
    
    # Título
    tk.Label(frame, text="Título *", font=("Arial", 10, "bold")).grid(
        row=1, column=0, sticky="w", pady=(0, 5)
    )
    e_titulo = tk.Entry(frame, width=50)
    e_titulo.insert(0, producto.get("titulo", ""))
    e_titulo.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    tk.Label(frame, text="(máx. 80 caracteres)", font=("Arial", 8), fg="gray").grid(
        row=2, column=2, sticky="w", padx=5
    )
    
    # Descripción
    tk.Label(frame, text="Descripción", font=("Arial", 10, "bold")).grid(
        row=3, column=0, sticky="w", pady=(0, 5)
    )
    t_descripcion = tk.Text(frame, width=50, height=5)
    t_descripcion.insert("1.0", producto.get("descripcion", ""))
    t_descripcion.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    tk.Label(frame, text="(máx. 500 caracteres)", font=("Arial", 8), fg="gray").grid(
        row=4, column=2, sticky="nw", padx=5
    )
    
    # Precio
    tk.Label(frame, text="Precio (€) *", font=("Arial", 10, "bold")).grid(
        row=5, column=0, sticky="w", pady=(0, 5)
    )
    e_precio = tk.Entry(frame, width=20)
    e_precio.insert(0, f"{producto.get('precio', 0):.2f}")
    e_precio.grid(row=6, column=0, sticky="w", pady=(0, 10))
    
    # Categoría
    tk.Label(frame, text="Categoría *", font=("Arial", 10, "bold")).grid(
        row=7, column=0, sticky="w", pady=(0, 5)
    )
    categoria_var = tk.StringVar(value=producto.get("nombre_categoria", ""))
    cb_categoria = ttk.Combobox(
        frame, 
        textvariable=categoria_var,
        values=categorias,
        state="readonly",
        width=30
    )
    cb_categoria.grid(row=8, column=0, sticky="w", pady=(0, 10))
    
    # Seleccionar la categoría actual
    cat_actual = producto.get("nombre_categoria", "")
    if cat_actual in categorias:
        cb_categoria.current(categorias.index(cat_actual))
    
    # Imagen (opcional)
    tk.Label(frame, text="Imagen (opcional)", font=("Arial", 10, "bold")).grid(
        row=9, column=0, sticky="w", pady=(0, 5)
    )
    lbl_imagen = tk.Label(frame, text="Sin cambios", fg="gray")
    lbl_imagen.grid(row=10, column=0, sticky="w")
    
    def seleccionar_imagen():
        filepath = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png"), ("Todos", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, "rb") as f:
                    imagen_bytes["data"] = f.read()
                    imagen_bytes["changed"] = True
                lbl_imagen.config(text=filepath.split("/")[-1], fg="green")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer la imagen: {e}")
    
    btn_imagen = tk.Button(frame, text="Cambiar...", command=seleccionar_imagen)
    btn_imagen.grid(row=10, column=1, sticky="w", padx=10)
    
    # --- Botones ---
    btn_frame = tk.Frame(frame)
    btn_frame.grid(row=11, column=0, columnspan=3, pady=20)
    
    def on_guardar():
        cn = begin_transaction()
        try:
            cambios = {
                "titulo": e_titulo.get().strip(),
                "descripcion": t_descripcion.get("1.0", tk.END).strip(),
                "precio": e_precio.get().strip(),
                "nombre_categoria": categoria_var.get(),
            }
            
            if imagen_bytes["changed"]:
                cambios["imagen"] = imagen_bytes["data"]
            
            modificar_producto(cn, id_producto, username, cambios)
            commit(cn)
            
            messagebox.showinfo("Guardado", "Producto modificado correctamente.")
            win.destroy()
            
        except ValueError as ex:
            rollback(cn)
            messagebox.showerror("Error de validación", str(ex))
        except Exception as ex:
            rollback(cn)
            messagebox.showerror("Error", f"Error al guardar: {ex}")
    
    def on_cancelar():
        win.destroy()
    
    tk.Button(
        btn_frame, 
        text="Guardar Cambios", 
        command=on_guardar,
        bg="#4CAF50",
        fg="white",
        width=15,
        font=("Arial", 10, "bold")
    ).pack(side=tk.LEFT, padx=10)
    
    tk.Button(
        btn_frame,
        text="Cancelar",
        command=on_cancelar,
        width=15
    ).pack(side=tk.LEFT, padx=10)


def show_editar_view(parent, id_producto: int, username: str):
    """Muestra el formulario de edición en el content_frame (vista embebida).
    
    Args:
        parent: Frame contenedor (content_frame)
        id_producto: ID del producto a editar
        username: Usuario que edita (debe ser el vendedor)
    """
    # Limpiar contenido anterior
    for widget in parent.winfo_children():
        widget.destroy()
    
    # Cargar datos actuales del producto y categorías
    producto = None
    categorias = []
    try:
        with connect() as cn:
            producto = consultar_producto(cn, id_producto)
            categorias = get_categorias(cn)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        from src.ui.productos.mis_productos_window import show_mis_productos_view
        show_mis_productos_view(parent, username)
        return
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el producto: {e}")
        from src.ui.productos.mis_productos_window import show_mis_productos_view
        show_mis_productos_view(parent, username)
        return
    
    if not producto:
        messagebox.showerror("Error", "Producto no encontrado.")
        from src.ui.productos.mis_productos_window import show_mis_productos_view
        show_mis_productos_view(parent, username)
        return
    
    if producto.get("username_vendedor") != username:
        messagebox.showerror("Error", "No tienes permiso para editar este producto.")
        from src.ui.productos.mis_productos_window import show_mis_productos_view
        show_mis_productos_view(parent, username)
        return
    
    imagen_bytes = {"data": None, "changed": False}
    
    # Frame principal
    main_frame = tk.Frame(parent, bg="white", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Header con botón volver
    header = tk.Frame(main_frame, bg="white")
    header.pack(fill=tk.X, pady=(0, 20))
    
    def on_volver():
        from src.ui.productos.detalle_window import show_detalle_view
        show_detalle_view(parent, id_producto, username)
    
    tk.Button(
        header,
        text="← Volver",
        command=on_volver,
        relief=tk.FLAT,
        font=("Arial", 10)
    ).pack(side=tk.LEFT)
    
    tk.Label(
        header,
        text=f"✏️ Editar Producto (ID: {id_producto})",
        font=("Arial", 16, "bold"),
        bg="white"
    ).pack(side=tk.LEFT, padx=20)
    
    # Formulario
    form_frame = tk.Frame(main_frame, bg="white")
    form_frame.pack(fill=tk.BOTH, expand=True)
    
    # Título
    tk.Label(form_frame, text="Título *", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
    e_titulo = tk.Entry(form_frame, width=60)
    e_titulo.insert(0, producto.get("titulo", ""))
    e_titulo.pack(anchor="w", pady=(0, 10))
    
    # Descripción
    tk.Label(form_frame, text="Descripción", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
    t_descripcion = tk.Text(form_frame, width=60, height=4)
    t_descripcion.insert("1.0", producto.get("descripcion", ""))
    t_descripcion.pack(anchor="w", pady=(0, 10))
    
    # Precio y Categoría
    row_frame = tk.Frame(form_frame, bg="white")
    row_frame.pack(fill=tk.X, pady=(0, 10))
    
    precio_frame = tk.Frame(row_frame, bg="white")
    precio_frame.pack(side=tk.LEFT, padx=(0, 30))
    tk.Label(precio_frame, text="Precio (€) *", font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
    e_precio = tk.Entry(precio_frame, width=15)
    e_precio.insert(0, f"{producto.get('precio', 0):.2f}")
    e_precio.pack(anchor="w")
    
    cat_frame = tk.Frame(row_frame, bg="white")
    cat_frame.pack(side=tk.LEFT)
    tk.Label(cat_frame, text="Categoría *", font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
    categoria_var = tk.StringVar(value=producto.get("nombre_categoria", ""))
    cb_categoria = ttk.Combobox(cat_frame, textvariable=categoria_var, values=categorias, state="readonly", width=25)
    cb_categoria.pack(anchor="w")
    cat_actual = producto.get("nombre_categoria", "")
    if cat_actual in categorias:
        cb_categoria.current(categorias.index(cat_actual))
    
    # Imagen
    img_frame = tk.Frame(form_frame, bg="white")
    img_frame.pack(fill=tk.X, pady=10)
    
    tk.Label(img_frame, text="Imagen", font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
    
    img_row = tk.Frame(img_frame, bg="white")
    img_row.pack(anchor="w", pady=5)
    
    lbl_imagen = tk.Label(img_row, text="Sin cambios", fg="gray", bg="white")
    lbl_imagen.pack(side=tk.LEFT)
    
    def seleccionar_imagen():
        filepath = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png"), ("Todos", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, "rb") as f:
                    imagen_bytes["data"] = f.read()
                    imagen_bytes["changed"] = True
                lbl_imagen.config(text=f"✓ {filepath.split('/')[-1]}", fg="green")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer la imagen: {e}")
    
    tk.Button(img_row, text="Cambiar...", command=seleccionar_imagen).pack(side=tk.LEFT, padx=10)
    
    # Botones
    btn_frame = tk.Frame(form_frame, bg="white")
    btn_frame.pack(pady=20)
    
    def on_guardar():
        cn = begin_transaction()
        try:
            cambios = {
                "titulo": e_titulo.get().strip(),
                "descripcion": t_descripcion.get("1.0", tk.END).strip(),
                "precio": e_precio.get().strip(),
                "nombre_categoria": categoria_var.get(),
            }
            
            if imagen_bytes["changed"]:
                cambios["imagen"] = imagen_bytes["data"]
            
            modificar_producto(cn, id_producto, username, cambios)
            commit(cn)
            
            messagebox.showinfo("Guardado", "Producto modificado correctamente.")
            from src.ui.productos.detalle_window import show_detalle_view
            show_detalle_view(parent, id_producto, username)
            
        except ValueError as ex:
            rollback(cn)
            messagebox.showerror("Error de validación", str(ex))
        except Exception as ex:
            rollback(cn)
            messagebox.showerror("Error", f"Error al guardar: {ex}")
    
    tk.Button(
        btn_frame, 
        text="✓ Guardar Cambios", 
        command=on_guardar,
        bg="#4CAF50",
        fg="white",
        width=18,
        font=("Arial", 11, "bold")
    ).pack(side=tk.LEFT, padx=10)
    
    tk.Button(
        btn_frame,
        text="Cancelar",
        command=on_volver,
        width=12
    ).pack(side=tk.LEFT, padx=10)
