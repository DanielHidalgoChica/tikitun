import tkinter as tk
from tkinter import messagebox, ttk
from src.db.db_app import connect
from src.repositories.perfiles import usuarios_repo
from src.repositories.productos import productos_repo


def show_perfil_view(parent_frame, username="bob"):
    """
    Muestra la vista de gestión de perfil (RF1.2).
    
    Consulta:
    - Información del perfil del usuario
    - Lista de productos disponibles ofertados
    """
    # Limpiar el frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Cargar datos del usuario
    try:
        with connect() as cn:
            usuario = usuarios_repo.get_usuario(cn, username)
            if usuario is None or usuario.get("cuenta_eliminada"):
                messagebox.showerror("Error", "El usuario no existe o ha sido eliminado")
                tk.Label(parent_frame, text="Usuario no encontrado").pack(pady=20)
                return
            
            # Obtener productos disponibles
            productos_disponibles = productos_repo.get_productos_usuario(cn, username)
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando perfil: {e}")
        tk.Label(parent_frame, text="Error al cargar el perfil").pack(pady=20)
        return
    
    # === SECCIÓN DE INFORMACIÓN DEL PERFIL ===
    frm_info = tk.LabelFrame(parent_frame, text="Información del Perfil", padx=15, pady=15)
    frm_info.pack(padx=10, pady=10, fill=tk.X)
    
    # Nombre completo y username
    tk.Label(frm_info, text=f"Nombre: {usuario.get('nombre_completo', 'N/A')}", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
    tk.Label(frm_info, text=f"Usuario: @{username}", font=("Arial", 11)).pack(anchor="w", pady=2)
    
    # Saldo
    saldo = usuario.get("saldo", 0.0)
    tk.Label(frm_info, text=f"Saldo: €{saldo:.2f}", font=("Arial", 11)).pack(anchor="w", pady=2)
    
    # Valoración media
    valoracion = usuario.get("valoracion_media", 0)
    val_texto = f"{valoracion:.1f}" if valoracion else "Sin valoraciones"
    tk.Label(frm_info, text=f"Valoración media: {val_texto} ⭐", font=("Arial", 11)).pack(anchor="w", pady=2)
    
    # === SECCIÓN DE PRODUCTOS DISPONIBLES ===
    frm_disponibles = tk.LabelFrame(parent_frame, text="Productos Disponibles para la Venta", padx=10, pady=10)
    frm_disponibles.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)
    
    if productos_disponibles:
        # Crear tabla de productos disponibles
        tree_disp = ttk.Treeview(
            frm_disponibles,
            columns=("ID", "Título", "Precio"),
            height=min(5, len(productos_disponibles)),
            show="headings"
        )
        tree_disp.column("ID", width=50)
        tree_disp.column("Título", width=250)
        tree_disp.column("Precio", width=100)
        
        tree_disp.heading("ID", text="ID")
        tree_disp.heading("Título", text="Título")
        tree_disp.heading("Precio", text="Precio")
        
        for prod in productos_disponibles:
            tree_disp.insert("", tk.END, values=(
                prod["id_producto"],
                prod["titulo"],
                f"€{prod['precio']:.2f}"
            ))
        
        tree_disp.pack(fill=tk.BOTH, expand=True)
    else:
        tk.Label(frm_disponibles, text="No tienes productos disponibles en venta", fg="gray").pack(pady=20)
    
    # === BOTONES DE ACCIÓN ===
    frm_acciones = tk.Frame(parent_frame)
    frm_acciones.pack(pady=15)
    
    tk.Button(
        frm_acciones,
        text="Editar Perfil",
        width=20,
        state=tk.DISABLED
    ).grid(row=0, column=0, padx=5)
    
    tk.Button(
        frm_acciones,
        text="Gestionar Monedero",
        width=20,
        state=tk.DISABLED
    ).grid(row=0, column=1, padx=5)
    
    tk.Button(
        frm_acciones,
        text="Dar de Baja",
        width=20,
        state=tk.DISABLED,
        fg="red"
    ).grid(row=0, column=2, padx=5)
