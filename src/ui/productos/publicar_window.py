"""
Ventana para publicar un nuevo producto (RF2.1).
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.db.db_app import begin_transaction, commit, rollback, connect
from src.services.productos.productos_service import publicar_producto, get_categorias


def open_publicar_producto(parent, username: str = "bob"):
    """Abre la ventana de publicación de producto.
    
    Args:
        parent: Ventana padre
        username: Usuario que publica el producto
    """
    win = tk.Toplevel(parent)
    win.title("Publicar Producto")
    win.geometry("500x450")
    win.resizable(False, False)
    
    # Cargar categorías desde la BD
    categorias = []
    try:
        with connect() as cn:
            categorias = get_categorias(cn)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las categorías: {e}")
    
    # Variable para guardar la imagen seleccionada
    imagen_bytes = {"data": None, "filename": ""}
    
    # --- Formulario ---
    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Título
    tk.Label(frame, text="Título *", font=("Arial", 10, "bold")).grid(
        row=0, column=0, sticky="w", pady=(0, 5)
    )
    e_titulo = tk.Entry(frame, width=50)
    e_titulo.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    tk.Label(frame, text="(máx. 80 caracteres)", font=("Arial", 8), fg="gray").grid(
        row=1, column=2, sticky="w", padx=5
    )
    
    # Descripción
    tk.Label(frame, text="Descripción", font=("Arial", 10, "bold")).grid(
        row=2, column=0, sticky="w", pady=(0, 5)
    )
    t_descripcion = tk.Text(frame, width=50, height=5)
    t_descripcion.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    tk.Label(frame, text="(máx. 500 caracteres)", font=("Arial", 8), fg="gray").grid(
        row=3, column=2, sticky="nw", padx=5
    )
    
    # Precio
    tk.Label(frame, text="Precio (€) *", font=("Arial", 10, "bold")).grid(
        row=4, column=0, sticky="w", pady=(0, 5)
    )
    e_precio = tk.Entry(frame, width=20)
    e_precio.grid(row=5, column=0, sticky="w", pady=(0, 10))
    
    # Categoría
    tk.Label(frame, text="Categoría *", font=("Arial", 10, "bold")).grid(
        row=6, column=0, sticky="w", pady=(0, 5)
    )
    categoria_var = tk.StringVar()
    cb_categoria = ttk.Combobox(
        frame, 
        textvariable=categoria_var,
        values=categorias,
        state="readonly",
        width=30
    )
    cb_categoria.grid(row=7, column=0, sticky="w", pady=(0, 10))
    if categorias:
        cb_categoria.current(0)
    
    # Imagen (opcional)
    tk.Label(frame, text="Imagen (opcional)", font=("Arial", 10, "bold")).grid(
        row=8, column=0, sticky="w", pady=(0, 5)
    )
    lbl_imagen = tk.Label(frame, text="No seleccionada", fg="gray")
    lbl_imagen.grid(row=9, column=0, sticky="w")
    
    def seleccionar_imagen():
        filepath = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png"), ("Todos", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, "rb") as f:
                    imagen_bytes["data"] = f.read()
                    imagen_bytes["filename"] = filepath.split("/")[-1]
                lbl_imagen.config(text=imagen_bytes["filename"], fg="green")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer la imagen: {e}")
    
    btn_imagen = tk.Button(frame, text="Seleccionar...", command=seleccionar_imagen)
    btn_imagen.grid(row=9, column=1, sticky="w", padx=10)
    
    # Vendedor (solo lectura, muestra el usuario actual)
    tk.Label(frame, text="Vendedor", font=("Arial", 10, "bold")).grid(
        row=10, column=0, sticky="w", pady=(10, 5)
    )
    lbl_vendedor = tk.Label(frame, text=f"@{username}", font=("Arial", 10), fg="blue")
    lbl_vendedor.grid(row=11, column=0, sticky="w")
    
    # --- Botones ---
    btn_frame = tk.Frame(frame)
    btn_frame.grid(row=12, column=0, columnspan=3, pady=20)
    
    def on_guardar():
        cn = begin_transaction()
        try:
            data = {
                "titulo": e_titulo.get().strip(),
                "descripcion": t_descripcion.get("1.0", tk.END).strip(),
                "precio": e_precio.get().strip(),
                "nombre_categoria": categoria_var.get(),
                "imagen": imagen_bytes["data"],
                "username_vendedor": username,
            }
            
            new_id = publicar_producto(cn, data)
            commit(cn)
            
            messagebox.showinfo(
                "Producto Publicado",
                f"¡Producto publicado correctamente!\n\nID: {new_id}\nTítulo: {data['titulo']}"
            )
            win.destroy()
            
        except ValueError as ex:
            rollback(cn)
            messagebox.showerror("Error de validación", str(ex))
        except Exception as ex:
            rollback(cn)
            messagebox.showerror("Error", f"Error al publicar: {ex}")
    
    def on_cancelar():
        win.destroy()
    
    tk.Button(
        btn_frame, 
        text="Publicar", 
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
